import paho.mqtt.client as mqtt
import time
import json
import random
from datetime import date

class simulador_Oximetro:

    def __init__(self, temperatura : float, O2 : int, id : str, bpm : int):
        self.O2 = O2
        self.temperatura = temperatura
        self.id = id
        self.bpm = bpm

    def get_o2(self):
        return (random.randint(self.O2 - 2, self.O2 + 2))

    def get_temperatura(self):
        return float(random.randint(self.temperatura-1, self.temperatura+1))

    def get_bpm(self):
        return (random.randint(self.bpm-3, self.bpm+3))


    def generate_payload(self, bpm, temperatura, id, o2):
        timestamp = time.time()
        payload = {"Timestamp": timestamp, "BPM": bpm, "Temperatura" : temperatura,"ID": id, "Oxigenio": o2}
        payload = json.dumps(payload)
        return payload

    def main(self):

        bpm = self.get_bpm()
        temperatura = self.get_temperatura()
        o2 = self.get_o2()
        payload = self.generate_payload(bpm, temperatura, self.id, o2)
        
        return payload
