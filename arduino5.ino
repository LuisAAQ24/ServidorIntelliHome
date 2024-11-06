#include <Adafruit_Sensor.h>

#include <DHT.h>
#include <DHT_U.h>


#include <Servo.h>

// Definir los pines para los 5 LEDs
#define PIN_LED1 13
#define PIN_LED2 12
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
bool led3State = false;  // Asegúrate de que todas las variables de estado de LED están declaradas
bool led4State = false;
bool led5State = false;
bool flameSensor;
bool fire = false;
bool sismo = false;
bool movimientoState = false;  // Estado actual del sensor de movimiento
bool lastMovimientoState = false;  // Estado anterior del sensor de movimiento
float lastHumedadPorciento = 0.0; 
bool servoOpened = false;

String serverMessage = "";  // Inicializa la variable para los mensajes del servidor
char delimitador = '_';

void setup() {
  // Inicia la comunicación serial y configura los pines de los LEDs como salida
  Serial.begin(9600);
  pinMode(PIN_LED1, OUTPUT);
  pinMode(PIN_LED2, OUTPUT);
  pinMode(PIN_LED3, OUTPUT);
  pinMode(PIN_LED4, OUTPUT);
  pinMode(PIN_LED5, OUTPUT);
  pinMode(PIN_LLAMA, INPUT);
  pinMode(PIN_MOVIMIENTO, INPUT);
  myServo.attach(SERVO_PIN);
  myServo.write(servoPos);
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

  float h = dht.readHumidity();
  if (isnan(h)) {
    Serial.println("Error al leer del sensor DHT!");
  } else {
    // Solo envía un mensaje si hay un cambio significativo en la humedad
    if (abs(h - lastHumedadPorciento) > 1.0) {  // Ajusta el valor de 1.0 según la sensibilidad deseada
      Serial.print("Humedad: ");
      Serial.print(h);
      Serial.println(" %");
      lastHumedadPorciento = h;  // Actualiza el último valor de humedad
    }
  }

  movimientoState = digitalRead(PIN_MOVIMIENTO); // Lee el valor del sensor de movimiento
  // Si hay un cambio en el estado del sensor de movimiento
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

  // Verifica si hay datos disponibles en el puerto serial
  if (Serial.available() > 0) {
    // Lee el mensaje enviado desde el servidor
    serverMessage = Serial.readStringUntil('\n');  // Lee hasta que encuentre un salto de línea

    // Compara el mensaje recibido con las acciones esperadas para cada LED
    if (serverMessage.equals("LED1")) {
      led1State = !led1State;  // Cambia el estado del LED 1
      digitalWrite(PIN_LED1, led1State ? HIGH : LOW);  // Enciende o apaga el LED 1
    } else if (serverMessage.equals("LED2")) {
      led2State = !led2State;  // Cambia el estado del LED 2
      digitalWrite(PIN_LED2, led2State ? HIGH : LOW);  // Enciende o apaga el LED 2
    } else if (serverMessage.equals("LED3")) {
      led3State = !led3State;  // Cambia el estado del LED 3
      digitalWrite(PIN_LED3, led3State ? HIGH : LOW);  // Enciende o apaga el LED 3
    } else if (serverMessage.equals("LED4")) {
      led4State = !led4State;  // Cambia el estado del LED 4
      digitalWrite(PIN_LED4, led4State ? HIGH : LOW);  // Enciende o apaga el LED 4
    } else if (serverMessage.equals("LED5")) {
      led5State = !led5State;  // Cambia el estado del LED 5
      digitalWrite(PIN_LED5, led5State ? HIGH : LOW);  // Enciende o apaga el LED 5
    } else if (serverMessage.equals("puerta")) {
      // Convierte el mensaje a un valor entero y mueve el servo a esa posición
      if (servoOpened) {
        for (servoPos = 270; servoPos >= 0; servoPos--) { // Cambié 180 por 270
          myServo.write(servoPos);
          delay(15);
        }
        servoOpened = false;  // Actualiza el estado a cerrado
      } else {
        for (servoPos = 0; servoPos <= 360; servoPos++) { // Cambié 180 por 270
          myServo.write(servoPos);
          delay(15);
        }
        servoOpened = true;  // Actualiza el estado a abierto
      }

    }
  }
}
