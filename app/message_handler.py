import can
import struct
import time
import logging
from dataclass import CanData

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")


class MessageHandler:
    """Handler"""

    def __init__(self):
        self.bus = None
        self.can_connected = True
        self.errors = []
        try:
            self.bus = can.interface.Bus(channel="can0", bustype="socketcan")
        except:
            self.can_connected = False
            self.errors.append("CAN bus not connected. Defualting to elapsed time.")
        self.data = CanData()
        self.start_time = time.time()

    @property
    def _voltage_request(self):
        return can.Message(
            arbitration_id=0x7DF,
            data=[0x02, 0x01, 0x42],
            is_extended_id=False,
        )

    @property
    def _runtime_request(self):
        return can.Message(
            arbitration_id=0x7DF, data=[0x02, 0x01, 0x1F], is_extended_id=False
        )

    def _can_request_and_parse(self) -> int:
        """Reads the CAN bus."""
        # Send the request message
        try:
            self.bus.send(self._runtime_request)
            logger.info("OBD-II request sent successfully.")
        except can.CanError as e:
            logger.error("Error sending OBD-II request.")
            self.errors.append(f"Error: {e}")

        logger.info("Waiting for response from MCU...")
        timeout = 1
        start_time = time.time()

        while time.time() - start_time < timeout:
            message = self.bus.recv(timeout=timeout)

            if message:
                # Check if the message ID is the expected MCU response (0x7E8)
                if message.arbitration_id == 0x7E8:
                    logger.info(f"Received response: {message.data}")

                    # Ensure the response is valid and corresponds to PID 0x1F
                    if len(message.data) > 4 and message.data[2] == 0x1F:
                        A = message.data[3]  # High byte
                        B = message.data[4]  # Low byte

                        # Convert to seconds
                        runtime = (A << 8) | B
                        logger.info(f"raw data: {message.data}")
                        logger.info(f"runtime in seconds: {runtime}")
                        print(runtime)
                        print(message.data)
                        return runtime
                    else:
                        logger.error("Invalid response length.")
                        self.errors.append("Invalid response length.")
                    break
        else:
            logger.error("No response received from MCU within the timeout.")
            self.errors.append("No response received from MCU within the timeout.")

    def request_runtime_data(self):
        """Requests runtime data if CAN data is streaming. If not, uses elapsed time."""
        if self.can_connected:
            runtime = self._can_request_and_parse()
        else:
            runtime = int(time.time() - self.start_time)
        self.set_runtime_data(runtime)

    def set_runtime_data(self, runtime: int):
        """Sets the runtime data."""
        self.data.runtime = runtime

    def get_runtime_data(self) -> str:
        """Returns the runtime data formatted as a string in the format HH:MM:SS.
        return: str
        """
        return time.strftime("%H:%M:%S", time.gmtime(self.data.runtime))

    def get_errors(self) -> list:
        """Returns a list of errors encountered during operation."""
        return self.errors
