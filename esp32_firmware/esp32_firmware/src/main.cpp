#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "toya525443076";
const char* password =  "05921029";
// const char* ssid = "sensor_ap";
// const char* password = "sensor_ap";



void setup() {
 
  Serial.begin(115200);
  delay(5000);   //Delay needed before calling the WiFi.begin
 
  WiFi.begin(ssid,password);
  while (WiFi.status() != WL_CONNECTED) { //Check for the connection
    delay(1000);
    Serial.println("Connecting to WiFi..");
  }
  
  Serial.println("Connected to the WiFi network");
  
}
  
void loop() {
  
 if(WiFi.status()== WL_CONNECTED){
  
   HTTPClient http;   
  
   http.begin("http://10.11.29.26:5000");
   http.addHeader("Content-Type", "text/plain");
   http.POST("dupa from esp32");
  //  int httpResponseCode = http.POST("dupa from esp32");
  
//    if(httpResponseCode!=0){
  
//     String response = http.getString();
  
//     Serial.println(httpResponseCode);
//     Serial.println(response);
  
//    }else{
  
//     Serial.print("Error on sending POST: ");
//     Serial.println(httpResponseCode);
  
//    }
  
//    http.end();
  
//  }else{
  
//     Serial.println("Error in WiFi connection");   
  
//  }
  
//   delay(10000);
  
}}