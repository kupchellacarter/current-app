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
        self.data: CanData = CanData()
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
            self.charging_mode = self.dbc_handler.charge_mode()
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
        if self.data:
            runtime = self.data.runtime
            self.gui.update_runtime(runtime)

        # PGN 0xFF20 MCU_Summary
        self.data = self.dbc_handler.dbc_request_and_parse(self.dbc_request.mcu_summary)

        if self.data:
            mcu_chargedenergy = (
                self.data.mcu_chargedenergy * self.data.mcu_chargedenergy_factor
            )
            mcu_chargedenergy_labelled = (
                f"{mcu_chargedenergy} {self.data.mcu_chargedenergy_unit}"
            )
            if self.data.mcu_chargestate.value == 1:
                mcu_chargestate = "Charging"
            elif self.data.mcu_chargestate.value == 2:
                mcu_chargestate = "Warmdown"
            else:
                mcu_chargestate = "Charge State Unknown"

            if self.data.mcu_plugstate.value == 1:
                mcu_plugstate = "No Plug"
            elif self.data.mcu_plugstate.value == 2:
                mcu_plugstate = "Connected"
            else:
                mcu_plugstate = "Plug State Unknown"

        system_errors = []
        # if self.data.mcu_fault_notlocked:
        #    system_errors.append("MCU Fault: Not Locked")
        if self.data and self.data.mcu_fault_thermundertemp:
            system_errors.append("Low Temp!")
        if self.data and self.data.mcu_fault_thermovertemp:
            system_errors.append("High Temp!")
        if self.data and self.data.mcu_fault_lvc:
            system_errors.append("Low Voltage!")
        if self.data and self.data.mcu_fault_hvc:
            system_errors.append("High Voltage!")
        # if self.data.mcu_fault_thermcensus:
        # system_errors.append("MCU Fault: Therm Census")
        # if self.data.mcu_fault_cellcensus:
        # system_errors.append("MCU Fault: Cell Census")
        if self.data and self.data.mcu_fault_hardware:
            system_errors.append("Hardware Fault")
        # if self.data.mcu_fault_illegalconfig:
        #    system_errors.append("MCU Fault: Illegal Configuration")
        if not self.data:
            system_errors.append("No Data")

        #  PGN 0xFF21 MCU_PackSummary
        self.data = self.dbc_handler.dbc_request_and_parse(
            self.dbc_request.mcu_pack_summary
        )
        if self.data:
            pack_voltage = round(
                self.data.mcu_packvoltage * self.data.mcu_packvoltage_factor, 2
            )
            pack_voltage_labelled = f"{pack_voltage} {self.data.mcu_packvoltage_unit}"
            pack_current = round(
                self.data.mcu_packcurrent * self.data.mcu_packcurrent_factor, 2
            )
            pack_current_labelled = f"{pack_current} {self.data.mcu_packcurrent_unit}"
            pack_kw = round(pack_voltage * pack_current / 1000, 2)
            pack_kw_labelled = f"{pack_kw} {self.data.mcu_packkw_unit}"
            self.gui.set_power(pack_kw_labelled)
            self.gui.set_pack_voltage(pack_voltage_labelled)
            self.gui.set_pack_current(pack_current_labelled)

        # PGN 0xFF22 MCU_CellSummary
        self.data = self.dbc_handler.dbc_request_and_parse(
            self.dbc_request.mcu_cell_summary
        )
        if self.data:
            cell_count = self.data.mcu_cellcount
            mean_cell_v = round(self.data.mcu_meancellv * self.data.mcu_meancellv_factor, 2)
            mean_cell_v_labelled = f"{mean_cell_v} {self.data.mcu_meancellv_unit}"
            self.gui.set_cell_voltage(mean_cell_v_labelled)
            self.gui.set_cell_count(cell_count)

        # PGN 0xFF23 MCU_ThermSummary
        self.data = self.dbc_handler.dbc_request_and_parse(
            self.dbc_request.mcu_therm_summary
        )
        if self.data:
            highest_therm = self.data.mcu_thhighest
            self.gui.set_temp(highest_therm)

        # PGN 0xFF24 MCU_SOCSummary
        self.data = self.dbc_handler.dbc_request_and_parse(
            self.dbc_request.mcu_soc_summary
        )
        if self.data:
            soc = self.data.mcu_soc
            pack_cur_kwh = self.data.mcu_packcurkwh * self.data.mcu_packcurkwh_factor
            pack_cur_kwh_labelled = f"{pack_cur_kwh} {self.data.mcu_packcurkwh_unit}"
            pack_max_kwh = self.data.mcu_packmaxkwh * self.data.mcu_packmaxkwh_factor
            pack_max_kwh_labelled = f"{pack_max_kwh} {self.data.mcu_packmaxkwh_unit}"
            self.gui.set_soc(soc)
            self.gui.set_pack_kwh(pack_cur_kwh, pack_max_kwh_labelled)

        self.data = self.dbc_handler.dbc_request_and_parse(self.dbc_request.bms_config1)
        if self.data:
            hvc = round(self.data.bms_hvc * self.data.bms_hvc_factor, 2)
            lvc = round(self.data.bms_lvc * self.data.bms_lvc_factor, 2)
            if mean_cell_v:
                self.gui.set_cell_voltage_slider(mean_cell_v, lvc, hvc)

        self.gui.update_error_label(system_errors)
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
