// Definir los pines para los 5 LEDs
#define PIN_LED1 13
#define PIN_LED2 12
#define PIN_LED3 11
#define PIN_LED4 9
#define PIN_LED5 8
#define PIN_LLAMA 7
#define PIN_HUMEDAD A0
#define PIN_MOVIMIENTO 6

// Variables para almacenar el estado de cada LED
bool led1State = false;
bool led2State = false;
bool led3State = false;
bool led4State = false;
bool led5State = false;
bool flameSensor;
bool fire = false;
bool movimientoState = false;  // Estado actual del sensor de movimiento
bool lastMovimientoState = false;  // Estado anterior del sensor de movimiento
float lastHumedadPorciento = 0.0;  // Último valor de humedad

String serverMessage = "";  // Inicializa la variable para los mensajes del servidor

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
}

void loop() {
  flameSensor = digitalRead(PIN_LLAMA);
  if (flameSensor && !fire) {
    Serial.write("Llama detectada\n");
    fire = true;
  }
  if (!flameSensor && fire) {
    Serial.write("Llama apagada\n");
    fire = false;
  }

  int humedadValue = analogRead(PIN_HUMEDAD);  // Lee el valor analógico del sensor de humedad
  float humedadPorciento = (humedadValue / 10.23);

  // Solo envía un mensaje si hay un cambio significativo en la humedad
  if (abs(humedadPorciento - lastHumedadPorciento) > 1.0) {  // Ajusta el valor de 1.0 según la sensibilidad deseada
    Serial.println(String(humedadPorciento) + "%");
    lastHumedadPorciento = humedadPorciento;  // Actualiza el último valor de humedad
  }

  movimientoState = digitalRead(PIN_MOVIMIENTO); // Lee el valor del sensor de movimiento
  if (movimientoState != lastMovimientoState) { // Si hay un cambio en el estado del sensor de movimiento
    if (movimientoState == HIGH) { // Si se detecta movimiento
      Serial.println("Movimiento detectado!");
    } else {
      Serial.println("Sin movimiento.");
    }
    lastMovimientoState = movimientoState; // Actualiza el estado anterior
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
    }
  }
  delay(200);
}
