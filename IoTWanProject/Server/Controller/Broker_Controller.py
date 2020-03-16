import paho.mqtt.client as mqtt
import json
from Crypto.Cipher import AES
import binascii
import os
import os.path
from os import path
from datetime import datetime


def check_MIC(MIC : str,dUI : str,aUI : str,number : str, key : str):
    encryptor = AES.new(str(key), AES.MODE_ECB)
    text = str(dUI)+str(aUI)+str(number).zfill(4)
    ciphertext = encryptor.encrypt(text)
    a = binascii.hexlify(ciphertext)
    a = a.decode()

    return(MIC == a)

def decrypt_message(key : str, text : str):
    encryptor = AES.new(str(key), AES.MODE_ECB)
    text_hexa = binascii.unhexlify(text)
    texto_decriptado_hexa = encryptor.decrypt(text_hexa)
    texto_real = texto_decriptado_hexa.decode().strip("#")
    return texto_real



def treat_JR(data_dict : dict):
    try:
        caminho = "../Devices/{}/{}".format(data_dict['appUI'], data_dict['devUI'])

        if path.exists(caminho):
            key_path = "../Devices/{}/{}/key".format(data_dict['appUI'], data_dict['devUI'])
            arq_key = open(key_path, "r+")
            key = arq_key.readline()
            key = key[:-1]
            if data_dict['JR'] == '1':
                if check_MIC(data_dict['MIC'],data_dict['devUI'],data_dict['appUI'],data_dict['nonce'],key):
                    nonce = "../Devices/{}/{}/nonce".format(data_dict['appUI'], data_dict['devUI'])
                    counter = "../Devices/{}/{}/counter".format(data_dict['appUI'], data_dict['devUI'])
                    arq_nonce = open(nonce,"r+")
                    if arq_nonce.readline() == data_dict['nonce']:
                        print("Nonce already Used")
                    else:
                        command = "echo {} > {}".format(data_dict['nonce'],nonce)
                        command = "echo -1 > {}".format(counter)

                        os.system(command)
            else:
                if check_MIC(data_dict['MIC'],data_dict['devUI'],data_dict['appUI'],data_dict['counter'],key):
                    counter = "../Devices/{}/{}/counter".format(data_dict['appUI'], data_dict['devUI'])

                    arq_counter = open(counter,"r+")
                    number = arq_counter.readline()
                    if int(number) >= int(data_dict['counter']) :
                        print("Repeated message")
                    else:
                        command = "echo {} > {}".format(data_dict['counter'],counter)
                        os.system(command)
                        data = decrypt_message(key,data_dict['payload'])

                        data_path = "../Devices/{}/{}/data".format(data_dict['appUI'], data_dict['devUI'])
                        date = datetime.now().strftime("%Y-%m-%d")
                        hour = datetime.now().strftime("%H:%M:%S")
                        command2 = "echo {},{},{} >> {}".format(date,hour,data,data_path)
                        os.system(command2)
        else:
            print("Device not Registered")
    except:
        print("Invalid data")
        exit(1)

username="hello"
password="world"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    client.subscribe("iotwanproject")


def on_message(client, userdata, msg):
    data = str(msg.payload.decode())
    print(msg.topic+" "+data)
    data_array = data.split(",")

    print(data_array)

    data_dict = {}
    try: 
        for i in range(0,len(data_array)):
            data_array[i] = data_array[i].split(":")
            data_dict[str(data_array[i][0])] = str(data_array[i][1])
    except:
        print("Invalid Data")
        exit(1)

        
    print(data_dict)
    treat_JR(data_dict)
    


client = mqtt.Client(client_id="subsription")
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set(username, password=password)

client.connect("0.0.0.0", 1883, 60)

client.loop_forever()


