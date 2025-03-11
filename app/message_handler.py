import can
import time
import logging
import cantools
from dataclass import CanData

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

DBC_FILE = "./app/DBC/MCU_J1939_v1-1-2_BETA.dbc"


class MessageHandler:
    """Handler"""

    def __init__(self):
        self.bus = None
        self.system_errors = {}
        self.errors = {}
        self.bus = can.interface.Bus(channel="can0", bustype="socketcan")
        self.db = cantools.database.load_file(DBC_FILE)
        self.data = CanData()

    def request_and_parse(self, target_pgn, b7=0x00):
        """Sends a J1939 read request for a specific PGN and decodes the response."""
        # Send a request message for the PGN (Parameter Group Number)
        request = can.Message(
            arbitration_id=0x14EBD0D8,  # J1939 Read Request for MCU
            data=[
                (target_pgn & 0xFF),  # PGN (little-endian)
                (target_pgn >> 8) & 0xFF,
                (target_pgn >> 16) & 0xFF,
                0x00,  # Rate (ignored)
                0x00,  # Repeat (ignored)
                0x00,  # B4 (reserved)
                0x00,  # B5 (reserved)
                b7,  # B7: Selects message type (MCUSUM, PACKSUM, etc.)
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

        timeout = 2  # Wait for up to 2 seconds
        start_time = time.time()

        while time.time() - start_time < timeout:
            message = self.bus.recv(timeout=timeout)
            if message and (message.arbitration_id & 0x1FFFF00) >> 8 == target_pgn:
                try:
                    decoded = self.db.decode_message(
                        message.arbitration_id, message.data
                    )
                    logger.info(f"Decoded message: {decoded}")
                    self.update_data(decoded)
                    return decoded
                except Exception as e:
                    logger.error(f"Failed to decode: {e}")
                    self.errors.append(str(e))
                    return

        logger.error(f"No response for PGN: {hex(target_pgn)}")
        self.errors.append(f"No response for PGN: {hex(target_pgn)}")

    def update_data(self, decoded_message):
        """Update CanData object with decoded values."""
        if "Voltage" in decoded_message:
            self.data.voltage = decoded_message["Voltage"]
        if "StateOfCharge" in decoded_message:
            self.data.soc = decoded_message["StateOfCharge"]
        if "Runtime" in decoded_message:
            self.data.runtime = decoded_message["Runtime"]

    def get_voltage(self):
        return self.data.voltage

    def get_soc(self):
        return self.data.soc

    def get_runtime(self):
        return time.strftime("%H:%M:%S", time.gmtime(self.data.runtime))

    def get_errors(self):
        return self.errors

    @property
    def voltage(self):
        return self.data.voltage

    @property
    def soc(self):
        return self.data.soc

    @property
    def runtime(self):
        return time.strftime("%H:%M:%S", time.gmtime(self.data.runtime))

    @property
    def get_errors(self):
        return self.errors


if __name__ == "__main__":
    handler = MessageHandler()
    handler.request_and_parse(0x00)
    # handler.request_and_parse("runtime")
    print("Voltage:", handler.voltage)
    print("SOC:", handler.soc)
    print("Runtime:", handler.runtime)
    print("Errors:", handler.get_errors)
