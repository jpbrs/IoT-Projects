import telegram.ext as telepot
import RPi.GPIO as GPIO
import _thread as thread
import time
import datetime as dt
from picamera import PiCamera
import os
camera = PiCamera()

camera.rotation = 180


##########################E-mail#############################
#colocando o email aqui ele envia uma notificação para recarregar a agua
#colocar o path do arquivo rega.txt no lugar de mensagem

email = 'jp.brs@poli.ufrj.br'
mensagem = 'ssmtp {} < /home/pi/Desktop/IoTProjects/rega.txt'

############################ GPIO #############################

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(7, GPIO.OUT) #Controlar a GPIO 4 pois o pino 7 será o controle do relé
GPIO.setup(18, GPIO.IN) #GPIO 24(pino 18) será a entrada de dados do meu sensor de luz
GPIO.setup(11, GPIO.IN) #Pino 11 será o Pino da GPIO de entrada de dados do higrometro


##############################Funções###############################

def kwget(key, kwargs, default=None):
    return kwargs[key] if key in kwargs else default

def emsg(msg, email):
    cmd = mensagem.format(email)
    os.system(cmd)

################################LUZ################################

#saida do sensor : 1 é apagado e 0 é iluminado
#pino relé é o pino in do relé
#pino_luminosidade é o pino conectado ao DOG do sensor LDR


class Luz:
    
    def __init__(self, pino_rele, pino_luminosidade):
        self.pino_rele = pino_rele
        self.pino_luminosidade = pino_luminosidade
        GPIO.setup(self.pino_rele, GPIO.OUT)
        GPIO.setup(self.pino_luminosidade, GPIO.IN)

        self.acesa = False

    def medir_luz(self):
        return GPIO.input(self.pino_luminosidade) #retorna se é true ou false baseado na quantidade de luz do quarto
    
    def liga_luz(self):
        GPIO.output(self.pino_rele, GPIO.LOW)
        
    def apaga_luz(self):
        GPIO.output(self.pino_rele, GPIO.HIGH)        
    def controlador_luz(self):
        self.apaga_luz()
        time.sleep(0.1)
        if self.medir_luz() == 1:
            self.liga_luz()
            if not self.acesa:
                self.acesa = True
                return 'luz acesa'
        else:
            if self.acesa:
                self.acesa = False
                return 'luz apagada'
    
##############################UMIDADE#############################
    
#saida do sensor : 1 é seco e 0 é umido
#pino_in_umidade é o pino conectado ao DOG do sensor de umidade do solo

class SemAgua(Exception):
    pass

class Agua:
    
    MAX_REGAS = 2;
    TEMPO_REGA = 2;
    
    def __init__(self, pino_in_umidade, pino_out_bomba, **kwargs):
        self.max_regas = kwget('max_regas', kwargs, MAX_REGAS)
        self.tempo_rega = kwget('tempo_rega', kwargs, TEMPO_REGA)
        
        self.pino_out_bomba = pino_out_bomba
        GPIO.setup(self.pino_out_bomba, GPIO.OUT)
        
        self.pino_in_umidade = pino_in_umidade
        GPIO.setup(self.pino_in_umidade, GPIO.IN)
        
        self.contador = 0;

    def umidade(self):
        return GPIO.input(self.pino_in_umidade)
        
    def rega(self, T):
        t = clock()
        yield True
        while clock() - t <= T:
            yield True
        else:
            yield False

    def regar_planta(self):
        if self.contador > self.max_regas:
            emsg(mensagem, email)
            raise SemAgua()
            
        rega = self.nova_rega()
        GPIO.output(self.pino_out_bomba, GPIO.HIGH)
        while rega(self.tempo_rega):
            continue
        else:
            GPIO.output(self,pino_out_bomba, GPIO.LOW)
            
        self.contador += 1
        print('Planta regada')
        
    def controlador_umidade(self):
        if self.umidade() == 1:
            self.regar_planta()
            return 'planta regada'

#############################################################
        
##########################################################################################        
    
#luz seria o controlador de luz
#agua seria o controlador de agua

class Bot:

    def __init__(self, token):
        self.token = token
        self.log = []

    def sendMessage(self, chat_id, msg):
        self.log.append((chat_id, msg))

    def sendVideo(self, chat_id, vfile):
        self.log.append((chat_id, vfile))

    def message_loop(self, handle):
        self.log.append(handle)

class InvalidCommand(Exception):
    pass
    
class Controlador():
    
    SLEEP_TIME = 5 # 1 minute
    LOG_FILE = 'control.log'
    LOG_FORMAT = "action: {}, time:{}"

    bot_token = '743802023:AAEaQu83rEO2ScZGFzPT2ShMWEXB6Gb_GEA'
    bot_id = 588134898
    
    def __init__(self, luz, agua, **kwargs):
        self.luz = luz
        self.agua = agua

        self.log_file = kwget('log_file', kwargs, self.LOG_FILE) 
        self.sleep_time = kwget('sleep_time', kwargs, self.SLEEP_TIME)
        self.bot = Bot(self.bot_token) #telepot.Bot(bot_token)

        self.setup_commands()
        self.in_loop = True

    def setup_commands(self):
        self.cmds = {}
        for item_name in dir(self):
            item = getattr(self, item_name)
            if hasattr(item, '__command__'):
                cmd_name = item.cmd_name
                self.cmds[cmd_name] = item

    def command(cmd):
        setattr(cmd, 'cmd_name', cmd.__code__.co_name)
        setattr(cmd, '__command__', True)
        return cmd

    def is_command(self, text):
        return text.startswith('/')

    def filter_command(self, cmd):
        cmd = cmd[1:]
        if (' ' in text) or cmd not in self.cmds:
            raise InvalidCommand('Unknow command: {}'.format(cmd))
        else:
            return cmd
        

    @command
    def Ola(self, chat_id, msg):
        self.bot.sendMessage(chat_id, 'Olá, Johnny')

    @command
    def liga_luz(self, chat_id, msg):
        self.bot.sendMessage(chat_id, 'Luz On')
        self.luz.liga_luz()

    @command
    def apaga_luz(self, chat_id, msg):
        self.bot.sendMessage(chat_id, 'Luz Off')
        self.luz.apaga_luz()            

    @command
    def photo(self, chat_id, msg):
        now = int(time.time())
        caminho = '/home/pi/Desktop/Share/{}.jpg'.format(now)
        camera.capture(caminho)
        self.bot.sendMessage(chat_id, '{}'.format(now))
        photo = 'https://api.telegram.org/file/bot{}/{}'.format(self.bot_token,caminho)
        self.bot.sendPhoto(chat_id, open(caminho, 'rb'))
        os.system('rm {}'.format(caminho))

    @command
    def video(self, chat_id, msg):
        now = int(time.time())
        caminho = '/home/pi/Desktop/Share/{}.h264'.format(now)
        camera.start_recording(caminho)
        time.sleep(15)
        camera.stop_recording()
        self.bot.sendMessage(chat_id, '{}'.format(now))
        novo_caminho = '/home/pi/Desktop/Share/{}.mp4'.format(now)
        os.system('MP4Box -fps 30 -add {} {}'.format(caminho, novo_caminho))
        self.bot.sendVideo(chat_id, open(novo_caminho, 'rb'))
        os.system('rm {}'.format(caminho))
        os.system('rm {}'.format(novo_caminho))

    @command
    def agua_recarregada(self, chat_id, msg):
        self.bot.sendMessage(chat_id, 'Contador zerado')
        self.agua.contador = 0

    @command
    def menu(self, chat_id, msg):
        string = ", ".join(map(lambda s:'/'+s,self.cmds.keys()))
        return self.bot.sendMessage(chat_id, string)

    
    def handle(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)

        if(content_type == 'text'):
            text = msg['text']
            print('Got command: {}'.format(text))

        if is_command(text):
            cmd = filter_command(txt)
        else:
            return None

        self.cmds[cmd](chat_id, msg)

    def log(self, action=None):
        if action is not None:
            return
        now = dt.datetime.now()
        args = (action, now.isoformat())
        log_string = self.LOG_FORMAT.format(*args)
        with open(self.log_file, 'a') as file:
            file.write(log_string)

    def loop(self):
        while self.in_loop:
            out = self.luz.controlador_luz()
            self.log(out)
            
            out = self.agua.controlador_umidade()
            self.log(out)
            time.sleep(self.sleep_time)
            
    def main(self):
        self.bot.message_loop(self.handle)
        thread.start_new(self.loop, ())
            

############################################################################################

##############################Funcionamento pinos 7,18,11##################################
    
controle_luz1 = Luz(7,18)
controle_agua1 = Agua(11)
Control1 = Controlador(controle_luz1, controle_agua1)
Control1.main()


##while True:
##    update = bot.getUpdates()
##    if update != []:
##        bot.sendMessage(bot_id, 'Olá, Johnny, meus comandos são:')
##        bot.sendMessage(bot_id, '/photo , /video, /stream, /luz')
##    update = []
        
