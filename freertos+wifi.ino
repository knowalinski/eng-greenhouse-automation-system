#include <Wire.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <Adafruit_SSD1306.h>

// const char* ssid = "toya525443076";
// const char* password =  "05921029";
const char* ssid = "sensor_ap";
const char* password = "sensor_ap";


Adafruit_SSD1306 display = Adafruit_SSD1306(128, 32, &Wire);

TaskHandle_t Task1;
TaskHandle_t Task2;
TaskHandle_t wifiTask;
TaskHandle_t oledTask;

const int led_1 = 15;
const int led_2 = 2;

void setup() {
  Serial.begin(115200); 
  pinMode(led_1, OUTPUT);
  pinMode(led_2, OUTPUT);

  xTaskCreatePinnedToCore(wifiTaskCode,"wifi task",10000,NULL,2,&wifiTask,0);                         
  delay(500); 

  xTaskCreatePinnedToCore(oledTaskCode,"Task2",10000,NULL,1,&oledTask,1);          
  delay(500); 


  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println(F("SSD1306 allocation failed"));
    while (1){yield();}}
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



void oledTaskCode( void * parameter ){
  Serial.print("oled task is running on core ");
  Serial.println(xPortGetCoreID());

  for(;;){
  digitalWrite(led_2, HIGH);
  delay(1000);
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(WHITE);
  display.setCursor(0, 10);
  // Display static text
  display.println("Hello, world!");
  display.println(WiFi.status());
  display.display(); 
  
  digitalWrite(led_2, LOW);
  delay(1000);
  }
}



void loop() {
  
}