#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <DHT_U.h>
#include <Servo.h>

// Definir los pines para los 5 LEDs
#define PIN_LED1 12
#define PIN_LED2 13
#define PIN_LED3 11
#define PIN_LED4 10
#define PIN_LED5 1
#define PIN_LLAMA 8
#define PIN_HUMEDAD A0
#define PIN_MOVIMIENTO 9
#define SERVO_PIN 7
#define DHTPIN 2     // Pin digital conectado al sensor
#define DHTTYPE DHT11   // Definir el tipo de sensor DHT

int servoPos = 0;
Servo myServo;  // Declaración del servo
DHT dht(DHTPIN, DHTTYPE);

// Variables para almacenar el estado de cada LED
bool led1State = false;
bool led2State = false;
bool led3State = false;
bool led4State = false;
bool led5State = false;
bool flameSensor;
bool fire = false;
bool sismo = false;
bool movimientoState = false;
float lastHumedadPorciento = 0.0; 
bool servoOpened = false; // Estado actual del servo

String serverMessage = "";  // Inicializa la variable para los mensajes del servidor
char delimitador = '_';

unsigned long lastHumedadSendTime = 0;  // Variable para controlar el intervalo de envío de humedad

void setup() {
  Serial.begin(9600);
  pinMode(PIN_LED1, OUTPUT);
  pinMode(PIN_LED2, OUTPUT);
  pinMode(PIN_LED3, OUTPUT);
  pinMode(PIN_LED4, OUTPUT);
  pinMode(PIN_LED5, OUTPUT);
  pinMode(PIN_LLAMA, INPUT);
  pinMode(PIN_MOVIMIENTO, INPUT);
  myServo.attach(SERVO_PIN);
  myServo.write(0);  // Inicialmente en posición cerrada
  dht.begin();
}

void loop() {
  flameSensor = digitalRead(PIN_LLAMA);
  if (flameSensor && !fire) {
    Serial.write("fuego\n");
    fire = true;
    delay(2000);
  }
  if (!flameSensor && fire) {
    Serial.write("nofuego\n");
    fire = false;
    delay(2000);
  }



  movimientoState = digitalRead(PIN_MOVIMIENTO);
  if (movimientoState && !sismo) {
    Serial.write("nosismo\n");
    sismo = true;
    delay(2000);
  }
  if (!movimientoState && sismo) {
    Serial.write("sismo\n");
    sismo = false;
    delay(2000);
  }

  if (Serial.available() > 0) {
    serverMessage = Serial.readStringUntil('\n');
    if (serverMessage.equals("humedad")) {
      float h = dht.readHumidity();
      if (isnan(h)) {
        Serial.println("Error al leer del sensor DHT!");
      } else {
        Serial.print("Humedad: ");
        Serial.print(h);
        Serial.println(" %");
     }
    }
    if (serverMessage.equals("LED1")) {
      led1State = !led1State;
      digitalWrite(PIN_LED1, led1State ? HIGH : LOW);
    } else if (serverMessage.equals("LED2")) {
      led2State = !led2State;
      digitalWrite(PIN_LED2, led2State ? HIGH : LOW);
    } else if (serverMessage.equals("LED3")) {
      led3State = !led3State;
      digitalWrite(PIN_LED3, led3State ? HIGH : LOW);
    } else if (serverMessage.equals("LED4")) {
      led4State = !led4State;
      digitalWrite(PIN_LED4, led4State ? HIGH : LOW);
    } else if (serverMessage.equals("LED5")) {
      led5State = !led5State;
      digitalWrite(PIN_LED5, led5State ? HIGH : LOW);
    } else if (serverMessage.equals("puerta")) {
      if (!servoOpened) {
        // Girar por 5 segundos
        unsigned long startTime = millis();
        while (millis() - startTime < 5000) {
          myServo.write(270);  // Ajusta el valor si es necesario
          delay(15);
        }
        servoOpened = true;  // Marcar el servo como abierto
      } else {
        // Regresar a la posición original
        myServo.write(0);  // Posición cerrada
        servoOpened = false;  // Marcar el servo como cerrado
      }
    }
  }
}
