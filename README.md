# current-app
This app is designed to be used with the boat that Carter and Al built <3
This program will parse the CAN Bus data and display it on a UI on the raspberry pi screen. 
Carter & Jillian 4eva <3


Project is designed for a Raspberry pi 4 B running with a 7" oficial raspberry pi touchscreen as a user interface for an electric boat project. newer or older pis would likely work, but the project is built on Python 3.11 which is the lates the RPi 4B can support at this time.

Main interface is with the Thunderstruck MCU: https://www.thunderstruck-ev.com/mcu.html?gad_source=1&gclid=Cj0KCQjwhMq-BhCFARIsAGvo0KdYqkYh-IWQe-ew9kLD75TUN-v8WSUi304nF8HaUrn4qdpTNPfFqkgaAmCJEALw_wcB

This project essentially replicates the official thunderstruck display, but with more customizability.

Data transfer is handled by the MCU integrated CAN network, communcating via the J1939 protocol.  A DBC for this protocol is included in the DBC directory, and acts as a dictionary for J1939 can transmissions, translating hex transmissions over the interface into human readable parameters and values.  

ALso required is a CAN hat for the raspberry pi.

