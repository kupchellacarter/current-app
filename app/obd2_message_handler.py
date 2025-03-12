import can
import time
import logging
from dataclass import CanData

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class OBD2MessageHandler:
    """Handler"""

    def __init__(self, can_data: CanData = CanData()):
        self.system_errors = []
        self.errors = []
        self.data = can_data
        self.bus = can.interface.Bus(channel="can0", interface="socketcan")

    @property
    def _runtime_request(self):
        return can.Message(
            arbitration_id=0x7DF, data=[0x02, 0x01, 0x1F], is_extended_id=False
        )

    def request_factory(self, metric: str):
        """Returns the appropriate request message for the given metric."""
        if metric == "runtime":
            return self._runtime_request
        else:
            raise ValueError(f"Invalid metric: {metric}")

    def obd2_request_and_parse(self, metric: str) -> int:
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
                    self.data.runtime = time.strftime("%H:%M:%S", time.gmtime(runtime))
                    return self.data
                else:
                    logger.error("Invalid response length.")
                    self.errors.append("Invalid response length.")
                    break
        else:
            logger.error("No response received from MCU within the timeout.")
            self.errors.append("No response received from MCU within the timeout.")


if __name__ == "__main__":
    handler = OBD2MessageHandler()
    handler.obd2_request_and_parse("runtime")
