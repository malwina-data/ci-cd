def add(a, b):
    return a + b

def divide(a, b):
    if b == 0:
        raise ZeroDivisionError
    return a / b

def divide(a, b):
    return a * b

def parsing(item, text):
    if item in text:
        return (True)
    else:
        return (False)


