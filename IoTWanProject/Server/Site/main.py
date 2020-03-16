from flask import Flask, render_template, request, redirect
from flask import session, flash, abort, send_from_directory
import hashlib
from json import JSONEncoder
import jsonpickle
import os


HOST = '0.0.0.0'
PORT = 5000

def get_hash(string:str):
    string_bytes = str.encode(string)
    string_hash = hashlib.md5(string_bytes)
    return string_hash.hexdigest()

def append_in_table(arquivo):
    sitebkp = open('templates/applicationsbkp.html','r')
    contents = sitebkp.readlines()
    site = open('templates/applications.html', 'w')
    contents = "".join(contents)
    site.write(contents)
    site.close()
    sitebkp.close()

    for line in arquivo:
        array_line = line.split(",")
        application = array_line[0]
        appkey = array_line[1]
        device = array_line[2]

        index = 0
        sitebkp = open('templates/applicationsbkp.html', 'r')
        for line in sitebkp:
            index +=1
            if '</tr>' in line:
                break
        sitebkp.close()

        site = open('templates/applications.html', 'r')
        contents = site.readlines()
        site.close()
        contents.insert(index, "\n<tr id=\"{}\">\n<td>{}</td>\n<td>{}</td>\n<td>{}</td>\n</tr>".format(application, application,device, appkey))
        site = open('templates/applications.html','w')
        contents = "".join(contents)
        site.write(contents)
        site.close()


user = open('credentials')
users = {}
for line in user:
    user_array = line.split(",")
    users[user_array[0]] = user_array[1]
user.close()

# FLASK Initializing
app = Flask(__name__)
app.secret_key = 'iotwanproject'

@app.route('/')
def login():
    if session.get('logged'):
        session.pop('logged')
    return render_template('login2.html')

@app.route('/autenticar', methods=['POST', ])
def _call_0():
    user = get_hash(request.form['username'])
    if user in users:
        senha = request.form['password']
        if get_hash(senha) == users[user]:
            session['logged'] = True #aluno # cria uma sessao com o usuario preenchido no login
            return redirect('/applications')
        else:
            flash('Senha Incorreta!')
    else:
        flash('Usuário não encontrado!')
    return redirect('/')

@app.route('/adicionar', methods=['POST', ])
def _call_1():
    application = request.form['application']
    appkey = request.form['appkey']
    device = request.form['device']
    if len(application) == 4 and len(appkey) == 16 and len(device) == 8:
        file = open("applications","a+")
        file.write("{},{},{}\n".format(application,appkey,device))
        file.close()
        comando = "mkdir ../Devices/{}".format(application)
        comando2 = "mkdir ../Devices/{}/{}".format(application,device)
        comando3 = "echo {} > ../Devices/{}/{}/key".format(appkey, application,device)
        comando4 = "echo {} > ../Devices/{}/{}/counter".format(-1, application,device)
        comando5 = "echo {} > ../Devices/{}/{}/nonce".format(-1, application,device)

        os.system(comando)
        os.system(comando2)
        os.system(comando3)
        os.system(comando4)
        os.system(comando5)



        return redirect('/applications')
    else:
        flash('Dados fora do padrão de tamanho')

        return redirect('/applications')
        
        

@app.route('/remover', methods=['POST', ])
def _call_2():
    application = request.form['application']
    temp_string = ""
    file = open('applications',"r")
    for line in file:
        array_line = line.split(",")
        if array_line[0] == application:
            pass
        else:
            temp_string += "{}".format(line)
    file.close()
    file = open('applications',"w")
    file.write(temp_string)
    file.close()
    return redirect('/applications')

@app.route('/applications')
def _call_3():
    aplicacoes = open('applications','r+')
    append_in_table(aplicacoes)

    if session.get("logged"):
        return render_template('applications.html')
    else:
        abort(503)

@app.route('/data', methods=['POST', ])
def _call_4():
    device = request.form['device']
    appUI = request.form['aUI']
    command2 = "echo \"<h1>Ultimos dados do dispositivo {} da Aplicação {}</h1>\" > ./templates/visualizacao.html".format(device,appUI)
    os.system(command2)
    command = "tail -1 ../Devices/{}/{}/data >> ./templates/visualizacao.html".format(appUI,device)
    os.system(command)

    return render_template('visualizacao.html')





if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=True ) # com debug true vai bastar salvar ao inves de ficar rodando diversas vezes