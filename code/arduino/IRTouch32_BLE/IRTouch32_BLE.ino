/*  
 *  BEFORE FLASHING A PCB: 
 *  Make sure PCB_NAME is correct.
 */

#include <ArduinoBLE.h>
#include "IRTouch32.h"

#define SERIAL    false

#define PCB_NAME "IRTouch"
#define BLE_UUID_DATA_SERV      "ECBC" //16b UUIDs needed for compatibility with Blatann lib (python)
#define BLE_UUID_DATA_CHAR      "C134"

using namespace std;

BLEService dataService( BLE_UUID_DATA_SERV );
BLECharacteristic dataCharacteristic( BLE_UUID_DATA_CHAR, BLERead | BLENotify, NUM_DATA_VALUES, true );

uint8_t data[NUM_DATA_VALUES];

void setup() {
  for( int i = 0 ; i < 4 ; i++ ) {
    pinMode(read_pins[i], INPUT);
  }

  pinMode(MUX_IRTOUCH32_S0, OUTPUT);
  pinMode(MUX_IRTOUCH32_S1, OUTPUT);
  pinMode(MUX_IRTOUCH32_S2, OUTPUT);
  setupBleMode();
  if( SERIAL ) {
    Serial.begin(9600);
    while(!Serial);
    Serial.println("Setup complete");
  }
}

void loop() {
  BLEDevice central = BLE.central();
  if ( central ) {
    while ( central.connected() ) {
      if( central.rssi() != 0 ) {        
        readData();
        if( SERIAL ) { printData(); }
        dataCharacteristic.writeValue(data, NUM_DATA_VALUES);
      }
    }
  }
}

//=================== FUNCTIONS =====================\\

void readData() {
  for(int i = 0 ; i < NUM_DATA_VALUES/NUM_MUXS  ; i++ ) {
    selectIRTouchMuxOut(i);
    for(int analog_pin_idx = 0 ; analog_pin_idx < NUM_MUXS ; analog_pin_idx++ ) {
      data[measure_idx_to_grid_idx[i*NUM_MUXS + analog_pin_idx]] = analogRead(read_pins[analog_pin_idx])/4.0; // Normalisation to go from 10 bit to 8 bit
      //Serial.println(measure_idx_to_grid_idx[i*NUM_MUXS + analog_pin_idx]);
    }
  }
}

void printData() {
  Serial.println("");
  for(int i = 0 ; i < NUM_DATA_VALUES ; i++ ) {
    Serial.print(String(data[i]) + String(" "));
  }
}

bool setupBleMode() {
  if ( !BLE.begin() ) {
    return false;
  }

  // set advertised local name and service UUID:
  BLE.setDeviceName( PCB_NAME );
  BLE.setLocalName( PCB_NAME );
  
  BLE.setAdvertisedService( dataService );
  dataService.addCharacteristic( dataCharacteristic );
  BLE.addService( dataService );
  uint8_t zeros[NUM_DATA_VALUES] = {0};
  dataCharacteristic.writeValue( zeros, NUM_DATA_VALUES );
  
  BLE.advertise();

  return true;
}
