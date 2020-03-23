# display_lag_tester
Measures the input lag of a display in milliseconds through the serial port in Arduino Uno and a photoresistor. 
How this measuring tool works:
1) The arduino sends a trigger through the serial interface to a pyhton program running on the computer and starts counting in ms, the program draws a white square under the sensor changing the area from black to white and back to black.
2) The Arduino program waits until the resistor detects a significant increase in brightness and stops the timer, giving the latency
3) The arduino sends the ms latency value through serial, the python program .
4) These steps repeat for at least 10 times to get an accurate measurement.



TO-DO:
- [ ] Add diagram of the aruino curcuit, a screenshot of the program, and a photo of both the program and the arduino running the test.
- [ ] Record the data of the measured latency coming from the arduino
- [ ] Dont count the first few measurements due to starting the python program.
- [ ] Reduce the latency of the Arduino sending serial data to the Python program (current added latency is about 80ms)
- [ ] Calibrate measuring latency by getting +0ms min and +16ms max using a CRT monitor and subtracting that value from the measured to get a much more accurate latency value.
