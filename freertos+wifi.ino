#include <Wire.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>


// parametry sieci
// const char* ssid = "sensor_ap";
// const char* password = "sensor_ap";
const char* ssid = "toya525443076";
const char* password = "05921029";

// deklaracje handlerów tasków
TaskHandle_t wifiTask;
TaskHandle_t httpTask;
TaskHandle_t taskxx;


// zmienne do testowania ramek danych
int soilTemperatureSensorValue = 255;
int soilMoistureSensorValue = 255;
int airTemperatureSensorValue = 255;
int airHumiditySensorValue = 255;
String dataFrame = "";

// deklaracja ledów do wizualizacji w taskach
const int led_1 = 15;
const int led_2 = 2;


void setup() {
  Serial.begin(115200); 
  pinMode(led_1, OUTPUT);
  pinMode(led_2, OUTPUT);
  

// stworzenie tasków wykonujących poszczególne funkcje
  xTaskCreatePinnedToCore(wifiTaskCode, "wifi task", 10000, NULL, 2, &wifiTask, 0);         
  delay(500); // te delaye teoretycznie zbędne, ale lepiej zostawić, żeby ta inicjalizacja przeszła bez problemów

  xTaskCreatePinnedToCore(httpHandlerTask,"http_task",10000,NULL,1,&httpTask,1);          
  delay(500); 

  xTaskCreatePinnedToCore(sensorDataCollector, "sensorDataCollector",10000,NULL,1,&taskxx,1);          
  delay(500); 
}

void wifiTaskCode( void * parameter){
  Serial.print("wifi task is running on core ");
  Serial.println(xPortGetCoreID());
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid,password);
  delay(10000);
  for(;;){
    digitalWrite(led_1, HIGH);
    if (WiFi.status() == WL_CONNECTED){
      Serial.println("connected"); // TODO: uptime
      delay(5000);    
      // continue;
    }
    else{
      Serial.print("reconnecting\n");
      WiFi.mode(WIFI_STA);
      WiFi.begin(ssid,password);
      delay(5000); 
    }
    digitalWrite(led_1, LOW);
    delay(5000);
  }
}

void httpHandlerTask( void * parameter){
  Serial.print("http_handler task is running on core ");
  Serial.println(xPortGetCoreID());
  
  for(;;){
    digitalWrite(led_2, HIGH);    
      if(WiFi.status()==WL_CONNECTED){
        HTTPClient http;

        http.begin("https://servertest.knowalinski.repl.co");
        http.addHeader("Content-Type", "text/plain");
        http.POST(dataFrame);
        delay(10000);      
    }
      
  digitalWrite(led_2, LOW);
  delay(1000);}
}

void sensorDataCollector(void * parameter){
  StaticJsonDocument<256> doc;
  for(;;){
  // Q: ale w sumie na chuja mu wysyłać czas, skoro serwer sobie zaindeksuje wiadomość do aktualnego czasu
  // A: jak będzie wysyłać zakolejkowane zaległe wiadomości to się może przydać, chociaż w sumie na chuja wysyłać zaległe, jak można je olać
  // doc["time"] = 5; // TODO: dodać funkcje getTime() pobierającą czas z serwera
  doc["soil_temperature"] = soilTemperatureSensorValue;
  doc["soil_moisture"] = soilMoistureSensorValue;
  doc["air_temperature"] = airTemperatureSensorValue;
  doc["air_humidity"] = airHumiditySensorValue;
  serializeJson(doc, dataFrame);
  delay(10000);
  }
  
}

void loop() {
  
}
