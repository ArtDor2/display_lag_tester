// uses pressure sensor to start countdown

const int pPressure = A0; // Photoresistor at Arduino analog pin A0
const int pLight = A1;

int value; // Store value from photoresistor (0-1023)
int count = 1; // to time the next squares flash
int latency = 0;
unsigned long StartTime = millis();
int waiting_for_black = 1;
int value_pressure;
int value_light;
int timer = 0;
bool send_now = false;

void setup() {
    pinMode(pPressure, INPUT);
    pinMode(pLight, INPUT);
    Serial.begin(9600);
}

void loop(){
    value_pressure = analogRead(pPressure);
    value_light = analogRead(pLight);

//    Serial.print("pressure: "); Serial.print(value_pressure); Serial.print("  ");
//    Serial.print("light: "); Serial.print(value_light); Serial.print("  ");
//    Serial.println("uT");

    if (value_light > 50){ // if photoresistor detects the white squares
        if (waiting_for_black == 0) {
            latency = millis() - StartTime;
            send_now = true;
        }
        else {
            waiting_for_black = 1;
        }
    }

    // pressure mouseclick version:
    if (value_pressure > 20) { // every 200ms send signal to draw squares
//        Serial.println("f"); // f = signal to pc to flash white squares
        StartTime = millis(); // start countdown
        waiting_for_black = 0;
    } else {
        if (send_now == true) {
            Serial.println(latency);
            send_now = false;
        } else {
            Serial.println("w"); // w = signal to wait for flash signal
        }
    }
//        timer += 1;

//    if (timer < 200) { // every 200ms send signal to draw squares
//        if (send_now == true) {
//            Serial.println(latency);
//            send_now = false;
//        } else {
//            Serial.println("w"); // w = signal to wait for flash signal
//        }
////        timer += 1;
//    } else {
//        Serial.println("f"); // f = signal to pc to flash white squares
//        timer = 0;
//        StartTime = millis(); // start countdown
//        waiting_for_black = 0;
//    }

    delay(1); //1ms delay
}
