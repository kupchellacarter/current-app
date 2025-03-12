import can
import time
import logging
from dataclass import CanData

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class OBD2MessageHandler:
    """Handler"""

    def __init__(self, can_data: CanData):
        self.system_errors = {}
        self.errors = {}
        self.bus = can.interface.Bus(channel="can0", bustype="socketcan")
        self.data = can_data

    @property
    def _voltage_request(self):
        return can.Message(
            arbitration_id=0x7DF,
            data=[0x03, 0x22, 0xDD, 0x83],
            is_extended_id=False,
        )

    @property
    def _runtime_request(self):
        return can.Message(
            arbitration_id=0x7DF, data=[0x02, 0x01, 0x1F], is_extended_id=False
        )

    @property
    def _soc_request(self):
        return can.Message(
            arbitration_id=0x7DF, data=[0x03, 0x22, 0xDD, 0x85], is_extended_id=False
        )

    def request_factory(self, metric: str):
        """Returns the appropriate request message for the given metric."""
        if metric == "runtime":
            return self._runtime_request
        elif metric == "voltage":
            return self._voltage_request
        elif metric == "soc":
            return self._soc_request
        else:
            raise ValueError(f"Invalid metric: {metric}")

    def request_and_parse(self, metric: str) -> int:
        """Reads the CAN bus."""
        # Send the request message
        request = self.request_factory(metric)
        try:
            self.bus.send(request)
        except can.CanError as e:
            self.errors.append(f"Error: {e}")

        timeout = 1
        start_time = time.time()

        while time.time() - start_time < timeout:
            message = self.bus.recv(timeout=timeout)
            if message and message.arbitration_id == 0x7E8:
                if metric == "runtime" and len(message.data) >= 5:
                    runtime_low_byte = message.data[3]
                    runtime_high_byte = message.data[4]
                    runtime = (runtime_high_byte << 8) | runtime_low_byte
                    self.data.runtime = runtime
                    return
                elif metric == "voltage":
                    pid = (message.data[2] << 8) | message.data[
                        3
                    ]  # Combine B2 and B3 for PID (0xDD83)
                    if pid == 0xDD83:
                        # Extract the pack voltage from B4 (low byte) and B5 (high byte)
                        voltage_raw = (message.data[5] << 8) | message.data[4]

                        # Calculate the voltage (assuming it's in the format voltage = voltage_raw / 10)
                        voltage = voltage_raw / 10.0  # Convert the raw value to voltage
                        self.data.voltage = voltage
                        return
                    else:
                        pass
                elif metric == "soc":
                    pid = (message.data[2] << 8) | message.data[
                        3
                    ]  # Combine B2 and B3 for PID (0xDD83)
                    if pid == 0xDD85:
                        # Extract the pack soc from B4 (low byte) and B5 (high byte)
                        soc = (message.data[5] << 8) | message.data[4]
                        self.data.soc = soc
                        return
                    else:
                        pass

                else:
                    logger.error("Invalid response length.")
                    self.errors.append("Invalid response length.")
                    break
        else:
            logger.error("No response received from MCU within the timeout.")
            self.errors.append("No response received from MCU within the timeout.")

    def get_runtime(self) -> str:
        """Returns the runtime data formatted as a string in the format HH:MM:SS.
        return: str
        """
        return time.strftime("%H:%M:%S", time.gmtime(self.data.runtime))

    def get_voltage(self) -> str:
        """Returns the runtime data formatted as a string in the format HH:MM:SS.
        return: str
        """
        return self.data.voltage

    def get_soc(self) -> str:
        """Returns the soc formatted as a string in the format xxx.
        return: str
        """
        return self.data.soc

    def get_errors(self) -> list:
        """Returns a list of errors encountered during operation."""
        return self.errors


if __name__ == "__main__":
    handler = OBD2MessageHandler()
    handler.request_and_parse("voltage")
    handler.request_and_parse("runtime")
