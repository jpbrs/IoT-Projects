import os

print(os.listdir('.')) #ls do diretorio

#os.rename('nome arquivo1','novo nome arquivo1')
#os.chmod('nome do arquivo', permissao)
#os.mkdir('/users/mac/Desktop/novo_diretorio')
#os.makedirs('/users/mac/Desktop/novo_diretorio/novo_dir/um_outro_dir') => Cria os diretorios recursivamente
#os.remove('nome do arquivo')
#os.rmdir('nome do diretorio')
#os.removedirs('nome do diretorio') remove o diretorio e todos que tem dentro(se forem vazios)
#os.getcwd() => Retorna o atual diretorio
#os.path.exists('nome do arquivo') => retorna true se o arquivo existir no diretorio
#os.chdir('/diretorio') => muda de diretorio
#os.getlogin() => retorna o usuario logado

import sys

print(sys.getsizeof(1)) # Retorna o tamanho de uma variavel

array_100 = [x for x in range(100)]
generator_100 = (x for x in range(100))

print(sys.getsizeof(array_100))
print(sys.getsizeof(generator_100))

print(sum(array_100) == sum (generator_100))

print(sys.platform) #Como eu estou usando Mac a plataforma vai ser darwin por conta do Mac OS ser baseado no Darwin OS

if sys.version_info.major < 3:
    print("Voce precisa baixar o python3 pq o 2 ja foi descontinuado") #=> Retorna a versao do python
    sys.exit(1)
elif sys.version_info.minor < 7:
    print("You are not running the latest version of Python")
else:
    print("All is good.")

import subprocess

ls = subprocess.run(['ls','-l'], capture_output=True, universal_newlines=True)#“We set it to capture stdout and stderr with the capture_output parameter. We then access the results using ls.stdout.”
