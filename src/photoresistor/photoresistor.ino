const int pResistor = A0; // Photoresistor at Arduino analog pin A0

int value; // Store value from photoresistor (0-1023)
int count = 0; // to time the next squares flash
int latency = 0;
unsigned long StartTime = millis();
int waiting_for_black = 1;

void setup() {
    pinMode(pResistor, INPUT); // Set pResistor - A0 pin as an input (optional)
    Serial.begin(9600);
}

void loop(){
    value = analogRead(pResistor);
    
    //  Serial.println(analogRead(A0)); // print photoresistor value
    Serial.println(latency);
    
    if (count == 300) {
      Serial.println("w"); // send signal to pc to flash white squares
      StartTime = millis(); // start countdown
      waiting_for_black = 0;
    }
    
    if (value > 200){ // if photoresistor detects the white squares
        if (waiting_for_black == 0) {
            count = 0; // stop countdown
            latency = millis() - StartTime;
        }
        else {
            waiting_for_black = 1;
        }
    }
    count += 1;
    delay(1); //Small delay
}
