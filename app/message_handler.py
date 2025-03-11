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


class MessageHandler:
    """Handler"""

    def __init__(self):
        self.system_errors = []
        self.errors = []
        self.bus = can.interface.Bus(channel="can0", bustype="socketcan")
        self.db = cantools.database.load_file(DBC_FILE)
        self.data = CanData()

    def request_and_parse(
        self, target_pgn, request_rate=0x00, repeat_count=0x00, b7=0x00
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
                msg = self.db.get_message_by_frame_id(
                    0x14FF20D0
                )  # I CHANGED THIS TO CALL mcu_SUM, DISCREPANCY IN PRIORITY TO dbc
                decoded = msg.decode(message_data)
                logger.info(f"Decoded message: {decoded}")
                self.update_data(decoded)
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
            if message and (message.arbitration_id & 0x1FFFF00) >> 8 == target_pgn:
                return message
        return None

    def update_data(self, decoded):
        """Update CanData with any recognized fields."""
        for field, value in decoded.items():
            # Normalize field names to match CanData attributes (e.g., MCU_PackVoltage -> pack_voltage)
            normalized_field = field.lower()
            if hasattr(self.data, normalized_field):
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

    @property
    def pack_voltage(self):
        return self.data.pack_voltage

    @property
    def pack_current(self):
        return self.data.pack_current

    @property
    def charged_energy(self):
        return self.data.charged_energy

    @property
    def charge_state(self):
        return self.data.charge_state

    @property
    def plug_state(self):
        return self.data.plug_state

    def get_errors(self):
        return self.errors


if __name__ == "__main__":
    handler = MessageHandler()

    # Request MCU Summary (0xFF20D0)
    handler.request_and_parse(0xFF20)

    print("Charged Energy:", handler.charged_energy)
    print("Charge State:", handler.charge_state)
    print("Plug State:", handler.plug_state)
    print("Errors:", handler.get_errors())

    # Request MCU Pack Summary (0xFF20E0)
    # handler.request_and_parse(0xFF20)
    # print("Pack Voltage:", handler.pack_voltage)
    # print("Pack Current:", handler.pack_current)
