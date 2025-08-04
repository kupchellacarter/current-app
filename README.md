# current-app
This app is designed to be used to control a display in an Electric boat built by Carter and Al Kupchella.

Hardware:
Raspberry Pi 4B running PiOS,
7" official raspberry pi touchscreen, 
RS485 CAN hat for RPi, 
Dilithium Designs Master COntrol Unit (MCU) and satellite BMS unit) https://www.thunderstruck-ev.com/mcu.html?gad_source=1&gclid=Cj0KCQjwhMq-BhCFARIsAGvo0KdYqkYh-IWQe-ew9kLD75TUN-v8WSUi304nF8HaUrn4qdpTNPfFqkgaAmCJEALw_wcB , 
15.5kWh LiFePo4 battery pack: 16S 310AH EVE cells.

This program interfaces over CAN with an off the shelf battery control unit from Thuderstruck Motors.  Software will parse the CAN Bus data and display it on a UI on the raspberry pi screen. 

Newer or older pis would likely work, but the project is built on Python 3.11 which is the latest the RPi 4B appears to support at this time.

Future updates will include pushable buttons on touchscreen to set charging parameters, and a GPS integration for a speed readout.

Data transfer is handled by the MCU integrated CAN network, communcating via the J1939 protocol.  A DBC for this protocol is included in the DBC directory, and acts as a dictionary for J1939 can transmissions, translating hex transmissions over the interface into human readable parameters and values.  



