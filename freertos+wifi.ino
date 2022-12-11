#include <Wire.h>
#include <WiFi.h>
#include <HTTPClient.h>


// parametry sieci
const char* ssid = "sensor_ap";
const char* password = "sensor_ap";

// deklaracje handlerów tasków
TaskHandle_t Task1;
TaskHandle_t Task2;
TaskHandle_t wifiTask;
TaskHandle_t httpTask;
TaskHandle_t taskxx;


// zmienne do testowania ramek danych
int soilTSensor = 0;
int soilHSensor = 0;
int tSensor = 0;
int hSensor = 0;
String dataFrame = "";

// deklaracja ledów do wizualizacji w taskach
const int led_1 = 15;
const int led_2 = 2;


void setup() {
  Serial.begin(115200); 
  pinMode(led_1, OUTPUT);
  pinMode(led_2, OUTPUT);

// stworzenie tasków wykonujących poszczególne funkcje
  xTaskCreatePinnedToCore(wifiTaskCode,
  "wifi task", // nazwa taska (to może być opisowe, nie jest to przetwarzane, słuzy do identyfikacji)
  10000, // wielkość stosu zarezerwowana dla taska
  NULL, // chuj wi
  2, // priorytet taska
  &wifiTask, // handler
  0); // rdzeń na którym się to odpala           
  delay(500); // te delaye teoretycznie zbędne, ale lepiej zostawić, żeby ta inicjalizacja przeszła bez problemów

  xTaskCreatePinnedToCore(httpHandlerTask,"http_task",10000,NULL,1,&httpTask,1);          
  delay(500); 

  xTaskCreatePinnedToCore(paramsHandlerTask, "paramsHandlerTask",10000,NULL,1,&taskxx,1);          
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
void paramsHandlerTask( void * parameter) {
  for(;;){
delay(1000);    
        soilTSensor++;
        soilHSensor++;
        tSensor++;
        hSensor++;
        // dataFrame = soilTSensor + ":" + soilHSensor + ":" + tSensor + ":" + hSensor + ";";
        dataFrame = "sT:{" + String(soilTSensor) + "}sH:{" + String(soilHSensor) + "}T:{" + String(tSensor)+"}H:{" + String(hSensor)+"}";
  }
}
void httpHandlerTask( void * parameter){
  Serial.print("http_handler task is running on core ");
  Serial.println(xPortGetCoreID());
  
  for(;;){
  digitalWrite(led_2, HIGH);    
    if(WiFi.status()==WL_CONNECTED){
      HTTPClient http;

      http.begin("http://192.168.1.137:5000");
      http.addHeader("Content-Type", "text/plain");
      http.POST(dataFrame);
delay(1000);      
    }
      
  digitalWrite(led_2, LOW);
  delay(1000);}
}


void loop() {
  
}
