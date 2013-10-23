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
        registros = registros[:200]
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
        #~ pp = pprint.PrettyPrinter(indent=1,width=60)
        #~ pprint.pprint(duplicates)
        
        # RECORRER LOS PARES DUPLICADOS QUE SOLO DIFIEREN EN LA DENOMINACION
        
        for pair in sorted(duplicates, key=duplicates.get, reverse=True):
            #print pair, 'similar ', duplicates[pair]
        
            pry1 = pair[0]
            pry2 = pair[1]
            dummy, difering_length, dummy = voting_helpers.difering_fields(pry1, 
                                                                           pry2, 
                                                                           self.DONT_CHECK_FIELDS + [self.NAME_FIELD])
            
            if difering_length == 0:
                
                print "===========================================================\n"    
                master = self.TABLE()
                for f in self.TABLE._meta.get_all_field_names():
                    if f in self.TIMESTAMP_FIELDS:
                        master.f = datetime.datetime.now()
                    else: 
                        if f not in self.DONT_SET_FIELDS + [self.NAME_FIELD]:
                            f1 = pry1.__getattribute__(f)
                            f2 = pry2.__getattribute__(f)
                            master_f = f1 if f1 else f2
                            if f1 and f2: # si existen los dos no podemos decidir
                                master_f = f1 if f1 == f2 else None
                            if any([f1, f2]) and f1 != f2:
                                 print f
                                 print pry1.id, "  ", f1
                                 print pry2.id, "  ", f2
                                 print "MASTER:", master_f, "\n"
                f == self.NAME_FIELD
                f1 = pry1.__getattribute__(f)
                f2 = pry2.__getattribute__(f)
                print f
                print pry1.id, "  ", f1
                print pry2.id, "  ", f2
                print "MASTER:", master_f, "\n"
                
