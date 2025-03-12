from current_gui import GUI
from obd2_message_handler import OBD2MessageHandler
from dbc_message_handler import DBCMessageHandler
import threading
from dataclass import CanData, DBCRequest


class App:
    """
    The main application class
    """

    def __init__(self):
        self.gui = GUI()
        self.data = CanData()
        self.dbc_request = DBCRequest()
        self.obd2_handler = OBD2MessageHandler(can_data=self.data)
        self.dbc_handler = DBCMessageHandler(can_data=self.data)
        self.charging_mode = False

    def query_data(self):
        """
        queries data and updates GUI
        """
        last_display = None
        while True:
            if self.charging_mode:
                self.display_charging_ui(last_display)
                last_display = "charging_ui"
            else:
                self.display_default_ui(last_display)
                last_display = "default_ui"

    def display_default_ui(self,last_display:str):
        """
        displays default UI
        """
        if not last_display or last_display != "default_ui":
            self.gui.display_defualt_ui()
        self.data = self.obd2_handler.obd2_request_and_parse("runtime")
        runtime = self.data.runtime
        self.data = self.dbc_handler.dbc_request_and_parse(self.dbc_request.mcu_soc_summary)
        soc = self.data.mcu_soc
        self.gui.set_soc(soc)
        # errors = obd2_handler.get_errors()
        # gui.show_errors(errors)
        # self.gui.update_error_label(system_errors)
        self.gui.update_runtime(runtime)
        self.gui.refresh_ui()

    def display_charging_ui(self,last_display:str):
        """
        displays charging UI
        """
        pass

    def main(self):
        """
        description here
        """
        # Start the query_data function in a separate background thread
        query_thread = threading.Thread(
            target=self.query_data,
            daemon=True,
        )
        query_thread.start()
        self.gui.run()


if __name__ == "__main__":
    app = App()
    app.main()
