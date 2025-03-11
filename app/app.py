from current_gui import GUI
from obd2_message_handler import OBD2MessageHandler
from can_opener import CanOpener
import threading


class App:
    """
    The main application class
    """

    def __init__(self):
        self.gui = GUI()
        self.obd2_handler = OBD2MessageHandler()
        self.can_opener = CanOpener()
        self.charging_mode = False

    def query_data(self):
        """
        queries data and updates GUI
        """
        while True:
            self.charging_mode = can_opener.listen_for_charge_messages()
            if self.charging_mode:
                self.display_charging_ui()
            else:
                self.display_default_ui()

    def display_default_ui(self):
        """
        displays default UI
        """
        self.obd2_handler.request_and_parse("runtime")
        runtime = self.obd2_handler.get_runtime()
        self.obd2_handler.request_and_parse("voltage")
        voltage = self.obd2_handler.get_voltage()
        system_errors = self.obd2_handler.system_errors
        self.obd2_handler.request_and_parse("soc")
        soc = self.obd2_handler.get_soc()
        # errors = obd2_handler.get_errors()
        # gui.show_errors(errors)
        self.gui.update_error_label(system_errors)
        self.gui.update_runtime(runtime)
        self.gui.update_soc(soc)
        self.gui.update_voltage(voltage)
        self.gui.refresh_ui()

    def display_charging_ui(self):
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
            args=(self.gui, self.obd2_handler, self.can_opener),
            daemon=True,
        )
        query_thread.start()
        self.gui.run()


if __name__ == "__main__":
    app = App()
    app.main()
