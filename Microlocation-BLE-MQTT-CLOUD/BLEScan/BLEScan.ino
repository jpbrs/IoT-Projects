/*
   Based on Neil Kolban example for IDF: https://github.com/nkolban/esp32-snippets/blob/master/cpp_utils/tests/BLE%20Tests/SampleScan.cpp
   Ported to Arduino ESP32 by Evandro Copercini
*/


// --- WIFI ---
#include <WiFi.h>
WiFiClient nodemcuClient;

void conectarWifi() {
  delay(10);
  WiFi.begin("SSID", "PASSWORD");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
}


// --- MQTT ---
#include <PubSubClient.h>
const char* mqtt_Broker = "BROKER_IP";
const char* client_id = "L1";
PubSubClient client(nodemcuClient);

void reconectarMQTT() {
  while (!client.connected()) {
    client.connect(client_id);
  }
}


// ------- BLE --------

#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEScan.h>
#include <BLEAdvertisedDevice.h>


int scanTime = 5; //In seconds
boolean found = false; //Se encontrou o iTag no último scan
int trigger = 0;
std::string array_device[10] = {"","","","","","","","","",""};
int i = 0;

#define trigger1 "FUN"
#define trigger2 "MAN"



BLEScan* pBLEScan;

class MyAdvertisedDeviceCallbacks: public BLEAdvertisedDeviceCallbacks {
    void onResult(BLEAdvertisedDevice advertisedDevice) {
      Serial.printf("Advertised Device: %s \n", advertisedDevice.toString().c_str());
      trigger = 0;
        for(int n = 0; n < 3; n++){
                if(advertisedDevice.getName().c_str()[n] == trigger1[n]){
                    trigger++;
                } else{
                  trigger=0;
                  break;
                }
        }

        for(int n = 0; n <= 2; n++){
                if(trigger == 3){
                  break;
                }
                if(advertisedDevice.getName().c_str()[n] == trigger2[n]){
                    trigger++;
                } else{
                  trigger=0;
                  break;
                }
        }
        
        if(trigger == 3){
            Serial.println(i);
            array_device[i] = advertisedDevice.getName()+client_id;
            Serial.println(array_device[i].c_str());

            i+=1;
            found = true;
            //Marcamos como encontrado, paramos o scan e guardamos o rssi
            Serial.println("Trigger igual");
          }
      
    }
};

void setup() {
  Serial.begin(115200);
  Serial.println("Scanning...");

  BLEDevice::init("");
  pBLEScan = BLEDevice::getScan(); //create new scan
  pBLEScan->setAdvertisedDeviceCallbacks(new MyAdvertisedDeviceCallbacks());
  pBLEScan->setActiveScan(true); //active scan uses more power, but get results faster
  pBLEScan->setInterval(10000);
  pBLEScan->setWindow(1000);  // less or equal setInterval value
}

void loop() {

  BLEScanResults foundDevices = pBLEScan->start(scanTime, false);


  conectarWifi();
  client.setServer(mqtt_Broker, 1883);

  if (!client.connected()) {
        reconectarMQTT();
   }

   if(found){
        for(int j = 0; j< i; j++){
            Serial.println(array_device[j].c_str());
            client.publish("jpbrs/location/", array_device[j].c_str(), true); 
            delay(2000);

            array_device[i] = "";
            
        }
        found = false;
  }

  Serial.print("Devices found: ");
  Serial.println(foundDevices.getCount());
  Serial.println("Scan done!");
  pBLEScan->clearResults();   // delete results fromBLEScan buffer to release memory

  i = 0;
  WiFi.disconnect();
}
