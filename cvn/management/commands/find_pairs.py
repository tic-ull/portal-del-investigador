# -*- encoding: utf8 -*-
import datetime
import pprint

from django.core.management.base import BaseCommand
from django.db.models import Q
from cvn.models import Proyecto

import string_utils.stringcmp
import voting_helpers

class Command(BaseCommand):
    help = u'Encuentra registros sospechosos de estar duplicados'
    TABLE = Proyecto
    NAME_FIELD = "denominacion_del_proyecto"
    TIMESTAMP_FIELDS = ['updated_at',
                         'created_at',
                       ]
                         
    DONT_SET_FIELDS = ['id',
                       'usuario',
                       ]                 
                                                
    DONT_CHECK_FIELDS = TIMESTAMP_FIELDS + DONT_SET_FIELDS                     
                         
    # constructor
    def __init__(self):
        super(Command, self).__init__()
        
        
    def handle(self, *args, **options):

        # all
        #registros = self.TABLE.objects.filter(pk__lte=150)
        #registros = self.TABLE.objects.all()
        # vigentes en 2012
        registros = self.TABLE.objects.filter( Q(fecha_de_inicio__lte=datetime.date(2012,12,31)) & Q(fecha_de_fin__gt=datetime.date(2012,1,1)))
        registros = registros[:50]
        print "Total de registros en estudio = ", len(registros)
        duplicates = {}
        checked = [] # almacena los índices que no requieren comprobación porque ya han sido detectados
        LIMIT = 0.75
        
        ##################################
        # ENCONTRAR LOS PARES DUPLICADOS #
        ##################################
        
        registros =  [p for p in registros]
        for idx1, pry1  in enumerate(registros[:-1]):
            print "\nFinding pairs for index: ", idx1, 
            for idx2, pry2 in enumerate(registros[idx1 + 1:], start=idx1 + 1):
                pry1_name = pry1.__getattribute__(self.NAME_FIELD)
                pry2_name = pry2.__getattribute__(self.NAME_FIELD)
                if pry1_name and pry2_name:
                    # comparisons made in lower case
                    percentage, time = string_utils.stringcmp.do_stringcmp("qgram3avrg", 
                                                                            pry1_name.lower(),
                                                                            pry2_name.lower())
                    if percentage > LIMIT:
                        pair = tuple([pry1, pry2])
                        duplicates[pair] = percentage

        print "\nTotal duplicates: ", len(duplicates)
   
        # RECORRER LOS PARES DUPLICADOS QUE SOLO DIFIEREN EN LA DENOMINACION
        
        pairs_solved = {}
        
        for pair in sorted(duplicates, key=duplicates.get, reverse=True):
            #print pair, 'similar ', duplicates[pair]
        
            pry1 = pair[0]
            pry2 = pair[1]
            dummy, difering_length, dummy = voting_helpers.difering_fields(pry1, 
                                                                           pry2, 
                                                                           self.DONT_CHECK_FIELDS + [self.NAME_FIELD])
            
            if difering_length == 0:
                master = self.TABLE()
                # todo a bit of fixing this 
                model_fields = set(self.TABLE._meta.get_all_field_names()) - set([self.NAME_FIELD])
                model_fields = list(model_fields) + [self.NAME_FIELD]
                
                repeat = True
                while repeat:
                    print "\n==========================================================="    
                    print " ID1 = %s comparado con ID2 = %s " % (pry1.id, pry2.id)    
                    print "==========================================================="    
                
                    for idx, f in enumerate(model_fields):
                        if f in self.TIMESTAMP_FIELDS:
                            master.f = datetime.datetime.now()
                        else: 
                            if f not in self.DONT_SET_FIELDS:
                                f1 = pry1.__getattribute__(f)
                                f2 = pry2.__getattribute__(f)
                                master_f = f1 if f1 else f2
                                if f1 and f2: # si existen los dos no podemos decidir
                                    master_f = f1 if f1 == f2 else None
                                if any([f1, f2]) and f1 != f2:
                                    print "\n", idx, "->", f
                                    print pry1.id, f1
                                    print pry2.id, f2
                                    print "NEW", master_f, "\n"
                                    choice = self.choice(pry1, pry2)
                                    if choice == -1 or choice == 0:
                                        break
                                    
                                    if choice == "":
                                        master.f = master_f
                                    else:
                                        master.f = f1 if choice == pry1.id else f2
                                    
                                    print "SET", master.f
                                    
                    if choice == 0:
                        break
                    if choice != -1:
                        repeat = False
                
                #~ pp = pprint.PrettyPrinter(indent=1,width=60)
                print "RESULTING REGISTER:"            
                pprint.pprint(master.__dict__)
                master.save()
                #pprint.pprint(master.__dict__)
                #choice = raw_input("DELETING")
                
                pairs_solved[(pry1.id, pry2.id)] = master.id
                
                master.delete()
                
        print pairs_solved
                
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
        
