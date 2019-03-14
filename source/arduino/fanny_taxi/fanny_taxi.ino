/***
 * Fanny Taxi
 * 
 * Programma per il controllo del movimento delle ruote 
 * del braccio robotico Fanny
 * 
 * Casa Corsini Fablab 2019
 */

#define M1PLUS 2
#define M1MINUS 3
#define M2PLUS 4
#define M2MINUS 5
#define M3PLUS 6
#define M3MINUS 7
#define M4PLUS 8
#define M4MINUS 9

#define CONTROL_FWD 0
#define CONTROL_BWD 1

#define STOP 0
#define AVANTI 1
#define INDIETRO 2
byte stato_moto = STOP;
byte nuovo_stato = STOP;

void setup() {

  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(M1PLUS, OUTPUT);
  pinMode(M1MINUS, OUTPUT);
  pinMode(M2PLUS, OUTPUT);
  pinMode(M2MINUS, OUTPUT);
  pinMode(M3PLUS, OUTPUT);
  pinMode(M3MINUS, OUTPUT);
  pinMode(M4PLUS, OUTPUT);
  pinMode(M4MINUS, OUTPUT);

  pinMode(CONTROL_FWD, INPUT);
  pinMode(CONTROL_BWD, INPUT);
  //parte da fermo
  attua_stato(STOP);
}

void loop() {
  leggi_comando();
  if (nuovo_stato != stato_moto) {
    stato_moto = nuovo_stato;
    attua_stato(stato_moto);
  }
  delay(750);
}

/**
 * Traduce lo stato del moto in comandi verso i relé
 */
void attua_stato(byte st)
{
  //Nota: comando relé attivo BASSO
  byte lplus = HIGH;
  byte lminus = HIGH;
  switch(st) {
    case STOP:
      digitalWrite(LED_BUILTIN, HIGH);      
      break;
    case AVANTI:
      lplus = LOW;
      digitalWrite(LED_BUILTIN, LOW);
      break;
    case INDIETRO:
      lminus = LOW;
      digitalWrite(LED_BUILTIN, LOW);
      break;
  }
  //Applica i livelli ai relé
  digitalWrite(M1PLUS, lplus);
  digitalWrite(M1MINUS, lminus);
  digitalWrite(M2PLUS, lplus);
  digitalWrite(M2MINUS, lminus);
  digitalWrite(M3PLUS, lplus);
  digitalWrite(M3MINUS, lminus);
  digitalWrite(M4PLUS, lplus);
  digitalWrite(M4MINUS, lminus);
}

/**
 * Legge i livelli di comando provenienti dalla RPi
 */
void leggi_comando(void)
{
  byte cfwd = digitalRead(CONTROL_FWD);
  byte cbwd = digitalRead(CONTROL_BWD);

  //Nota: questo caso comprende anche il caso ALTO-ALTO
  if (cfwd == LOW) {
    nuovo_stato = AVANTI;
    return;
  }

  if (cbwd == LOW) {
    nuovo_stato = INDIETRO;
    return;
  }

  nuovo_stato = STOP;
}

