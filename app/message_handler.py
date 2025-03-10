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

    def request_factory(self, metric: str):
        """Returns the appropriate request message for the given metric."""
        if metric == "runtime":
            return self._runtime_request
        elif metric == "voltage":
            return self._voltage_request
        else:
            raise ValueError(f"Invalid metric: {metric}")

    def request_and_parse(self, metric: str) -> int:
        """Reads the CAN bus."""
        # Send the request message
        request = self.request_factory(metric)
        print(request)
        try:
            self.bus.send(request)
        except can.CanError as e:
            self.errors.append(f"Error: {e}")

        timeout = 1
        start_time = time.time()

        while time.time() - start_time < timeout:
            message = self.bus.recv(timeout=timeout)
            if message and len(message.data) > 3:
                if metric == "runtime":
                    runtime = (message.data[2] << 8) | message.data[3]
                    print(runtime)
                    print(message.data)
                    self.data.runtime = runtime
                    return
                elif metric == "voltage":
                    print("checking voltage")
                    print(message.data)
                    high_byte = message.data[3]
                    low_byte = message.data[4]
                    print(f"high_byte: {high_byte}")
                    print(f"low_byte: {low_byte}")
                    voltage = (high_byte * 256 + low_byte) / 10.0
                    print(f"Voltage: {voltage} V")
                    self.data.voltage = voltage
                    return
                else:
                    logger.error("Invalid response length.")
                    self.errors.append("Invalid response length.")
                    break
        else:
            logger.error("No response received from MCU within the timeout.")
            self.errors.append("No response received from MCU within the timeout.")

    def get_runtime_data(self) -> str:
        """Returns the runtime data formatted as a string in the format HH:MM:SS.
        return: str
        """
        return time.strftime("%H:%M:%S", time.gmtime(self.data.runtime))

    def get_voltage(self) -> str:
        """Returns the runtime data formatted as a string in the format HH:MM:SS.
        return: str
        """
        return self.data.voltage

    def get_errors(self) -> list:
        """Returns a list of errors encountered during operation."""
        return self.errors


if __name__ == "__main__":
    handler = MessageHandler()
    handler.request_and_parse("voltage")
