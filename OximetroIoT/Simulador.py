import paho.mqtt.client as paho
import GeradorDados
import threading
import random
import time

n = 30 #Numero de threads/conexões com o broker (maximo suportado é 1000)


broker="192.168.0.18"
port=1883

def on_publish(client,userdata,result):             #create function for callback
    print("data published \n")
    pass

#Cria um nó virtual para simular uma unidade meteorológica que produzirá os dados
def simular(temperatura : float, O2 : int, id : str, bpm : int):
    while True:
        oximetro = GeradorDados.simulador_Oximetro(temperatura, O2, id, bpm)
        payload = oximetro.main()

        client1= paho.Client(str(id), clean_session=False, transport="tcp")                           #create client object
        client1.on_publish = on_publish                          #assign function to callback
        client1.connect(broker,port) 
        client1.loop_start()
        client1.publish(topic="oximetroiot",payload=payload,qos=2) 
        client1.loop_stop()
        time.sleep(2)


for i in range(1,n+1):
    
    temperatura = random.randint(36,40)
    o2 = random.randint(70,95)
    bpm = random.randint(60,80)

    t = threading.Thread(target=simular,args=(temperatura,o2,i,bpm))
    t.start()
