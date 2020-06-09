#!/usr/bin/python3

Str = 'this is string example....wow!!!'
suffix = '!!'
print (Str.endswith(suffix))
print (Str.endswith(suffix,len(Str)-3,len(Str)-1))
print (Str.startswith('th'))

list = ['Hello','World','Worldzinho']
if 'Worldzinho' in list: 
    print(list)

print('wow' in Str) #Procura wow na String e retorna True ou False

import re

result = re.search(r'wow', Str) #Padrao a procurar, String
if result:
    print("found {}".format(result.group(0))) #result.group(n) com n sendo a posicao da str procurada, ex: eu sou, group(0)==eu

#“So far re hasn’t given you anything you couldn’t get using the in operator. However, what if you are looking for a person in a text, but you can’t remember if the name is Bobbi or Robby?

name = 'Cobbe'
text = "Hello, I am a created person for Joao Pedro use to test the re.search function and my name is {}".format(name)

result = re.search(r'[R,B]obb[i,y]',text) # o r' é porque se trata de uma regular expression
if result:
    print("found {}".format(result.group(0)))

result = re.search(r'[A-Za-z]obb[a-z]',text) # procura testando todas as letras entre a e z, sendo as primeiras maiusculas ou minusculas
if result:
    print("found {}".format(result.group(0)))

#“These are premade character sets. Some commonly used ones are \w, which is equivalent to [a-zA-Z0-9_] and \d, which is equivalent to [0-9].”

email_list = "marian@joao.com,jonathan_jacobo@helloworld.com"

result_unico = re.search(r'\w+\@\w+\.\w+', email_list) #O "+" depois do ultimo 'w' é para indicar que tem mais de um carctere, o re search procura em coisas separadas por virgula ou espaco
if result_unico:
    print("found {}".format(result_unico.group(0)))

matched = re.findall(r'\w+\@\w+\.\w+', email_list)
print(matched) #retorna um array com todos os emails achados

matched = re.finditer(r'\w+\@\w+\.\w+', email_list)
print(matched)
print(next(matched).group(0))
print(next(matched).group(0))

print(re.sub("\d","#","The password is 1234")) #Substitui qualquer numero(\d) na String por "#"
print(re.sub("\w+\@\w+\.\w+", "e-mail address", "Por favor entre em contato comigo através de contato@nginx.com"))

#“All of the examples so far have called methods on the re module directly. This is adequate for many cases, but if the same match is going to happen many times, performance gains can be had by compiling the regular expression into an object.”

email_regex = re.compile(r'\w+\@\w+\.\w+')
print(email_regex.search(email_list))
print(email_regex.findall(email_list))

print(re.sub(email_regex, "e-mail address", "Por favor entre em contato comigo através de contato@nginx.com"))

