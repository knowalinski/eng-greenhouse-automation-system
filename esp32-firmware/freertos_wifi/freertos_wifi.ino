#include <Wire.h>
#include <WiFi.h>
#include <Arduino.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <driver/adc.h>
#include "Adafruit_SHT31.h"



#pragma region VARIABLES
#define AOUT_PIN 36

const char *ssid = "toya525443076";
const char *password = "05921029";

int sensorID = 1;

Adafruit_SHT31 sht31 = Adafruit_SHT31();

double prevTemperature = 0, prevHumidity = 0, prevMoisture = 0;
double temperature, humidity, soilMoisture;

// deklaracje handlerów tasków
TaskHandle_t wifiTask;
TaskHandle_t httpTask;
TaskHandle_t sensorTask;
TaskHandle_t sensorOperatorTask;

String dataFrame = "";
String getTime = "";

// deklaracja ledów do wizualizacji w taskach
const int led_1 = 15, led_2 = 2;

#pragma endregion // VARIABLES

#pragma region SETUP
void setup()
{
  Serial.begin(115200);
  sht31.begin(0x44);
  pinMode(led_1, OUTPUT);
  pinMode(led_2, OUTPUT);

  // stworzenie tasków wykonujących poszczególne funkcje
  xTaskCreatePinnedToCore(wifiTaskCode, "wifi task", 10000, NULL, 2, &wifiTask, 0);
  delay(500);

  xTaskCreatePinnedToCore(httpHandlerTask, "http_task", 5000, NULL, 1, &httpTask, 1);
  delay(500);

  xTaskCreatePinnedToCore(sensorDataCollector, "sensorDataCollector", 10000, NULL, 1, &sensorTask, 1);
  delay(500);

  xTaskCreatePinnedToCore(sensorOperator, "sensorOperator", 5000, NULL, 1, &sensorOperatorTask, 1);
  delay(500);
}
#pragma endregion // SETUP

#pragma region WIFI
void wifiTaskCode(void *parameter)
{
  Serial.print("wifi task is running on core ");
  Serial.println(xPortGetCoreID());
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  delay(10000);
  for (;;)
  {
    digitalWrite(led_1, HIGH);
    if (WiFi.status() == WL_CONNECTED)
    {
      Serial.println("connected");
      delay(5000);
    }
    else
    {
      Serial.print("reconnecting\n");
      WiFi.mode(WIFI_STA);
      WiFi.begin(ssid, password);
      delay(5000);
    }
    digitalWrite(led_1, LOW);
    delay(5000);
  }
}

#pragma endregion // WIFI

#pragma region HTTP
void httpHandlerTask(void *parameter)
{
  Serial.print("http_handler task is running on core ");
  Serial.println(xPortGetCoreID());

  for (;;)
  {
    digitalWrite(led_2, HIGH);
    if (WiFi.status() == WL_CONNECTED)
    {
      HTTPClient http;

      http.begin("http://10.5.101.7:5000/data-collector");

      http.addHeader("Content-Type", "text/plain");
      http.POST(dataFrame);
      http.end();
      delay(10000);
    }

    digitalWrite(led_2, LOW);
    delay(100);
  }
}
#pragma endregion // HTTP

#pragma region SENSOR_OPERATOR
void sensorOperator(void *parameter)
{

  for (;;)
  {
    if (WiFi.status() == WL_CONNECTED)
    {
      double temperatureReading = sht31.readTemperature();
      double humidityReading = sht31.readHumidity();

      if (!isnan(temperatureReading))
      {
        temperature = temperatureReading;
        prevTemperature = temperatureReading;
      }
      else
      {
        temperature = prevTemperature;
      }

      if (!isnan(humidityReading))
      {
        humidity = humidityReading;
        prevHumidity = humidityReading;
      }
      else
      {
        humidity = prevHumidity;
      }

      double soilMoistureReading = analogRead(AOUT_PIN);
      soilMoistureReading = map(soilMoistureReading, 100, 600, 10000, 0);
      soilMoistureReading = soilMoistureReading / 100;
      if (0 < soilMoistureReading && soilMoistureReading < 100)
      {
        soilMoisture = soilMoistureReading;
        prevMoisture = soilMoistureReading;
      }
      else
      {
        soilMoisture = prevMoisture;
      }

      delay(1000);
    }
  }
}
#pragma endregion // DATA_OPERATOR

#pragma region DATA_COLLECTOR
void sensorDataCollector(void *parameter)
{
  StaticJsonDocument<1024> doc;
  StaticJsonDocument<256> docTime;
  for (;;)
  
  {
    if (WiFi.status() == WL_CONNECTED)
    {dataFrame.clear();
    doc.clear();
    docTime.clear();
    getTime.clear();
    HTTPClient http;
    http.begin("http://10.5.101.7:5000/get-datetime");
    http.GET();
    getTime = http.getString();
    http.end();

    deserializeJson(docTime, getTime);
    Serial.println(getTime);
    if (!docTime["date"].isNull() || !docTime["time"].isNull())
    {
      doc["sensor_id"] = sensorID;
      doc["air_temperature"] = temperature;
      doc["air_humidity"] = humidity;
      doc["soil_moisture"] = soilMoisture;
      doc["date"] = docTime["date"];
      doc["time"] = docTime["time"];

      serializeJson(doc, dataFrame);
      Serial.println(dataFrame);
    }

    delay(9000);
  }}
}
#pragma endregion // TASKS

void loop()
{
}
