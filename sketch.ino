#include <DHT.h>
#include <DHT_U.h>
#include <Servo.h>
#include <OneWire.h>
#include <DallasTemperature.h>

#include <String.h>
#include <stdio.h>

#define LPIN0 2
#define LPIN1 3
#define LPIN2 4
#define LPIN3 5
#define LPIN4 6

#define PPIN0 7
#define PPIN1 8

#define HPIN0 9

#define DHTTYPE DHT11

#define DHTPIN0 10
#define DHTPIN1 11
#define DHTPIN2 12

#define DTPIN0 13

#define USTRIGPIN0 22
#define USECHOPIN0 23

bool switchin = true;
float usTemp1 = 0.0;
float usTemp2 = 0.0;

OneWire oneWire0(DTPIN0);
DallasTemperature dTSens0(&oneWire0);

Servo servo0;
Servo servo1;

DHT dht0(DHTPIN0, DHTTYPE);
DHT dht1(DHTPIN1, DHTTYPE);
DHT dht2(DHTPIN2, DHTTYPE);

unsigned long tempTime = millis();

char comInput[64] = "O-0-0";

void StringParse(char* str)
{
  char *token = strtok(str, "-");

  char com[64];
  char sID[64];
  char sIN[64];
  
  strcpy(com, token);
  token = strtok(NULL, "-");
  strcpy(sID, token);
  token = strtok(NULL, "-");
  strcpy(sIN, token);

  int lookup;

  if(strcmp(com, "L") == 0)
    lookup = 0;
  else if(strcmp(com, "H") == 0)
    lookup = 1;
  else if(strcmp(com, "P") == 0)
    lookup = 2;
  else
    lookup = 3;  
  switch(lookup)
  {
    case 0:
      LightControll(atoi(sID), atoi(sIN));
      Serial.print("\nLIGHTS ");
      Serial.print(sID);
      Serial.print(" ");
      Serial.println(sIN);
      break;
    case 1:
      HeaterRelay(atoi(sID), atoi(sIN));
      Serial.print("\nHEAT ");
      Serial.print(sID);
      Serial.print(" ");
      Serial.println(sIN);
      break;
    case 2:
      Serial.print("\nPUMP ");
      Serial.print(sID);
      Serial.print(" ");
      Serial.println(sIN);
      break;
    case 3:
      Serial.println("\nERROR PARSING");
      break;
      
  }

}

void ServoControll(Servo servo, bool state)
{
    int servoPos = 0;
    if(state)
    {
      for (servoPos = 10; servoPos <= 160; servoPos += 1) 
        servo.write(servoPos);              
      for (servoPos = 160; servoPos >= 10; servoPos -= 1) 
        servo.write(servoPos);                
    }
    else
      servo.write(servoPos);
}

void LightControll(int pin, int perc)
{
  int output = map(perc, 0, 100, 0, 255);
  analogWrite(pin, output);
}

void HeaterRelay(int pin, bool state)
{
  digitalWrite(pin, state);
}

void DHTRead(DHT dht, int ID)
{
  char hOut[64];
  char tOut[64];

  float hTemp = dht.readHumidity();
  float tTemp = dht.readTemperature();

  strcpy(hOut, "DHTH-");
  strcat(hOut, String(ID).c_str());
  strcat(hOut, "-");
  strcat(hOut, String(hTemp).c_str());

  strcpy(tOut, "DHTT-");
  strcat(tOut, String(ID).c_str());
  strcat(tOut, "-");
  strcat(tOut, String(tTemp).c_str());

  
  Serial.print(hOut);
  Serial.print("\n");
  Serial.print(tOut);
  Serial.print("\n");
}

void DTRead(DallasTemperature dTSens, int ID)
{
    char tOut[64];
    dTSens.requestTemperatures();  
    float tTemp = dTSens.getTempCByIndex(0);
    
    strcpy(tOut, "DT-");
    strcat(tOut, String(ID).c_str());
    strcat(tOut, "-");
    strcat(tOut, String(tTemp).c_str());

    Serial.print(tOut);
}

float UsControll(int echoPin)
{
  float pulse, output;
  pulse = pulseIn(echoPin, HIGH);
  output = 0.017 * pulse;
  return output;
}

void setup() 
{
  pinMode(LPIN0, OUTPUT);
  pinMode(LPIN1, OUTPUT);
  pinMode(LPIN2, OUTPUT);
  pinMode(LPIN3, OUTPUT);
  pinMode(LPIN4, OUTPUT);

  pinMode(HPIN0, OUTPUT);

  pinMode(USTRIGPIN0, OUTPUT);
  pinMode(USECHOPIN0, INPUT);  

  servo0.attach(PPIN0);
  servo1.attach(PPIN1);

  dht0.begin();

  Serial.begin(115200);
  
  
}

void loop() 
{
  while(Serial.available())
  {
    strcpy(comInput, Serial.readString().c_str());
    StringParse(comInput);
  }
  digitalWrite(USTRIGPIN0, HIGH);
  delayMicroseconds(10);
  digitalWrite(USTRIGPIN0, LOW);
  usTemp1 = UsControll(USECHOPIN0);
  if(switchin)
  {
    usTemp2 = usTemp1;
  }
  else
  {
    if((usTemp2+usTemp1)<20)
      digitalWrite(LPIN0, HIGH);
  }
  switchin = !switchin;
  
  if(millis() - tempTime > 10000)
  {
    DHTRead(dht0, 0);
    DHTRead(dht1, 1);
    DHTRead(dht2, 2);

    DTRead(dTSens0, 0);

    digitalWrite(LPIN0, LOW);
    
    tempTime = millis();
  }

}
