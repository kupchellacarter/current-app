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
        self.obd2_handler: OBD2MessageHandler = None
        self.dbc_handler: DBCMessageHandler = None
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

    def display_default_ui(self, last_display: str):
        """
        displays default UI
        """
        if not last_display or last_display != "default_ui":
            self.gui.display_defualt_ui()
        self.data = self.obd2_handler.obd2_request_and_parse("runtime")
        runtime = self.data.runtime
        self.data = self.dbc_handler.dbc_request_and_parse(self.dbc_request.mcu_summary)

        #  PGN 0xFF21 MCU_PackSummary
        self.data = self.dbc_handler.dbc_request_and_parse(
            self.dbc_request.mcu_pack_summary
        )
        pack_voltage = self.data.mcu_packvoltage * self.data.mcu_packvoltage_factor
        pack_voltage_labelled = f"{pack_voltage} {self.data.mcu_packvoltage_unit}"
        pack_current = self.data.mcu_packcurrent * self.data.mcu_packcurrent_factor
        pack_current_labelled = f"{pack_current} {self.data.mcu_packcurrent_unit}"
        pack_kw = pack_voltage * pack_current
        pack_kw_labelled = f"{pack_kw} {self.data.mcu_packkw_unit}"

        # PGN 0xFF22 MCU_CellSummary
        self.data = self.dbc_handler.dbc_request_and_parse(
            self.dbc_request.mcu_cell_summary
        )
        cell_count = self.data.mcu_cellcount
        lowest_cell_v = self.data.mcu_lowestcellv * self.data.mcu_lowestcellv_factor
        lowest_cell_v_labelled = f"{lowest_cell_v} {self.data.mcu_lowestcellv_unit}"
        mean_cell_v = self.data.mcu_meancellv * self.data.mcu_meancellv_factor
        mean_cell_v_labelled = f"{mean_cell_v} {self.data.mcu_meancellv_unit}"
        highest_cell_v = self.data.mcu_highestcellv * self.data.mcu_highestcellv_factor
        highest_cell_v_labelled = f"{highest_cell_v} {self.data.mcu_highestcellv_unit}"

        # PGN 0xFF24 MCU_SOCSummary
        self.data = self.dbc_handler.dbc_request_and_parse(
            self.dbc_request.mcu_soc_summary
        )
        soc = self.data.mcu_soc
        soc_labelled = f"{soc} {self.data.mcu_soc_unit}"
        pack_cur_kwh = self.data.mcu_packcurkwh * self.data.mcu_packcurkwh_factor
        pack_cur_kwh_labelled = f"{pack_cur_kwh} {self.data.mcu_packcurkwh_unit}"
        pack_max_kwh = self.data.mcu_packmaxkwh * self.data.mcu_packmaxkwh_factor
        pack_max_kwh_labelled = f"{pack_max_kwh} {self.data.mcu_packmaxkwh_unit}"

        self.data = self.dbc_handler.dbc_request_and_parse(self.dbc_request.bms_config1)

        # errors = obd2_handler.get_errors()
        # gui.show_errors(errors)
        # self.gui.update_error_label(system_errors)
        self.gui.set_soc(soc)
        self.gui.set_pack_kwh(pack_cur_kwh_labelled, pack_max_kwh_labelled)

        self.gui.set_pack_voltage(pack_voltage_labelled)
        self.gui.set_pack_current(pack_current_labelled)
        self.gui.set_power(pack_kw_labelled)
        self.gui.set_cell_voltage(lowest_cell_v_labelled)
        self.gui.set_cell_voltage(mean_cell_v_labelled)
        self.gui.set_cell_voltage(highest_cell_v_labelled)

        self.gui.update_runtime(runtime)
        self.gui.refresh_ui()

    def display_charging_ui(self, last_display: str):
        """
        displays charging UI
        """
        pass

    def main(self):
        """
        description here
        """
        try:
            app.obd2_handler = OBD2MessageHandler(can_data=self.data)
            app.dbc_handler = DBCMessageHandler(can_data=self.data)
        except Exception as e:
            app.gui.display_error_ui(e)
            self.gui.run()
            return
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
