// Definir los pines para los 5 LEDs
#define PIN_LED1 13
#define PIN_LED2 12
#define PIN_LED3 11
#define PIN_LED4 9
#define PIN_LED5 8

// Variables para almacenar el estado de cada LED
bool led1State = false;
bool led2State = false;
bool led3State = false;
bool led4State = false;
bool led5State = false;

String serverMessage = "";  // Inicializa la variable para los mensajes del servidor

void setup() {
  // Inicia la comunicación serial y configura los pines de los LEDs como salida
  Serial.begin(9600);
  pinMode(PIN_LED1, OUTPUT);
  pinMode(PIN_LED2, OUTPUT);
  pinMode(PIN_LED3, OUTPUT);
  pinMode(PIN_LED4, OUTPUT);
  pinMode(PIN_LED5, OUTPUT);
}

void loop() {
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
    }
  }
}
