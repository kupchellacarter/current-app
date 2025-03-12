import can
import time
import logging
import cantools
from dataclass import CanData
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

DBC_FILE = os.path.join(os.path.dirname(__file__), "DBC", "MCU_J1939_v1-1-2_BETA.dbc")
# DBC_FILE = "app\DBC\MCU_J1939_v1-1-2_BETA.dbc"
REQUEST_ID = 0x14EBD0D8  # J1939 request format


class OBD2MessageHandler:
    """Handler"""

    def __init__(self):
        self.system_errors = {}
        self.errors = {}
        self.bus = can.interface.Bus(channel="can0", bustype="socketcan")
        self.db = cantools.database.load_file(DBC_FILE)
        self.data = CanData()

    def request_and_parse(
        self, target_pgn, request_rate=0x0A, repeat_count=0x14, b7=0x00
    ):
        """Sends a J1939 read request decodes the response, PGN agnostic."""
        # Create the CAN request message
        request = can.Message(
            arbitration_id=REQUEST_ID,
            data=[
                (target_pgn & 0xFF),  # Byte 0 PGN LSB
                (target_pgn >> 8) & 0xFF,  # Byte 1 PGN MSB
                request_rate,  # How often to send (in MCU ticks, 50ms each)
                repeat_count,  # Number of responses (0xFF for continuous)
                0x00,
                0x00,  # Reserved bytes
                b7,  # Message type selector (0x00 request full data set)
            ],
            is_extended_id=True,
        )

        try:
            self.bus.send(request)
            logger.info(
                f"Read request sent for PGN: {hex(target_pgn)} with B7: {hex(b7)}"
            )
        except can.CanError as e:
            logger.error(f"CAN transmission error: {e}")
            self.errors.append(str(e))
            return

        message = self._wait_for_response(target_pgn)
        if message:
            try:
                message_data = message.data
                frame_id = (0x14 << 24) | (target_pgn << 8) | 0xD0
                msg = self.db.get_message_by_frame_id(frame_id)
                decoded = msg.decode(message_data)
                logger.info(f"Decoded message: {decoded}")
                self.update_data(decoded)
                print("Decoded Message:", decoded)
                return decoded
            except Exception as e:
                logger.error(f"Failed to decode: {e}")
                self.errors.append(str(e))
                return

        logger.error(f"No response for PGN: {hex(target_pgn)}")
        self.errors.append(f"No response for PGN: {hex(target_pgn)}")

    def _wait_for_response(self, target_pgn, timeout=2):
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

            setattr(self.data, normalized_field, value)

            # Collect fault information if present
            if "fault" in field.lower() and value:
                self.system_errors.append(field)

    # def get_voltage(self):
    #     return self.data.voltage

    # def get_soc(self):
    #     return self.data.soc

    # def get_runtime(self):
    #     return time.strftime("%H:%M:%S", time.gmtime(self.data.runtime))

    # def get_errors(self):
    #     return self.errors

    # @property
    # def voltage(self):
    #     return self.data.voltage

    # @property
    # def soc(self):
    #     return self.data.soc

    # @property
    # def runtime(self):
    #     return time.strftime("%H:%M:%S", time.gmtime(self.data.runtime))

    # @property
    # def get_errors(self):
    #     return self.errors

    # @property
    # def pack_voltage(self):
    #     return getself.data.pack_voltage

    # @property
    # def pack_current(self):
    #     return self.data.pack_current

    # @property
    # def charged_energy(self):
    #     return self.data.charged_energy

    # @property
    # def charge_state(self):
    #     return self.data.charge_state

    # @property
    # def plug_state(self):
    #     return self.data.plug_state

    # def get_errors(self):
    #     return self.errors


if __name__ == "__main__":
    handler = OBD2MessageHandler()
    handler.request_and_parse("voltage")
    handler.request_and_parse("runtime")
