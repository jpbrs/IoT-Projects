import os

open_file = open("book.txt", "r")

text = open_file.readlines()
len(text)
print(text[1])

open_file.close()

# “A handy way of opening files is to use with statements. You do not need to close a file explicitly in this case. Python closes it and releases the file resource at the end of the indented block”
with open("book.txt","r") as open_file:
    for line in open_file:
        print(line)
    # file will close at the end of this statement
print(open_file.closed)

# “You can define environment variables and application runtimes in a file named .envrc; direnv uses it to set these things up when you enter the directory with the file.”
text = """export STAGE=PROD
export TABLE_ID=token-storage-1234"""

with open('.envrc', 'w') as opened_file:
    opened_file.write(text)

print(os.system('cat .envrc'))

# with open('policy.json','r') as opened_file:
#     policy = opened_file.readlines()
#     print(policy) #nao da p manipular visto os \n, formato, etc.

import json
from pprint import pprint

with open('policy.json','r') as opened_file:
    policy = json.load(opened_file) #Carrega o arquivo Json como um Python dictionary
    pprint(policy)

    policy['Statement']['Resource'] = "S3"
    pprint(policy) #indentado  
    print(policy)  #Nao indentado