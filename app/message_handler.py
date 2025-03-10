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
        self.errors = []
        self.bus = can.interface.Bus(channel="can0", bustype="socketcan")
        self.data = CanData()

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
            self.bus.send(self._voltage_request)
            logger.info("OBD-II request sent successfully.")
        except can.CanError as e:
            logger.error("Error sending OBD-II request.")
            self.errors.append(f"Error: {e}")

        logger.info("Waiting for response from MCU...")
        timeout = 1
        start_time = time.time()

        while time.time() - start_time < timeout:
            message = self.bus.recv(timeout=timeout)

            # if message:
            #     if len(message.data) > 3:
            #         runtime = (message.data[2] << 8) | message.data[3]
            #         print(runtime)
            #         print(message.data)
            #         return runtime
            if (
                len(message.data) > 3 and message.data[2] == 0x42
            ):  # Check for voltage PID
                # Extract the high byte (message.data[3]) and low byte (message.data[4])
                high_byte = message.data[3]
                low_byte = message.data[4]

                # Decode the voltage: (High Byte * 256 + Low Byte) / 10
                voltage = (high_byte * 256 + low_byte) / 10.0
                print(f"Voltage: {voltage} V")
                return voltage
            else:
                logger.error("Invalid response length.")
                self.errors.append("Invalid response length.")
                break
        else:
            logger.error("No response received from MCU within the timeout.")
            self.errors.append("No response received from MCU within the timeout.")

    def request_runtime_data(self):
        """Requests runtime data if CAN data is streaming."""
        runtime = self._can_request_and_parse()
        # self.data.runtime = runtime
        self.data.voltage = runtime

    def get_runtime_data(self) -> str:
        """Returns the runtime data formatted as a string in the format HH:MM:SS.
        return: str
        """
        # return time.strftime("%H:%M:%S", time.gmtime(self.data.runtime))
        return self.data.voltage

    def get_errors(self) -> list:
        """Returns a list of errors encountered during operation."""
        return self.errors
