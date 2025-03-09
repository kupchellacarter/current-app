import can

# Set up the CAN interface (replace 'can0' with the correct interface if needed)
bus = can.interface.Bus(channel='can0', bustype='socketcan')

# OBD-II request message
message = can.Message(arbitration_id=0x7DF, data=[0x02, 0x01, 0x1F], is_extended_id=False)

# Send the message
try:
    bus.send(message)
    print("OBD-II request sent successfully.")
except can.CanError:
    print("Error sending OBD-II request.")