# input_lag_test v0.3 2020-03-29
Measures the input lag of a display in milliseconds through the serial port in Arduino Uno and a photoresistor. 
How this measuring tool works:
1) The arduino sends a trigger through the serial interface to a pyhton program running on the computer and starts counting in ms, the program draws a white square under the sensor changing the area from black to white and back to black.
2) The Arduino program waits until the resistor detects a significant increase in brightness and stops the timer, giving the latency
3) The arduino sends the ms latency value through serial, the python program .
4) These steps repeat for at least 10 times to get an accurate measurement.

![Arduino view](https://github.com/ArtDor2/display_lag_tester/blob/master/images/IMG_20200329_175024.jpg)
![Arduino view 2](https://github.com/ArtDor2/display_lag_tester/blob/master/images/IMG_20200329_174912.jpg)
![test demo](https://github.com/ArtDor2/display_lag_tester/blob/master/images/test%20demo.png)

TO-DO:
- [x] Add diagram of the aruino curcuit, a screenshot of the program, and a photo of both the program and the arduino running the test.
- [x] Record the data of the measured latency coming from the arduino ty python dictionary
- [x] show min max ms
- [ ] save data to file
- [x] Dont count the first few measurements due to starting the python program.
- [ ] Reduce the latency of the Arduino sending serial data to the Python program (current added latency is about 70ms)
- [ ] Calibrate measuring latency by getting +0ms min and +16ms max using a CRT monitor and subtracting that value from the measured to get a much more accurate latency value.
- [ ] Make an alternate version with a pressure resistor to test other devices such as an Android phone.
