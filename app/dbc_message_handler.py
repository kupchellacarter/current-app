import can
import time
import logging
import cantools
from dataclass import CanData, DBCRequest
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

DBC_FILE = os.path.join(os.path.dirname(__file__), "DBC", "MCU_J1939_v1-1-2_BETA.dbc")
REQUEST_ID = 0x14EBD0D8  # J1939 request format


class DBCMessageHandler:
    """Handler"""

    def __init__(self, can_data: CanData = CanData()):
        self.system_errors = []
        self.errors = []
        self.db = cantools.database.load_file(DBC_FILE)
        self.data = can_data
        self.dbc_request = DBCRequest()
        self.bus = None
        try:
            self.bus = can.interface.Bus(channel="can0", interface="socketcan")
        except Exception as e:
            logger.error(f"Failed to connect to CAN bus: {e}")
            self.errors.append(str(e))
            raise Exception("Failed to connect to CAN bus")

    def get_dbc_request(self, target_pgn):
        return can.Message(
            arbitration_id=REQUEST_ID,
            data=[
                (target_pgn & 0xFF),  # Byte 0 PGN LSB
                (target_pgn >> 8) & 0xFF,  # Byte 1 PGN MSB
                self.dbc_request.request_rate,  # How often to send (in MCU ticks, 50ms each)
                self.dbc_request.repeat_count,  # Number of responses (0xFF for continuous)
                0x00,
                0x00,  # Reserved bytes
                self.dbc_request.b7,  # Message type selector (0x00 request full data set)
            ],
            is_extended_id=True,
        )

    def dbc_request_and_parse(self, target_pgn) -> CanData | None:
        """Sends a J1939 read request decodes the response, PGN agnostic."""
        # Create the CAN request message
        request = self.get_dbc_request(target_pgn)
        try:
            self.bus.send(request)
            logger.info(
                f"Read request sent for PGN: {hex(target_pgn)} with B7: {hex(self.dbc_request.b7)}"
            )
        except can.CanError as e:
            logger.error(f"CAN transmission error: {e}")
            self.errors.append(str(e))
            return

        message = self.wait_for_response(target_pgn)
        if message:
            try:
                message_data = message.data
                frame_id = (0x14 << 24) | (target_pgn << 8) | 0xD0
                msg = self.db.get_message_by_frame_id(frame_id)
                decoded = msg.decode(message_data)
                self.update_data(decoded)
                return self.data

            except Exception as e:
                logger.error(f"Failed to decode: {e}")
                self.errors.append(str(e))
                return

        logger.error(f"No response for PGN: {hex(target_pgn)}")
        self.errors.append(f"No response for PGN: {hex(target_pgn)}")

    def wait_for_response(self, target_pgn, timeout=2):
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
            if not hasattr(self.data, normalized_field):
                setattr(self.data, normalized_field, value)

            setattr(self.data, normalized_field, value)

            # Collect fault information if present
            if "fault" in field.lower() and value:
                self.system_errors.append(field)


if __name__ == "__main__":
    handler = DBCMessageHandler()

    # Request MCU Summary (0xFF20D0)
    handler.dbc_request_and_parse(0xFF20)  # MCU_Summary

    # print("Charged Energy:", handler.charged_energy)
    # print("Charge State:", handler.charge_state)
    # print("Plug State:", handler.plug_state)
    # print("Errors:", handler.get_errors())

    # Request MCU_SOC Summary (0xFF24)
    handler.dbc_request_and_parse(0xFF24)  # MCU_SOC
    handler.dbc_request_and_parse(0xFF10)  # Pack_sumary
    # print("SOC:", handler.MCU_SOC)

    # print("Pack Current:", handler.pack_current)
