#include <Wire.h>
#include <WiFi.h>
#include <HTTPClient.h>
// #include <Adafruit_SSD1306.h>

// const char* ssid = "toya525443076";
// const char* password =  "05921029";
const char* ssid = "sensor_ap";
const char* password = "sensor_ap";
String dataFrame = "";

// Adafruit_SSD1306 display = Adafruit_SSD1306(128, 32, &Wire);

TaskHandle_t Task1;
TaskHandle_t Task2;
TaskHandle_t wifiTask;
TaskHandle_t httpTask;
TaskHandle_t taskxx;
// HTTPClient http;
int soilTSensor = 0;
int soilHSensor = 0;
int tSensor = 0;
int hSensor = 0;

const int led_1 = 15;
const int led_2 = 2;

void setup() {
  Serial.begin(115200); 
  pinMode(led_1, OUTPUT);
  pinMode(led_2, OUTPUT);

  xTaskCreatePinnedToCore(wifiTaskCode,"wifi task",10000,NULL,2,&wifiTask,0);                         
  delay(500); 

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
