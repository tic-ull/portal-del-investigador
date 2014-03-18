
def isdigit(obj):
    if type(obj) is str and obj.isdigit():
        return True
    else:
        return False

def noneToZero(value):
    return value if not value is None else 0
