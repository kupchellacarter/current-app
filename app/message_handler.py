import can
import struct
import time
import logging
from dataclass import CanData

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")


class MessageHandler:
    """Handler"""

    def __init__(self):
        # Set up the CAN interface (replace 'can0' with the correct interface if needed)
        self.bus = None
        self.can_connected = True
        try:
            self.bus = can.interface.Bus(channel="can0", bustype="socketcan")
        except:
            self.can_connected = False
            logger.error("CAN bus not connected")
        self.data = CanData()
        self.start_time = time.time()

    def _format_seconds(self, seconds: int) -> str:
        """docstring"""
        return time.strftime("%H:%M:%S", time.gmtime(seconds))

    def request_runtime_data(self):
        if self.can_connected:
            # OBD-II request message (0x7DF 0x02 0x01 0x1F)
            request_message = can.Message(
                arbitration_id=0x7DF, data=[0x02, 0x01, 0x1F], is_extended_id=False
            )
            # Send the request message
            try:
                self.bus.send(request_message)
                logger.info("OBD-II request sent successfully.")
            except can.CanError:
                logger.error("Error sending OBD-II request.")

            # Now listen for the response from the MCU (0x7E8)
            logger.info("Waiting for response from MCU...")

            # Set the timeout for waiting for a response (e.g., 1 second)
            timeout = 1.0
            start_time = time.time()

            while time.time() - start_time < timeout:
                message = self.bus.recv(
                    timeout=timeout
                )  # Wait for a message with a timeout

                if message:
                    # Check if the message ID is the expected MCU response (0x7E8)
                    if message.arbitration_id == 0x7E8:
                        logger.info(f"Received response: {message.data}")

                        # Decode the response (expecting a runtime value at PID 0x1F)
                        if len(message.data) > 3:
                            runtime = (message.data[2] << 8) | message.data[3]
                            self.set_runtime_data(runtime)
                        else:
                            logger.error("Invalid response length.")
                        break
            else:
                logger.warning("No response received from MCU within the timeout.")
        else:
            elapsed = int(time.time() - self.start_time)
            self.set_runtime_data(elapsed)

    def set_runtime_data(self, runtime: int):
        self.data.runtime = runtime

    def get_runtime_data(self) -> int:
        """docstring"""
        return self._format_seconds(self.data.runtime)
