# -*- encoding: utf8 -*-
import datetime
import logging
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
from cvn.models import Usuario, Proyecto, Publicacion, Congreso, Convenio
from string_utils.stringcmp import do_stringcmp


def difering_fields(obj1, obj2, EXCLUDE_FIELDS=[]):
    # return:
    #  - how many of them are different
    # fields where one or two of the values is None,
    # are not counted as different
    # pass a EXCLUDE_FIELDS list with the fields you want
    # to ignore in the comparison
    assert (type(obj1) == type(obj2),
            "The types of the objects are not the same, dude")
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
    logging.info(message)


class Command(BaseCommand):
    help = u'Encuentra registros sospechosos de estar duplicados'
    option_list = BaseCommand.option_list + (
        make_option(
            "-u",
            "--user",
            dest="usuario",
            help="specify user for duplicate control. Use 'all'.",
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
    )

    TABLES = {'Proyecto': Proyecto,
              'Publicacion': Publicacion,
              'Congreso': Congreso,
              'Convenio': Convenio}
    NAME_FIELDS = {'Proyecto': 'denominacion_del_proyecto',
                   'Publicacion': 'titulo',
                   'Congreso': 'titulo',
                   'Convenio': 'denominacion_del_proyecto'}

    TIMESTAMP_FIELDS = ['updated_at', 'created_at', ]

    DONT_SET_FIELDS = ['id', 'usuario', ]

    DONT_CHECK_FIELDS = TIMESTAMP_FIELDS + DONT_SET_FIELDS

    # mínima similitud para considerar dos registros como duplicados
    LIMIT = 0.75

    DIFFERING_PAIRS = 0  # Default value. No contamos la denominación.

    YEAR = 2012

    # constructor
    def __init__(self):
        super(Command, self).__init__()
        log_filename = 'logs/dup_pairs_' \
            + datetime.datetime.now().strftime('%Y_%m_%d@%H_%M.log')
        logging.basicConfig(filename=log_filename,
                            level=logging.INFO,
                            format='%(asctime)s: %(message)s',
                            datefmt='%d-%m-%Y %H:%M')

    def handle(self, *args, **options):

        if options['usuario'] is None:
            raise CommandError("Option `--user=...` must be specified.")
        else:
            usuario = options['usuario']

        if options['table'] is None:
            raise CommandError("Option `--table=...` must be specified.")
        else:
            if options['table'] in self.TABLES:
                TABLE = self.TABLES[options['table']]
                NAME_FIELD = self.NAME_FIELDS[options['table']]
            else:
                raise CommandError("\"{0}\" is not a table. Use Proyecto, \
                Convenio, Publicacion or Congreso ".format(options['table']))

        if options['differing_pairs'] is None:
            raise CommandError("Option `--diff=0, 1...` must be specified.")
        else:
            try:
                self.DIFFERING_PAIRS = int(options['differing_pairs'])
            except:
                raise CommandError("Option `--diff needs an integer 0,1,...")

        log_print("Buscando duplicados en el modelo \
            {0}".format(TABLE.__name__))

        if TABLE == Proyecto:
            # --------------------------- PROYECTOS ---------------------- #
            # PROYECTOS vigentes en 2012
            registros = TABLE.objects.filter(
                Q(fecha_de_inicio__lte=datetime.date(self.YEAR, 12, 31)) &
                Q(fecha_de_fin__gt=datetime.date(self.YEAR, 1, 1)))
            # excluye los registros ya detectados previamente
            # y que están huérfanos de usuario
            registros = registros.exclude(usuario=None)
            # ------------------------------------------------------------ #

        elif TABLE == Publicacion:
            # ---------------------- PUBLICACIONES ----------------------- #
            # PUBLICACIONES en 2012
            registros = TABLE.objects.filter(fecha__year=self.YEAR)
            # excluye los registros ya detectados previamente
            # y que están huérfanos de usuario
            registros = registros.exclude(usuario=None)
            # ------------------------------------------------------------ #

        elif TABLE == Congreso:
            # --------------------------- CONGRESOS ---------------------- #
            # Asistencia a congresos en 2012
            registros = TABLE.objects.filter(
                Q(fecha_realizacion__lte=datetime.date(self.YEAR, 12, 31)) &
                Q(fecha_finalizacion__gt=datetime.date(self.YEAR, 1, 1)))
            # excluye los registros ya detectados previamente
            # y que están huérfanos de usuario
            registros = registros.exclude(usuario=None)
            # ----------------------------------------------------------- #

        elif TABLE == Convenio:
            # ------------------------ CONVENIOS ------------------------- #
            # Convenios vigentes en 2012
            registros_raw = TABLE.objects.raw('SELECT * FROM cvn_convenio WHERE (YEAR(fecha_de_inicio) = ' + 'self.YEAR' + ' OR (duracion_anyos < 100 AND YEAR(INTERVAL (duracion_anyos * 365 + duracion_meses * 12 + duracion_dias) DAY + fecha_de_inicio) >= ' + 'self.YEAR' + ') OR /* caso de dato erróneo */ (duracion_anyos >= 100 AND YEAR(INTERVAL (duracion_meses * 12 + duracion_dias) DAY + fecha_de_inicio) >= ' + 'self.YEAR' + ') OR /* caso de dato erróneo */ (duracion_anyos >= ' + 'self.YEAR' + '))')
            # excluye los registros ya detectados previamente
            # y que están huérfanos de usuario
            registros = []
            for r in registros_raw:
                list_usuarios = r.usuario.all()
                if list_usuarios is not None and len(list_usuarios) > 0:
                    registros.append(r)
            # ------------------------------------------------------------ #

        if usuario != "all":
            # obtenemos el usuario cuyo documento es usuario
            try:
                usuario = Usuario.objects.get(documento=usuario)
            except:
                raise CommandError('El usuario con documento "{0}" no existe'
                                   .format(usuario))

            if TABLE in [Congreso, Publicacion, Proyecto]:
                registros = registros.filter(usuario=usuario)
            else:  # TABLE is Convenio
                new_registros = []
                for r in registros:
                    if usuario in r.usuario.all():
                        new_registros.add(r)
                registros = new_registros

        log_print("Total de registros en estudio = {0}".format(len(registros)))
        duplicates = {}

        ##################################
        # ENCONTRAR LOS PARES DUPLICADOS #
        ##################################

        registros = [p for p in registros]

        for idx1, pry1 in enumerate(registros[:-1]):
            print "Finding pairs for index: ", idx1
            for idx2, pry2 in enumerate(registros[idx1 + 1:], start=idx1 + 1):
                pry1_name = pry1.__getattribute__(NAME_FIELD)
                pry2_name = pry2.__getattribute__(NAME_FIELD)
                if pry1_name and pry2_name:
                    # comparisons made in lower case
                    percentage, time = do_stringcmp("qgram3avrg",
                                                    pry1_name.lower(),
                                                    pry2_name.lower())
                    if percentage > self.LIMIT:
                        pair = tuple([pry1, pry2])
                        duplicates[pair] = percentage

        log_print("Total duplicates = {0} de {1} "
                  .format(len(duplicates), len(registros)))

        # RECORRER LOS PARES DUPLICADOS
        pairs_solved = {}
        sorted_pairs = sorted(duplicates, key=duplicates.get, reverse=True)

        choice = ""
        count = 0
        for pair in sorted_pairs:
            if choice == 'q':
                log_print("User aborted main loop...")
                break
            pry1 = pair[0]
            pry2 = pair[1]
            difering_length = difering_fields(
                pry1, pry2, self.DONT_CHECK_FIELDS + [NAME_FIELD])

            save = True
            if difering_length == self.DIFFERING_PAIRS:
                master = TABLE()
                # todo a bit of fixing this
                model_fields = (set(TABLE._meta.get_all_field_names())
                                - set([NAME_FIELD]))
                model_fields = list(model_fields) + [NAME_FIELD]
                FIELD_WIDTH = 28
                COLWIDTH = 50

                repeat = True
                while repeat:
                    log_print("=============================================")
                    log_print(" ID1 = {0} comparado con ID2 = {1} ({2:2.2f}%)"
                              .format(pry1.id, pry2.id, duplicates[pair]*100))
                    log_print("=============================================")

                    # overview of the two registers
                    log_print("Field".ljust(FIELD_WIDTH)
                              + "ID1".ljust(COLWIDTH)
                              + "ID2".ljust(COLWIDTH))
                    log_print("-" * (FIELD_WIDTH + 2 * COLWIDTH))
                    for f in model_fields:
                        if f not in (self.DONT_SET_FIELDS +
                                     self.TIMESTAMP_FIELDS):
                            f1 = pry1.__getattribute__(f)
                            f1 = "" if f1 is None else f1
                            f2 = pry2.__getattribute__(f)
                            f2 = "" if f2 is None else f2
                            if any([f1, f2]):
                                log_print(unicode(f)[:FIELD_WIDTH-1]
                                          .ljust(FIELD_WIDTH)
                                          + unicode(f1)[:COLWIDTH-1]
                                          .ljust(COLWIDTH)
                                          + unicode(f2)[:COLWIDTH-1]
                                          .ljust(COLWIDTH))
                    log_print("-" * (FIELD_WIDTH + 2 * COLWIDTH))

                    for f in model_fields:
                        if f not in (self.DONT_SET_FIELDS +
                                     self.TIMESTAMP_FIELDS):
                            f1 = pry1.__getattribute__(f)
                            f2 = pry2.__getattribute__(f)
                            master_f = f1 if f1 else f2
                            if f1 and f2:
                                try:
                                    master_f = f1 if len(f1) >= len(f2) else f2
                                except:
                                    master_f = f1
                            # A AND B, A == B
                            # si existen los dos no podemos decidir
                            if f1 and f2 and f1 == f2:
                                attr = f1
                                master.__setattr__(f, attr)
                            # A OR B, A != B
                            if any([f1, f2]) and f1 != f2:
                                log_print(f)
                                print "--------------------------------"
                                log_print(u"{0:5d}: {1}".format(pry1.id, f1))
                                log_print(u"{0:5d}: {1}".format(pry2.id, f2))
                                print "  NEW:", master_f, "\n"
                                print "--------------------------------"
                                choice = self.choice(pry1, pry2)
                                if choice in [-1, 0, 'q']:
                                    break

                                if choice == "":
                                    attr = master_f
                                else:
                                    if choice == "j":
                                        attr = f1 + "; " + f2
                                    else:
                                        attr = f1 if choice == pry1.id else f2
                                master.__setattr__(f, attr)
                                log_print(u"SET TO: {0}".format(attr))
                                log_print(u"----------")

                            # NOT A AND NOT B

                    if choice in [0, 'q']:
                        save = False
                        break
                    if choice != -1:
                        repeat = False

                if save:
                    count += 1
                    master.save()
                    pairs_solved[(pry1.id, pry2.id)] = master.id

        print pairs_solved
        log_print("========================================")
        log_print(u"Número de campos diferentes " +
                  u"(contando la denominación): {0}"
                  .format(self.DIFFERING_PAIRS + 1))
        log_print("========================================")
        log_print("Parejas cambiadas = {0}".format(count))
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
                    logging.info(u"Proyecto {0} [ID={1}] " +
                                 u"añadir usuario {2} [ID={3}]"
                                 .format(master_p, master_p.id, u, u.id))
                    p.usuario.remove(u)
                    logging.info(u"Proyecto {0} [ID={1}] " +
                                 u"borrar usuario {2} [ID={3}]"
                                 .format(p, p.id, u, u.id))

                p.save()
            master_p.save()

    def choice(self, pry1, pry2):
        print 'Return=NEW   %s=ID1   %s=ID2   0=Ignorar pareja  -1=Reniciar'\
            + ' j=join_fields  q=save_and_abort' % (pry1.id, pry2.id),
        choice = None
        while (choice != "" and choice != pry1.id and choice != pry2.id and
               choice != -1 and choice != 0 and choice != 'j' and
               choice != 'q'):
            choice = raw_input("? ")
            try:
                choice = int(choice)
            except:
                pass
        return choice

    def test():
        print "TEST"
