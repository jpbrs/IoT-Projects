#include <SPI.h>
#include <LoRa.h>
#include "DHT.h"
#include "mbedtls/aes.h"
#define dUI "iotwan01"
#define aUI "0X0X"
#define DHTPIN 4     // Digital pin connected to the DHT sensor
#define DHTTYPE DHT11   // DHT 11
//Definindo os pinos a serem usados no transceiver
#define ss 5
#define rst 14
#define dio0 2

char * key = "iotwanprojectkey";
DHT dht(DHTPIN, DHTTYPE);


int counter = 0;


String create_plain_text(int number){
  String MIC_text;
  MIC_text.concat(dUI);
  MIC_text.concat(aUI);
  char c_str[4];
  sprintf(c_str,"%04d",number);
  MIC_text.concat(c_str);
  return MIC_text;
}

String create_mic_hash(int nonce){
  char jr_buffer[17];
  create_plain_text(nonce).toCharArray(jr_buffer, sizeof(jr_buffer));
  
  char *plainText = jr_buffer;
  unsigned char cipherTextOutput[16];

  encrypt(plainText, key, cipherTextOutput);
  String MIC_hash;

  Serial.println("\nMIC:");
  for (int i = 0; i < 16; i++) {

    char str[3];

    sprintf(str, "%02x", (int)cipherTextOutput[i]);
    MIC_hash.concat(str[0]);
    MIC_hash.concat(str[1]);
  }
  Serial.println(MIC_hash);
  return MIC_hash;
  
}

String create_payload_hash(String payload){
  int tamanho = payload.length();
  String junk = "#";
  
  if(tamanho > 16){
    Serial.println("Tamanho de dados não suportado");
    return junk;
  } else if(tamanho > 0){
    int dif = 16 - tamanho;
    for(int j = 0; j < dif; j++){
      payload.concat(junk);
    }
  } else{
    return junk;
  }


  char payload_buffer[17];
  payload.toCharArray(payload_buffer, sizeof(payload_buffer));

  char *payload_text = payload_buffer;
  unsigned char cipherTextOutput[16];

  encrypt(payload_text, key, cipherTextOutput);
  String payload_hash;

  Serial.println("\n Payload Hash:");
  for (int i = 0; i < 16; i++) {

    char str[3];

    sprintf(str, "%02x", (int)cipherTextOutput[i]);
    payload_hash.concat(str[0]);
    payload_hash.concat(str[1]);
  }
  Serial.println(payload_hash);
  return payload_hash;
  
}

void encrypt(char * plainText, char * key, unsigned char * outputBuffer){

  mbedtls_aes_context aes;

  mbedtls_aes_init( &aes );
  mbedtls_aes_setkey_enc( &aes, (const unsigned char*) key, strlen(key) * 8 );
  mbedtls_aes_crypt_ecb( &aes, MBEDTLS_AES_ENCRYPT, (const unsigned char*)plainText, outputBuffer);
  mbedtls_aes_free( &aes );
}

void decrypt(unsigned char * chipherText, char * key, unsigned char * outputBuffer){

  mbedtls_aes_context aes;

  mbedtls_aes_init( &aes );
  mbedtls_aes_setkey_dec( &aes, (const unsigned char*) key, strlen(key) * 8 );
  mbedtls_aes_crypt_ecb(&aes, MBEDTLS_AES_DECRYPT, (const unsigned char*)chipherText, outputBuffer);
  mbedtls_aes_free( &aes );
}

void setup() {
  dht.begin();
  Serial.begin(115200);

  while (!Serial);
  Serial.println("LoRa Sender");

  LoRa.setPins(ss, rst, dio0);
  while (!LoRa.begin(915E6)){
    Serial.println(".");
    delay(500);
  }
  LoRa.setSyncWord(0xF3);
  LoRa.setSpreadingFactor(12);
  Serial.println("LoRa Initializing OK!");
}

String create_join_request_payload(String MIC_HASH, int nonce_number){
  
  String payload_str = "{";
  payload_str.concat("JR:");
  payload_str.concat(1);
  payload_str.concat(",");
  payload_str.concat("appUI:");
  payload_str.concat(aUI);
  payload_str.concat(",");
  payload_str.concat("MIC:");
  payload_str.concat(MIC_HASH);
  payload_str.concat(",");
  payload_str.concat("devUI:");
  payload_str.concat(dUI);
  payload_str.concat(",");
  payload_str.concat("nonce:");
  payload_str.concat(nonce_number);
  payload_str.concat("}");


  return payload_str;
}

String create_data_payload(){
  
  float t = dht.readTemperature();
  int temp = round(t);
  float h = dht.readHumidity();
  int um = round(h);


  String payload_str = ("T:");
  payload_str.concat(temp);
  payload_str.concat(",");
  payload_str.concat("U:");
  payload_str.concat(um);

  return payload_str;
  
}

String create_final_payload(String payload_hash, int counter, String MIC_HASH){
  String payload_str = ("JR:");
  payload_str.concat(0);
  payload_str.concat(",");
  payload_str.concat("appUI:");
  payload_str.concat(aUI);
  payload_str.concat(",");
  payload_str.concat("MIC:");
  payload_str.concat(MIC_HASH);
  payload_str.concat(",");
  payload_str.concat("devUI:");
  payload_str.concat(dUI);
  payload_str.concat(",");
  payload_str.concat("counter:");
  payload_str.concat(counter);
  payload_str.concat(",");
  payload_str.concat("payload:");
  payload_str.concat(payload_hash);


  return payload_str;

}


void loop() {

  int nonce = random(0,9999);
  String MIC_HASH_jr = create_mic_hash(nonce);
  String payload_jr = create_join_request_payload(MIC_HASH_jr, nonce);
  
  //Join Request messages
  for(int j = 0; j <3; j++){
    LoRa.beginPacket();
    LoRa.print(payload_jr);
    LoRa.endPacket();
    Serial.println("Join request sent:");
    Serial.println(payload_jr);    
    delay(1000);
  }

  for(int i = 0; i<999999; i++){
    String MIC_HASH_pl = create_mic_hash(counter);
    String data = create_data_payload();
    String payload_hash = create_payload_hash(data);
    String final_payload = create_final_payload(payload_hash, counter, MIC_HASH_pl);
    
    Serial.print("Enviando pacote:\n");
    Serial.println(final_payload);
    Serial.print("Com Payload criptografado:\n");
    Serial.println(data);

    LoRa.beginPacket();
    LoRa.print(final_payload);
    LoRa.endPacket();

    delay(1000);
    counter++;
  }

  

  delay(5000);
}
