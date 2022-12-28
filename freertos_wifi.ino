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
TaskHandle_t sensorTask;


// zmienne do testowania ramek danych
int sensorId = 1;
int soilTemperatureSensorValue = 255;
int soilMoistureSensorValue = 255;
double airTemperatureSensorValue = 255;
int airHumiditySensorValue = 255;
String dataFrame = "";
String getTime = "";

// deklaracja ledów do wizualizacji w taskach
const int led_1 = 15;
const int led_2 = 2;


void setup() {
  Serial.begin(115200); 
  pinMode(led_1, OUTPUT);
  pinMode(led_2, OUTPUT);
  

// stworzenie tasków wykonujących poszczególne funkcje
  xTaskCreatePinnedToCore(wifiTaskCode, "wifi task", 10000, NULL, 2, &wifiTask, 0);         
  delay(500);

  xTaskCreatePinnedToCore(httpHandlerTask,"http_task",10000,NULL,1,&httpTask,1);          
  delay(500); 

  xTaskCreatePinnedToCore(sensorDataCollector, "sensorDataCollector",10000,NULL,1,&sensorTask,1);          
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

        // http.begin("https://servertest.knowalinski.repl.co");
        http.begin("http://10.5.101.7:5000/data-collector");
        http.addHeader("Content-Type", "text/plain");
        http.POST(dataFrame);
        http.end();
        delay(10000);      
    }
      
  digitalWrite(led_2, LOW);
  delay(100);}
}

void sensorDataCollector(void * parameter){
  StaticJsonDocument<1024> doc;
  StaticJsonDocument<256> docTime;
  for(;;){
  dataFrame.clear();
  doc.clear();
  getTime.clear();
  HTTPClient http;
  http.begin("http://10.5.101.7:5000/get-datetime");
  http.GET();
  getTime = http.getString();
  

  deserializeJson(docTime, getTime);
  Serial.println(getTime);

  airTemperatureSensorValue = random(2200,2500);
  doc["sensor_id"] = random(1,5);
  // doc["soil_temperature"] = soilTemperatureSensorValue;
  doc["soil_temperature"] = airTemperatureSensorValue/100;
  doc["soil_moisture"] = soilMoistureSensorValue;
  doc["air_temperature"] = String(airTemperatureSensorValue/100);
  doc["air_humidity"] = airHumiditySensorValue;
  doc["date"] = docTime["date"];
  doc["time"] = docTime["time"];
  // doc["sensor_id"] = random(1,5);
  // doc["soil_temperature"] = random(200,220)/10;
  // doc["soil_moisture"] = random(90,95);
  // doc["air_temperature"] = random(200,230)/10;
  // doc["air_humidity"] = random(70,75);
  serializeJson(doc, dataFrame);
  Serial.println(dataFrame);
  
  http.end();
  delay(9000);
  }
  
}

void loop() {
  
}
