# -*- encoding: utf8 -*-
import datetime
import pprint
import copy
from time import strftime
import logging

from django.core.management.base import BaseCommand
from django.db.models import Q
from cvn.models import Proyecto, Publicacion, Congreso, Convenio

from viinvDB.models import GrupoinvestInvestigador

# utilidades de comparación de cadenas
import string_utils.stringcmp

# utilidades de diferencias entre registros
import voting_helpers

# utilidades de limpieza de títulos, denominación, etc
import naming_cleaning

def log_and_print(message):
    print message
    logging.info(message)

class Command(BaseCommand):
    help = u'Encuentra registros sospechosos de estar duplicados'
    
    ########### ZONA MANUAL ##########################
    # cambiar a mano por ahora.
    
    # TABLE = Proyecto
    # TABLE = Publicacion
    # TABLE = Congreso
    TABLE = Convenio
    
    #NAME_FIELD = "denominacion_del_proyecto"
    #NAME_FIELD = "titulo"
    #NAME_FIELD = "titulo"
    NAME_FIELD = "denominacion_del_proyecto" # es así también para convenios
    
    ########### FIN DE ZONA MANUAL ###################
    
    TIMESTAMP_FIELDS = ['updated_at',
                         'created_at',
                       ]
                         
    DONT_SET_FIELDS = ['id',
                       'usuario',
                       ]                 
                                                
    DONT_CHECK_FIELDS = TIMESTAMP_FIELDS + DONT_SET_FIELDS                     
    
    # mínima similitud para considerar dos registros como duplicados
    LIMIT = 0.75
    
    DIFFERING_PAIRS = 5 # no contamos la denominación.
                     
    # constructor
    def __init__(self):
        super(Command, self).__init__()
        log_filename = 'logs/dup_pairs_' + datetime.datetime.now().strftime('%Y_%m_%d@%H_%M.log')
        logging.basicConfig(filename=log_filename, 
                            level=logging.INFO,
                            format='%(asctime)s: %(message)s', 
                            datefmt='%d-%m-%Y %H:%M')

        
    def handle(self, *args, **options):
        log_and_print("Buscando duplicados en el modelo {0}".format(self.TABLE.__name__))
        
        # all
        #registros = self.TABLE.objects.filter(pk__lte=150)
        #registros = self.TABLE.objects.all()
        
        # ----------------------------- PROYECTOS ------------------------- #
        # PROYECTOS vigentes en 2012
        # registros = self.TABLE.objects.filter( Q(fecha_de_inicio__lte=datetime.date(2012,12,31)) & Q(fecha_de_fin__gt=datetime.date(2012,1,1)))
        # excluye los registros ya detectados previamente y que están huérfanos de usuario
        # registros = registros.exclude(usuario=None)
        # ----------------------------------------------------------------- # 
        

        # --------------------------- PUBLICACIONES ----------------------- #
        # PUBLICACIONES en 2012
        # registros = self.TABLE.objects.filter(fecha__year=2012)
        # excluye los registros ya detectados previamente y que están huérfanos de usuario
        # registros = registros.exclude(usuario=None)
        # ----------------------------------------------------------------- # 
        
        # ----------------------------- CONGRESOS ------------------------- #
        # Asistencia a congresos en 2012
        # registros = self.TABLE.objects.filter( Q(fecha_realizacion__lte=datetime.date(2012,12,31)) & Q(fecha_finalizacion__gt=datetime.date(2012,1,1)))
        # excluye los registros ya detectados previamente y que están huérfanos de usuario
        # registros = registros.exclude(usuario=None)
        # ----------------------------------------------------------------- # 
        

        # ----------------------------- CONVENIOS ------------------------- #
        # Convenios vigentes en 2012
        registros_raw = self.TABLE.objects.raw('SELECT * FROM cvn_convenio WHERE (YEAR(fecha_de_inicio) = 2012 OR (duracion_anyos < 100 AND YEAR(INTERVAL (duracion_anyos * 365 + duracion_meses * 12 + duracion_dias) DAY + fecha_de_inicio) >= 2012) OR /* caso de dato erróneo */ (duracion_anyos >= 100 AND YEAR(INTERVAL (duracion_meses * 12 + duracion_dias) DAY + fecha_de_inicio) >= 2012) OR /* caso de dato erróneo */ (duracion_anyos >= 2012))')
        # excluye los registros ya detectados previamente y que están huérfanos de usuario
        registros = []
        for r in registros_raw:
            list_usuarios = r.usuario.all()
            if list_usuarios is not None and len(list_usuarios) > 0:
                registros.append(r)
        # ----------------------------------------------------------------- # 

        if args:
            try:
                registros = registros[:int(args[0])]
            except:
                print "se esperaba el límite de registros como entero, usando todos los registros"
                pass
        log_and_print("Total de registros en estudio = {0}".format(len(registros)))
        duplicates = {}
        
        ##################################
        # ENCONTRAR LOS PARES DUPLICADOS #
        ##################################
        
        
        # Basic cleaning
        registros =  [p for p in registros]
        #for idx, registro in enumerate(registros):
            #print "Cleaning register: ", idx
            #name_field_content = registro.__getattribute__(self.NAME_FIELD)
            #if name_field_content:
                #name_field_content = naming_cleaning.clean_ending_period(name_field_content)
                ## add here more "intelligent" cleaning if desired
                #registro.__setattr__(self.NAME_FIELD, name_field_content)
                #registro.save()
 
        for idx1, pry1  in enumerate(registros[:-1]):
            print "Finding pairs for index: ", idx1 
            for idx2, pry2 in enumerate(registros[idx1 + 1:], start=idx1 + 1):
                pry1_name = pry1.__getattribute__(self.NAME_FIELD)
                pry2_name = pry2.__getattribute__(self.NAME_FIELD)
                if pry1_name and pry2_name:
                    # comparisons made in lower case
                    percentage, time = string_utils.stringcmp.do_stringcmp("qgram3avrg", 
                                                                            pry1_name.lower(),
                                                                            pry2_name.lower())
                    if percentage > self.LIMIT:
                        pair = tuple([pry1, pry2])
                        duplicates[pair] = percentage

        log_and_print("Total duplicates = {0} de {1} ".format(len(duplicates), len(registros)))
   
        # RECORRER LOS PARES DUPLICADOS
        pairs_solved = {}        
        sorted_pairs = sorted(duplicates, key=duplicates.get, reverse=True)
        
        choice = ""
        count = 0
        for pair in sorted_pairs:
            if choice == 'q':
                log_and_print("User aborted main loop...")
                break
            pry1 = pair[0]
            pry2 = pair[1]
            dummy, difering_length, dummy = voting_helpers.difering_fields(pry1, 
                                                                           pry2, 
                                                                           self.DONT_CHECK_FIELDS + [self.NAME_FIELD])
            
            save = True
            if difering_length == self.DIFFERING_PAIRS:
                master = self.TABLE()
                # todo a bit of fixing this 
                model_fields = set(self.TABLE._meta.get_all_field_names()) - set([self.NAME_FIELD])
                model_fields = list(model_fields) + [self.NAME_FIELD]
                FIELD_WIDTH = 28
                COLWIDTH = 50
                
                repeat = True
                while repeat:
                    log_and_print("===========================================================")    
                    log_and_print(" ID1 = {0} comparado con ID2 = {1} ({2:2.2f}%)".format(pry1.id, pry2.id, duplicates[pair]*100))    
                    log_and_print("===========================================================")    
                
                    # overview of the two registers
                    log_and_print("Field".ljust(FIELD_WIDTH) + "ID1".ljust(COLWIDTH) + "ID2".ljust(COLWIDTH))
                    log_and_print("-" * (FIELD_WIDTH + 2 * COLWIDTH))
                    for f in model_fields:
                        if f not in self.DONT_SET_FIELDS + self.TIMESTAMP_FIELDS:
                            f1 = pry1.__getattribute__(f)
                            f1 = "" if f1 is None else f1
                            f2 = pry2.__getattribute__(f)
                            f2 = "" if f2 is None else f2
                            if any([f1, f2]):
                                log_and_print(unicode(f)[:FIELD_WIDTH-1].ljust(FIELD_WIDTH) + 
                                              unicode(f1)[:COLWIDTH-1].ljust(COLWIDTH) + 
                                              unicode(f2)[:COLWIDTH-1].ljust(COLWIDTH))
                    log_and_print("-" * (FIELD_WIDTH + 2 * COLWIDTH))

                    for f in model_fields:
                        if f not in self.DONT_SET_FIELDS + self.TIMESTAMP_FIELDS:
                            f1 = pry1.__getattribute__(f)
                            f2 = pry2.__getattribute__(f)
                            master_f = f1 if f1 else f2
                            if f1 and f2:
                                try:
                                    master_f = f1 if len(f1)>= len(f2) else f2
                                except:
                                    master_f = f1
                            # A AND B, A == B
                            if f1 and f2 and f1 == f2: # si existen los dos no podemos decidir
                                attr = f1
                                master.__setattr__(f, attr)
                            # A OR B, A != B
                            if any([f1, f2]) and f1 != f2:
                                log_and_print(f)
                                print "--------------------------------"
                                log_and_print(u"{0:5d}: {1}".format(pry1.id, f1))
                                log_and_print(u"{0:5d}: {1}".format(pry2.id, f2))
                                print "  NEW:", master_f, "\n"
                                print "--------------------------------"
                                choice = self.choice(pry1, pry2)
                                if choice == -1 or choice == 0 or choice =='q':
                                    break
                        
                                if choice == "":
                                    attr = master_f
                                else:
                                    if choice == "j":
                                        attr = f1 + "; " + f2
                                    else:
                                        attr = f1 if choice == pry1.id else f2
                                master.__setattr__(f, attr)
                                log_and_print(u"SET TO: {0}".format(attr))
                                log_and_print(u"----------")
                            
                            # NOT A AND NOT B
        
                    if choice == 0 or choice =='q':
                        save = False
                        break
                    if choice != -1:
                        repeat = False
             
                if save:
                    count +=1
                    master.save()
                    pairs_solved[(pry1.id, pry2.id)] = master.id
                    
        print pairs_solved
        log_and_print("========================================")
        log_and_print(u"Número de campos diferentes (contando la denominación): {0}".format(self.DIFFERING_PAIRS + 1))
        log_and_print("========================================")
        log_and_print("Parejas cambiadas = {0}".format(count))
        log_and_print("========================================")
        log_and_print("Cambiando los registros afectados en la BBDD")
        for pair, new_id in pairs_solved.iteritems():
            log_and_print(u"----------")
            log_and_print("Cambiando usuarios de {0} y {1} a {2}".format(pair[0], pair[1], new_id))
            master_p = self.TABLE.objects.get(pk=new_id)
            for pry_id in pair:
                p = self.TABLE.objects.get(pk=pry_id)
                for u in p.usuario.all():
                    master_p.usuario.add(u)
                    logging.info(u"Proyecto {0} [ID={1}] añadir usuario {2} [ID={3}]".format(master_p, master_p.id, u, u.id))
                    p.usuario.remove(u)
                    logging.info(u"Proyecto {0} [ID={1}] borrar usuario {2} [ID={3}]".format(p, p.id, u, u.id))

                p.save()
            master_p.save()
        
        #~ for pair, new_id in pairs_solved.iteritems():
            #~ print "Cambiando usarios de {0} a {1} y {2}".format(new_id, pair[0], pair[1])
            #~ master_p = self.TABLE.objects.get(new_id)
            #~ for pry_id in pair:
                #~ p = self.TABLE.objects.get(pk=pry_id)
                #~ for u in p.usuario.all():
                    #~ p.usuario.add(u)
                    #~ logging.info(u"Proyecto {0} añadir usuario {1}".format(p, u))
                    #~ master_p.usuario.remove(u)
                    #~ logging.info(u"Proyecto {0} borrar usuario {1}".format(master_p, u))
        #~ 
                #~ p.save()
            #~ master_p.save()
        #~ 
        
                
    def choice(self, pry1, pry2):
        print 'Return=NEW   %s=ID1   %s=ID2   0=Ignorar pareja  -1=Reniciar  j=join_fields  q=save_and_abort' % (pry1.id, pry2.id),
        choice = None
        while choice != "" and choice != pry1.id and choice != pry2.id and choice != -1 and choice != 0 and choice != 'j'and choice != 'q':
            choice = raw_input("? ")
            try:
                choice = int(choice)
            except: 
                pass
        return choice
        
    def test():
        print "TEST"

