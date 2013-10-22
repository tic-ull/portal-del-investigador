#!/usr/bin/python
# encoding: utf-8

def most_voted_safest(lista):
    # si la votación es válida devuelve True y el elemento más votado de la lista
    # devuelve False y None si la votación es inválida
    # [2, 2, "", None"]  -> True, 2
    # [3, 2, "", ""] -> False, None
    # [1, "", "", None] -> True, 1
    s = set(lista)
    # check for basic empty strings
    if "" in s: s.remove(""); s.add(None)
    if " " in s: s.remove(""); s.add(None)

    if len(s) == 0 or len(s) > 2:
        return False, None
    if len(s) == 2:
        s.discard(None) # only one element left
        return True, s.pop()
    if len(s) == 1: 
        return True, s.pop()


def difering_fields(obj1, obj2, EXCLUDE_FIELDS = []):
    # return the total number of the objects, how many of them are different, and a list of the difering fields
    # fields where one or two of the values is None, are not counted as different
    # pass a EXCLUDE_FIELDS list with the fields you want to ignore in the comparison
    assert (type(obj1) == type(obj2), "The types of the objects are not the same, dude")
    difering = []
    tipo = type(obj1)
    fields = tipo._meta.get_all_field_names()
    for f in fields:
        if f not in EXCLUDE_FIELDS:
            f1 = obj1.__getattribute__(f)
            f2 = obj2.__getattribute__(f)
            if f1 and f2 and f1 != f2:
                difering.append(f)
    return len(fields), len(difering), difering 


def all_None(lista):
    # return True if all the elements of the list are None
    return not any(lista)
    
if __name__ == '__main__':
    print [2, 2, "", None],  most_voted_safest([2, 2, "", None])
    print [3, 2, "", ""],  most_voted_safest([3, 2, "", ""])
    print [2, "", "", ""],  most_voted_safest([2, "", "", ""])
    print [2, 2, 3, 3, " ", ""],  most_voted_safest([2, 2, 3, 3, " ", ""])

