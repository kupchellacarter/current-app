import can

bus = can.interface.Bus(channel='can0', bustype='socketcan')

# Send OBDII request for Pack Voltage (PID 0x22dd83)
request = can.Message(arbitration_id=0x7DF,  # OBDII broadcast address
                      data=[0x02, 0x22, 0xDD, 0x83, 0x00, 0x00, 0x00, 0x00],
                      is_extended_id=False)

print("Sending OBDII request for Pack Voltage...")
bus.send(request)

# Listen for the response
while True:
    response = bus.recv(timeout=1.0)
    if response and response.arbitration_id == 0x7E8:
        print("Received OBDII Response:", response.data)
        break




