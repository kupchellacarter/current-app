import can
import time

# Set up the CAN interface (replace 'can0' with the correct interface if needed)
bus = can.interface.Bus(channel='can0', bustype='socketcan')

# OBD-II request message (0x7DF 0x02 0x01 0x1F)
request_message = can.Message(arbitration_id=0x7DF, data=[0x02, 0x01, 0x1F], is_extended_id=False)

# Send the request message
try:
    bus.send(request_message)
    print("OBD-II request sent successfully.")
except can.CanError:
    print("Error sending OBD-II request.")

# Now listen for the response from the MCU (0x7E8)
print("Waiting for response from MCU...")

# Set the timeout for waiting for a response (e.g., 1 second)
timeout = 1.0
start_time = time.time()

while time.time() - start_time < timeout:
    message = bus.recv(timeout=timeout)  # Wait for a message with a timeout

    if message:
        # Check if the message ID is the expected MCU response (0x7E8)
        if message.arbitration_id == 0x7E8:
            print(f"Received response: {message.data}")

            # Decode the response (expecting a runtime value at PID 0x1F)
            if len(message.data) > 3:
                runtime = (message.data[2] << 8) | message.data[3]
                print(f"Runtime data (in seconds): {runtime}")
            else:
                print("Invalid response length.")
            break
else:
    print("No response received from MCU within the timeout.")
