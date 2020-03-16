#include <SPI.h>
#include <LoRa.h>

//Definindo os pinos a serem usados no transceiver
#define ss 5
#define rst 14
#define dio0 2
#ifndef MQTT_MAX_PACKET_SIZE
#define MQTT_MAX_PACKET_SIZE 256
#endif
#include <WiFi.h>
#include <MQTT.h>                 //https://github.com/256dpi/arduino-mqtt
MQTTClient client(256);
const char* ssid = "COSTA E SILVA";
const char* password =  "mj12k890";
const char* mqttServer = "192.168.0.18";
const int mqttPort = 1883;
const char* mqttUser = "abcdefg";
const char* mqttPassword = "123456";
WiFiClient espClient;



void setup() {
  client.begin("192.168.0.18", espClient);

  //Frequencia do Monitor Serial
  Serial.begin(115200);
  while (!Serial);
  Serial.println("LoRa Receiver");
  //Configurando os pinos do transceiver LoRa
  LoRa.setPins(ss, rst, dio0);
  //915E6 for North America
  while (!LoRa.begin(915E6)) {
    Serial.println(".");
    delay(500);
  }
  LoRa.setSyncWord(0xF3);
  LoRa.setSpreadingFactor(12);

  Serial.println("Lora Inicializado!");
// ----------------------------------------------------------------------------------- //
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.println("Iniciando conexao com a rede WiFi..");
  }
  Serial.println("Conectado na rede WiFi!");

}


void reconectabroker()
{
  //Conexao ao broker MQTT
  while (!client.connect("192.168.0.18", mqttUser, mqttPassword))
  {
    Serial.print("Conectando ao broker");
    delay(1000);
  }
}




void loop() {
  reconectabroker();
  // try to parse packet
  int packetSize = LoRa.parsePacket();
  if (packetSize) {
    // pacote recebido
//    Serial.print("Pacote recebido '");
    // Ler pacote
    while (LoRa.available()) {
      String LoRaData = LoRa.readString();
      Serial.print(LoRaData);
      char mensagem[140];
      LoRaData.toCharArray(mensagem, 140); 

      client.publish("iotwanproject", mensagem);
    }
    // Mostra o RSSI do pacote
    Serial.print("' with RSSI ");
    Serial.println(LoRa.packetRssi());
  }
 //-------------------------------------------------------------

 


}
