
// These constants won't change.  They're used to give names
// to the pins used:

int value = 0;


void setup() {
  // initialize serial communications at 9600 bps:
  Serial.begin(9600); 
}

void JSONsender( int value ){
  Serial.println( "{ \"sensor\" : " + String(value, DEC) +" }");
}
// serialEvent



void loop() {
  
  int sensor = analogRead(A0);
  if( abs(value-sensor) > 9 ){
    value = sensor;
    JSONsender( value );
  }
}
