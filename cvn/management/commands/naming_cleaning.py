#!/usr/bin/python
# encoding: utf-8

PROJECT_CODE_BEGIN = "([A-Z]{2,3}[-/]?[1-2]\d{3}[-/]?(?:\d+)?(?:[-/]?[A-Z]?\d{1,2}[-/]?\d{1,2})?)"

def is_all_caps(name):
    return name == name.upper()

def is_cap_words(name):
    """ todas las palabras con mayúsculas"""
    return name.istitle()

def delete_quotes(name):
    return name.replace('"', '')

def clean_ending_period(name):
    if name[-1] == ".":
        return name[:-1]
    else:
        return name

def cap_first_letter(name):
    return name[0].upper() + name [1:]    

def delete_repeated_spaces(name):
    return  " ".join(name.split())
    
def cap_first_letter_phrases(name):
    # please clean repeated spaces first
    return  ". ".join([cap_first_letter(phrase) for phrase in name.split(". ")])
        
# testing
    
if __name__ == '__main__':
    assert (is_all_caps("PERRO"))
    assert (not is_all_caps("Perro"))
    assert (not is_all_caps("perro"))
    
    assert (clean_ending_period("Title.") == "Title")
    assert (clean_ending_period("Title") == "Title")
    
    assert (cap_first_letter("this title is good") == "This title is good")
    assert (cap_first_letter("This title is good") == "This title is good")
    
    assert (delete_repeated_spaces("\t This  title is  wrong") == "This title is wrong")
    
    assert (cap_first_letter_phrases("this title was converted from upper. it lost the caps") == "This title was converted from upper. It lost the caps")
    
    assert (is_cap_words("This Title Was Titled"))

    assert (delete_quotes('This is "wrong", boy') == 'This is wrong, boy')

