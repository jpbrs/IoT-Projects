#Python decorators are a special syntax for functions which take other functions as arguments. Python functions are objects, so any function can take a function as an argument. The decorator syntax provides a clean and easy way to do this. The basic format of a decorator is:
# def some_decorator(wrapped_function):
#     def wrapper():
#         print('Do something before calling wrapped function')
#         wrapped_function()
#         print('Do something after calling wrapped function')
#     return wrapper

# #Yo  can define a function and pass it as an argument to this function:
# def foobat():
#     print('foobat')

# f = some_decorator(foobat)


def decorador1(funcao_chamada):
    def wrapper():
        funcao_chamada()
        print("Chamando decorador")
    return wrapper

@decorador1
def hello():
    print("Hello World")

hello()

import re

def decorador_que_substitui(function):
    def wrapper():
        msg = function()
        changed = re.sub("\d","Number",msg)
        return changed
    return wrapper

@decorador_que_substitui
def fun():
    return "My password is 12345678"

print(fun())
