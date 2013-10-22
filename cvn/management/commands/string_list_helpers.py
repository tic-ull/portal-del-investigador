#!/usr/bin/python
# encoding: utf-8

def most_voted_safest(lista):
    # devuelve True si la votación es válida y el elemento más votado de una lista.
    # [2, 2, "", None"]  -> True, 2
    # [3, 2, "", ""] -> False, None
    # [1, "", "", None] -> True, 1
    s = set(lista)
    # check for basic empty strings
    if "" in s: s.remove(""); s.add(None)
    if " " in s: s.remove(""); s.add(None)

    if len(s)=0 or len(s) > 2:
        return False, None
    if len(s) = 2:
        s.discard(None) # only one element left
        return True, s.pop()
    if len(s) = 1: 
		return True, s.pop()
    
if __name__ == '__main__':
    print [2, 2, "", None],  most_voted_safest([2, 2, "", None])
    print [3, 2, "", ""],  most_voted_safest([3, 2, "", ""])
    print [2, "", "", ""],  most_voted_safest([2, "", "", ""])
    print [2, 2, 3, 3, " ", ""],  most_voted_safest([2, 2, 3, 3, " ", ""])

