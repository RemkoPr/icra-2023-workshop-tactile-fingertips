# SensorComm

Package allowing communication with IRTouch infrared tactile fingertips, read out using an Arduino nano 33 BLE via Bluetooth Low Energy.

Install using 
```
pip install -e path-to-package-root
```

You may need to install the [TKinter](https://riptutorial.com/tkinter/example/3206/installation-or-setup) module separately. It might be pre-installed, but only for Python2, so make sure it is installed for Python3.
## Note
There's an issue where, if the BLE data characteristic UUID is changed in the Arduino code of the sensor, the Python side may not realize this, requiring you to use the old UUID.
