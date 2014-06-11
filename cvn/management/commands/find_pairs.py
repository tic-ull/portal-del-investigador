# -*- encoding: UTF-8 -*-

from cvn.models import (Proyecto, Congreso, Convenio, Articulo,
                        TesisDoctoral, Libro, Capitulo)
from core.models import UserProfile
from django.conf import settings as st
from django.core.management.base import BaseCommand, CommandError
from joblib import Parallel, delayed
from optparse import make_option
from string_utils.stringcmp import do_stringcmp
import logging
import os
import signal
import subprocess
import time

logger = logging.getLogger(__name__)


def signal_handler(signal, frame):
    return None


def difering_fields(obj1, obj2, EXCLUDE_FIELDS=[]):
    difering = []
    tipo = type(obj1)
    fields = tipo._meta.get_all_field_names()
    for f in fields:
        if f not in EXCLUDE_FIELDS:
            f1 = obj1.__getattribute__(f)
            f2 = obj2.__getattribute__(f)
            if f1 and f2 and f1 != f2:
                difering.append(f)
    return len(difering)


def log_print(message):
    print message
    logger.info(message)


def backupDatabase(username, dbname, port):
    dbName = st.DATABASES['historica']['NAME']
    filePath = '%s/%s.%s.gz' % (st.BACKUP_DIR, dbName,
                                time.strftime('%Y-%m-%d-%Hh%Mm%Ss'))
    params = 'export PGPASSWORD=%s\npg_dump -U%s -h %s %s | gzip -9 -c > %s' \
        % (st.DATABASES['historica']['PASSWORD'],
           st.DATABASES['historica']['USER'],
           st.DATABASES['historica']['HOST'],
           dbName, filePath)

    if not os.path.exists(st.BACKUP_DIR):
        os.mkdir(st.BACKUP_DIR)
    proc = subprocess.Popen([params], stderr=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    if err:
        os.remove(filePath)
    return err


def findDup(i, registros, NAME_FIELD, LIMIT):
    duplicates = {}
    pry1 = registros[i]
    for pry2 in registros[i + 1:]:
        pry1_name = pry1.__getattribute__(NAME_FIELD)
        pry2_name = pry2.__getattribute__(NAME_FIELD)
        if pry1_name and pry2_name:
            percentage, time = do_stringcmp("qgram3avrg",
                                            pry1_name.lower(),
                                            pry2_name.lower())
            if percentage > LIMIT:
                pair = tuple([pry1, pry2])
                duplicates[pair] = percentage
    return duplicates


class Command(BaseCommand):
    help = u'Encuentra registros sospechosos de estar duplicados'
    option_list = BaseCommand.option_list + (
        make_option(
            "-u",
            "--document",
            dest="usuario",
            default=False,
            help="specify ID document for duplicate control. Use 'all'.",
        ),
        make_option(
            "-t",
            "--table",
            dest="table",
            help="specify table for duplicate control",
        ),
        make_option(
            "-d",
            "--diff",
            dest="differing_pairs",
            help="specify the number of differing pairs for duplicate control",
        ),
        make_option(
            "-y",
            "--year",
            dest="year",
            default=False,
            help="specify the year for searching in format XXXX or use 'all'",
        ),
    )

    TABLES = {'Proyecto': Proyecto,
              'Articulo': Articulo,
              'Libro': Libro,
              'Capitulo': Capitulo,
              'Congreso': Congreso,
              'Convenio': Convenio,
              'Tesis': TesisDoctoral}

    NAME_FIELDS = {'Proyecto': 'denominacion_del_proyecto',
                   'Articulo': 'titulo',
                   'Libro': 'titulo',
                   'Capitulo': 'titulo',
                   'Congreso': 'titulo',
                   'Convenio': 'denominacion_del_proyecto',
                   'Tesis': 'titulo'}

    TIMESTAMP_FIELDS = ['updated_at', 'created_at', ]

    DONT_SET_FIELDS = ['id', 'usuario', ]

    DONT_CHECK_FIELDS = TIMESTAMP_FIELDS + DONT_SET_FIELDS

    # mínima similitud para considerar dos registros como duplicados
    LIMIT = 0.75

    # Default value. No contamos la denominación
    DIFFERING_PAIRS = 0

    FIELD_WIDTH = 28
    COLWIDTH = 50

    def print_cabecera_registro(self, pry1, pry2, duplicates,
                                pair, model_fields, count):
        os.system("clear")
        log_print("=====================================================")
        log_print(" ID1 = {0} comparado con ID2 = {1} ({2:2.2f}%) {3}/{4}"
                  .format(pry1.id, pry2.id, duplicates[pair] * 100,
                          count, len(duplicates)))
        log_print("=====================================================")
        log_print("Field".ljust(self.FIELD_WIDTH)
                  + "ID1".ljust(self.COLWIDTH)
                  + "ID2".ljust(self.COLWIDTH))
        log_print("-" * (self.FIELD_WIDTH + 2 * self.COLWIDTH))
        for f in model_fields:
            if f not in (self.DONT_SET_FIELDS +
                         self.TIMESTAMP_FIELDS):
                f1 = pry1.__getattribute__(f)
                f1 = "" if f1 is None else f1
                f2 = pry2.__getattribute__(f)
                f2 = "" if f2 is None else f2
                if (f1 != f2):
                    log_print(unicode(f)[:self.FIELD_WIDTH - 1]
                              .ljust(self.FIELD_WIDTH)
                              + unicode(f1)[:self.COLWIDTH - 1]
                              .ljust(self.COLWIDTH)
                              + unicode(f2)[:self.COLWIDTH - 1]
                              .ljust(self.COLWIDTH))
        log_print("-" * (self.FIELD_WIDTH + 2 * self.COLWIDTH))

    def checkArgs(self, options):
        if options['table'] is None:
            raise CommandError("Option `--table=...` must be specified.")
        else:
            if options['table'] in self.TABLES:
                TABLE = self.TABLES[options['table']]
                NAME_FIELD = self.NAME_FIELDS[options['table']]
            else:
                raise CommandError("\"{0}\" is not a table. Use Proyecto, " +
                                   "Convenio, Articulo, Libro, Capitulo, " +
                                   "Tesis or Congreso "
                                   .format(options['table']))
        if options['differing_pairs'] is None:
            raise CommandError("Option `--diff=0, 1...` must be specified.")
        else:
            try:
                self.DIFFERING_PAIRS = int(options['differing_pairs'])
            except:
                raise CommandError("Option `--diff needs an integer 0,1,...")
        return TABLE, NAME_FIELD

    def runQueries(self, options, TABLE):
        log_print("Buscando duplicados en el modelo " +
                  "{0}".format(TABLE.__name__))
        if not options['year']:
            registros = TABLE.objects.exclude(usuario=None)
        else:
            self.YEAR = options['year']
            if TABLE == Proyecto:
                registros = TABLE.objects.filter(
                    fecha_de_inicio__year=self.YEAR
                ).exclude(usuario=None)

            elif TABLE in [Articulo, Libro, Capitulo]:
                registros = TABLE.objects.filter(
                    fecha__year=self.YEAR
                ).exclude(usuario=None)

            elif TABLE == Congreso:
                registros = TABLE.objects.filter(
                    fecha_de_inicio__year=self.YEAR
                ).exclude(usuario=None)

            elif TABLE == TesisDoctoral:
                registros = TABLE.objects.filter(
                    fecha__year=self.YEAR
                ).exclude(usuario=None)

            elif TABLE == Convenio:
                registros = TABLE.objects.filter(
                    fecha_de_inicio__year=self.YEAR
                ).exclude(usuario=None)

        if options['usuario']:
            usuario = options['usuario']
            try:
                usuario = UserProfile.objects.get(documento=usuario)
            except:
                raise CommandError('El usuario con documento "{0}" no existe'
                                   .format(usuario))

            if TABLE in [Congreso, Articulo, Libro, Capitulo, Proyecto]:
                registros = registros.filter(usuario=usuario)
            else:
                new_registros = []
                for r in registros:
                    if usuario in r.usuario.all():
                        new_registros.add(r)
                registros = new_registros
        log_print("Total de registros en estudio = {0}".format(len(registros)))
        return registros

    def findDuplicates(self, registros, NAME_FIELD, threads):
        result = Parallel(n_jobs=threads)(delayed(findDup)(
            i, registros, NAME_FIELD, self.LIMIT
        ) for i in range(0, len(registros)))
        duplicates = {}
        for i in result:
            duplicates.update(i)
        log_print("Total duplicates = {0} de {1} "
                  .format(len(duplicates), len(registros)))
        return duplicates

    def mergePair(self, model_fields, pair, master, duplicates, count):
        repeat = True
        while repeat:
            repeat = False
            for f in model_fields:
                if f not in (self.DONT_SET_FIELDS + self.TIMESTAMP_FIELDS):
                    f1 = pair[0].__getattribute__(f)
                    f2 = pair[1].__getattribute__(f)
                    master_f = f1 if f1 else f2
                    if f1 and f2:
                        try:
                            master_f = f1 if len(f1) >= len(f2) else f2
                        except:
                            master_f = f1
                    if f1 and f2 and f1 == f2:
                        attr = f1
                        master.__setattr__(f, attr)
                    if any([f1, f2]) and f1 != f2:
                        self.print_cabecera_registro(pair[0], pair[1],
                                                     duplicates, pair,
                                                     model_fields, count)
                        log_print(f)
                        print "--------------------------------"
                        log_print(u"{0:5d}: {1}".format(pair[0].id, f1))
                        log_print(u"{0:5d}: {1}".format(pair[1].id, f2))
                        print "\n  NEW:", master_f, "\n"
                        print "--------------------------------"
                        choice = self.choice(pair[0], pair[1])

                        # Salir del for => Deja de comparar registros de la
                        # pareja => break

                        # Salir del while => Deja de comparar la pareja. =>
                        # repeat = True continua el while

                        # Reiniciar tupla saliendo del for
                        if choice == -1:
                            repeat = True
                            break
                        # Ignora la tupla saliendo de la función mergePair
                        if choice == 0:
                            return None, False
                        # Ignora la tupla saliendo de mergePair retornando
                        # exit=True
                        if choice == 'q':
                            return None, True
                        # Selecciona el registro recomendado
                        if choice == "":
                            attr = master_f
                        # Selecciona el registro de la tupla 1
                        if choice == 1:
                            attr = f1
                        # Selecciona el registro de la tupla 2
                        if choice == 2:
                            attr = f2
                        master.__setattr__(f, attr)
                        log_print(u"SET TO: {0}".format(attr))
                        log_print(u"----------")
        return master, False

    def confirmDuplicates(self, sorted_pairs, TABLE, NAME_FIELD, duplicates):
        pairs_solved = {}
        count = 0
        for pair in sorted_pairs:
            count += 1
            difering_length = difering_fields(
                pair[0], pair[1], self.DONT_CHECK_FIELDS + [NAME_FIELD])

            if difering_length == self.DIFFERING_PAIRS:
                master = TABLE()
                model_fields = TABLE._meta.get_fields_with_model()
                model_fields = [
                    field[0].get_attname() for field in model_fields
                ]
                master, exit = self.mergePair(model_fields, pair,
                                              master, duplicates, count)
                if master:
                    master.save()
                    pairs_solved[(pair[0].id, pair[1].id)] = master.id
                if exit:
                    log_print("User aborted main loop...")
                    break
        return pairs_solved

    def handle(self, *args, **options):
        TABLE, NAME_FIELD = self.checkArgs(options)
        log_print("Haciendo copia de seguridad de BD")
        error = backupDatabase('viinv', 'memviinv', '5432')
        if error:
            log_print(error)
        else:
            print('Realizando consultas')
            registros = self.runQueries(options, TABLE)
            registros = [p for p in registros]
            print('Buscando parejas de duplicados')
            duplicates = self.findDuplicates(registros, NAME_FIELD, 2)
            sorted_pairs = sorted(duplicates, key=duplicates.get, reverse=True)
            signal.signal(signal.SIGINT, signal_handler)
            pairs_solved = self.confirmDuplicates(sorted_pairs, TABLE,
                                                  NAME_FIELD, duplicates)
            self.commit_changes(TABLE, pairs_solved)

    def commit_changes(self, TABLE, pairs_solved):
        print pairs_solved
        log_print("========================================")
        log_print(u"Número de campos diferentes " +
                  u"(contando la denominación): {0}"
                  .format(self.DIFFERING_PAIRS + 1))
        log_print("========================================")
        log_print("Parejas cambiadas = {0}".format(len(pairs_solved)))
        log_print("========================================")
        log_print("Cambiando los registros afectados en la BBDD")
        for pair, new_id in pairs_solved.iteritems():
            log_print(u"----------")
            log_print("Cambiando usuarios de {0} y {1} a {2}"
                      .format(pair[0], pair[1], new_id))
            master_p = TABLE.objects.get(pk=new_id)
            for pry_id in pair:
                p = TABLE.objects.get(pk=pry_id)
                for u in p.usuario.all():
                    master_p.usuario.add(u)
                    log_print((u"Proyecto {0} [ID={1}] " +
                              u"añadir usuario {2} [ID={3}]")
                              .format(master_p, master_p.id, u, u.id))
                    p.usuario.remove(u)
                    log_print((u"Proyecto {0} [ID={1}] " +
                              u"borrar usuario {2} [ID={3}]")
                              .format(p, p.id, u, u.id))
                p.save()
            master_p.save()

    def choice(self, pry1, pry2):
        print ('Return=NEW\t1=ID1\t2=ID2\t0=Ignorar pareja\t-1=Reniciar' +
               '\tq=save_and_abort')
        choice = None
        while (choice not in ["", 1, 2, -1, 0, 'q']):
            choice = raw_input("? ")
            try:
                choice = int(choice)
            except:
                pass
        return choice
