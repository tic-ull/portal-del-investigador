#!/usr/bin/python
# encoding: utf-8

PROJECT_CODE_BEGIN = "([A-Z]{2,3}[-/]?[1-2]\d{3}[-/]?(?:\d+)?\
                    (?:[-/]?[A-Z]?\d{1,2}[-/]?\d{1,2})?)"


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


def capitalize(name):
    return name[0].upper() + name[1:]


def delete_repeated_spaces(name):
    return " ".join(name.split())


def capitalize_phrases(name):
    # please clean repeated spaces first
    return ". ".join([capitalize(phrase) for phrase in name.split(". ")])

# testing

if __name__ == '__main__':
    assert (is_all_caps("PERRO"))
    assert (not is_all_caps("Perro"))
    assert (not is_all_caps("perro"))

    assert (clean_ending_period("Title.") == "Title")
    assert (clean_ending_period("Title") == "Title")

    assert (capitalize("this title is good") == "This title is good")
    assert (capitalize("This title is good") == "This title is good")

    assert (delete_repeated_spaces("\t This  title is  wrong")
            == "This title is wrong")

    assert (capitalize_phrases("this title was converted. it lost the caps")
            == "This title was converted. It lost the caps")

    assert (is_cap_words("This Title Was Titled"))

    assert (delete_quotes('This is "wrong", boy') == 'This is wrong, boy')
