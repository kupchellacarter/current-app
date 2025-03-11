import can


class CanOpener:

    def __init__(self, channel="can0", bitrate=250000):
        self.channel = channel
        self.bitrate = bitrate
        self.bus = can.interface.Bus(
            channel=self.channel, bustype="socketcan", bitrate=self.bitrate
        )

    def listen_for_charge_messages(self) -> bool:
        """This function listens for messages that the charger sends when it's charging"""
        target_id = 0x18EB2440

        message = self.bus.recv()
        if message is not None:
            if message.arbitration_id == target_id:
                print("Charger Detected!")
                return True

        return False

        # TODO fill this in!
        # if it receives messages, return True
        # if no traffic, return False
        pass

    def decode_messages(self):

        pass


# Usage
if __name__ == "__main__":
    opener = CanOpener()
    result = opener.listen_for_charge_messages()
    print("MMessage Detected:", result)
