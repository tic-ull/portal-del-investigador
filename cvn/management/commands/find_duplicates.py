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
    IRRELEVANT_FIELDS = ['updated_at',
                         'id',
                         'usuario',
                         'created_at',
                         ]
                         
    # constructor
    def __init__(self):
        super(Command, self).__init__()
        
        
    def handle(self, *args, **options):

        # all
        #registros = self.TABLE.objects.filter(pk__lte=150)
        #registros = self.TABLE.objects.all()
        # vigentes en 2012
        registros = self.TABLE.objects.filter( Q(fecha_de_inicio__lte=datetime.date(2012,12,31)) & Q(fecha_de_fin__gt=datetime.date(2012,1,1)))
        
        print "Total de registros en estudio = ", len(registros)
        duplicates = []
        checked = [] # almacena los índices que no requieren comprobación porque ya han sido detectados
        LIMIT = 0.75
        
        ############################
        # ENCONTRAR LOS DUPLICADOS #
        ############################
        
        registros =  [p for p in registros]
        for idx1, pry1  in enumerate(registros[:-1]):
            found = False
            if idx1 not in checked:
                for idx2, pry2 in enumerate(registros[idx1 + 1:], start=idx1 + 1):
                    if idx1 != idx2:
                        pry1_name = pry1.__getattribute__(self.NAME_FIELD)
                        pry2_name = pry2.__getattribute__(self.NAME_FIELD)
                        if pry1_name and pry2_name:
                            percentage, time = string_utils.stringcmp.do_stringcmp("qgram3avrg", 
                                                                pry1_name.lower(),
                                                                pry2_name.lower())
                            if percentage > LIMIT:
                                checked.append(idx2);
                                if not found:
                                    duplicates.append([pry1])
                                    print "===================================================================="
                                    print pry1.id,  pry1_name, "<IS SIMILAR TO>"
                                duplicates[-1].append(pry2)
                                print pry2.id,  pry2_name, percentage
                                found = True;
        
        print "\nTotal duplicates: ", len(duplicates)
        pp = pprint.PrettyPrinter(indent=1,width=60)
        #pprint.pprint(duplicates)
        
        ###############################
        # PREPARAR EL REGISTRO MASTER #
        ###############################
        
        # Se prepara un registro máster que reemplazará al de los duplicados
        # Para cada campo del modelo hacer
            # Si es denominación o algo similar usar los algoritmos de criterio
            # Si es otro campo usar la funcion de votacion.
        
        master = {}

        for group in duplicates:
            fields = {}
            for f in self.TABLE._meta.get_all_field_names():
                if f not in self.IRRELEVANT_FIELDS:
                    fields[f] = [reg.__getattribute__(f) for reg in group]
            master[tuple(group)] = fields   
        
        for key, value in master.items():
            print "==========================================="
            print key
            print "DIFERING FIELDS: ", voting_helpers.difering_fields(key[0], key[1], self.IRRELEVANT_FIELDS)
            for key2, value2 in value.items():
                if any(value2):  # only prints list where at least one element is not None
                    print " ", key2
                    for v in value2:
                        print "  ", v
    
        
        
