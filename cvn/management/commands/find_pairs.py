# -*- encoding: utf8 -*-
import datetime
import pprint
import copy
from time import strftime
import logging

from django.core.management.base import BaseCommand
from django.db.models import Q
from cvn.models import Proyecto

import string_utils.stringcmp
import voting_helpers

def log_and_print(message):
    print message
    logging.info(message)

class Command(BaseCommand):
    help = u'Encuentra registros sospechosos de estar duplicados'
    TABLE = Proyecto
    
    # cambiar a mano por ahora
    NAME_FIELD = "denominacion_del_proyecto"
    
    TIMESTAMP_FIELDS = ['updated_at',
                         'created_at',
                       ]
                         
    DONT_SET_FIELDS = ['id',
                       'usuario',
                       ]                 
                                                
    DONT_CHECK_FIELDS = TIMESTAMP_FIELDS + DONT_SET_FIELDS                     
    
    # mínima similitud para considerar dos registros como duplicados
    LIMIT = 0.75

                         
    # constructor
    def __init__(self):
        super(Command, self).__init__()
        log_filename = 'dup_pairs_' + datetime.datetime.now().strftime('%Y_%m_%d_%H_%M.log')
        logging.basicConfig(filename=log_filename, 
                            level=logging.INFO,
                            format='%(asctime)s: %(message)s', 
                            datefmt='%d-%m-%Y %H:%M')

        
    def handle(self, *args, **options):
        log_and_print("Buscando duplicados en {0}".format(self.TABLE))
        
        # all
        #registros = self.TABLE.objects.filter(pk__lte=150)
        #registros = self.TABLE.objects.all()
        # vigentes en 2012
        registros = self.TABLE.objects.filter( Q(fecha_de_inicio__lte=datetime.date(2012,12,31)) & Q(fecha_de_fin__gt=datetime.date(2012,1,1)))
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
        
        registros =  [p for p in registros]
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
   
        # RECORRER LOS PARES DUPLICADOS QUE SOLO DIFIEREN EN LA DENOMINACION
        
        pairs_solved = {}
        
        #for pair in sorted(duplicates, key=duplicates.get, reverse=True):
        sorted_pairs = sorted(duplicates, key=duplicates.get, reverse=False)
        
        # DEBUG ONLY. COMMENT AFTERWARDS
        count = 0
        for pair in sorted_pairs:
            #print pair, 'similar ', duplicates[pair]
            
            if count == 4:
                break
                
            pry1 = pair[0]
            pry2 = pair[1]
            dummy, difering_length, dummy = voting_helpers.difering_fields(pry1, 
                                                                           pry2, 
                                                                           self.DONT_CHECK_FIELDS + [self.NAME_FIELD])
            
            
            # change this to evaluate pairs that differ in more than one field
            if difering_length == 0:
                count +=1
                master = self.TABLE()
                # todo a bit of fixing this 
                model_fields = set(self.TABLE._meta.get_all_field_names()) - set([self.NAME_FIELD])
                model_fields = list(model_fields) + [self.NAME_FIELD]
                
                repeat = True
                while repeat:
                    log_and_print("===========================================================")    
                    log_and_print(" ID1 = {0} comparado con ID2 = {1} ({2:2.2f}%)".format(pry1.id, pry2.id, duplicates[pair]*100))    
                    log_and_print("===========================================================")    
                
                    for idx, f in enumerate(model_fields):
                        if f not in self.DONT_SET_FIELDS + self.TIMESTAMP_FIELDS:
                            f1 = pry1.__getattribute__(f)
                            f2 = pry2.__getattribute__(f)
                            master_f = f1 if f1 else f2
                            if f1 and f2: # si existen los dos no podemos decidir
                                master_f = f1 if f1 == f2 else None
                            if any([f1, f2]) and f1 != f2:
                                log_and_print(f)
                                print "--------------------------------"
                                log_and_print(u"{0:5d}: {1}".format(pry1.id, f1))
                                log_and_print(u"{0:5d}: {1}".format(pry2.id, f2))
                                print "NEW", master_f, "\n"
                                print "--------------------------------"
                                choice = self.choice(pry1, pry2)
                                if choice == -1 or choice == 0:
                                    break
                        
                                if choice == "":
                                    attr = master_f
                                else:
                                    attr = f1 if choice == pry1.id else f2
                                master.__setattr__(f, attr)
                                log_and_print(u"SET TO: {0}".format(attr))
                                 
                                    
                    if choice == 0:
                        break
                    if choice != -1:
                        repeat = False
             
                master.save()
                #pp = pprint.PrettyPrinter(indent=1,width=60)
                #pprint.pprint(master.__dict__)
                
                pairs_solved[(pry1.id, pry2.id)] = master.id
                
                #master.delete()
                
        print pairs_solved
        
        log_and_print("Cambiando los registros afectados en la BBDD")
        for pair, new_id in pairs_solved.iteritems():
            log_and_print("Cambiando usuarios de {0} y {1} a {2}".format(pair[0], pair[1], new_id))
            master_p = self.TABLE.objects.get(pk=master.id)
            for pry_id in pair:
                p = self.TABLE.objects.get(pk=pry_id)
                for u in p.usuario.all():
                    master_p.usuario.add(u)
                    logging.info(u"Proyecto {0} añadir usuario {1}".format(master_p, u))
                    p.usuario.remove(u)
                    logging.info(u"Proyecto {0} borrar usuario {1}".format(p, u))

                p.save()
            master_p.save()
        
        for pair, new_id in pairs_solved.iteritems():
            print "Cambiando usarios de {0} a {1} y {2}".format(new_id, pair[0], pair[1])
            master_p = self.TABLE.objects.get(pk=master.id)
            for pry_id in pair:
                p = self.TABLE.objects.get(pk=pry_id)
                for u in p.usuario.all():
                    p.usuario.add(u)
                    logging.info(u"Proyecto {0} añadir usuario {1}".format(p, u))
                    master_p.usuario.remove(u)
                    logging.info(u"Proyecto {0} borrar usuario {1}".format(master_p, u))

                p.save()
            master_p.save()
        
        
                
    def choice(self, pry1, pry2):
        print 'Return=NEW     %s=ID1      %s=ID2     0=Ignorar pareja     -1=Reniciar pareja' % (pry1.id, pry2.id),
        choice = None
        while choice != "" and choice != pry1.id and choice != pry2.id and choice != -1 and choice != 0:
            choice = raw_input("? ")
            try:
                choice = int(choice)
            except: 
                pass
        return choice
        


