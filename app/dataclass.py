from dataclasses import dataclass
import cantools


@dataclass
class CanData:

    # OBDii Handled
    runtime: str = "00:00:00"

    # From PGN 0xFF20 MCU_Summary
    mcu_chargedenergy: float = 0.0
    mcu_chargedenergy_factor: float = 0.01
    mcu_chargedenergy_unit: str = "kWh"
    mcu_chargestate: cantools.database.namedsignalvalue.NamedSignalValue = None
    mcu_plugstate: cantools.database.namedsignalvalue.NamedSignalValue = None
    mcu_fault_notlocked: int = 0
    mcu_fault_thermundertemp: int = 0
    mcu_fault_thermovertemp: int = 0
    mcu_fault_lvc: int = 0
    mcu_fault_hvc: int = 0
    mcu_fault_thermcensus: int = 0
    mcu_fault_cellcensus: int = 0
    mcu_fault_hardware: int = 0
    mcu_fault_illegalconfig: int = 0

    # PGN 0xFF21 MCU_PackSummary
    mcu_packvoltage: float = 0.0
    mcu_packvoltage_factor: float = 0.1
    mcu_packvoltage_unit: str = "V"
    mcu_packcurrent: float = 0.0
    mcu_packcurrent_factor: float = 0.1
    mcu_packcurrent_unit: str = "A"
    mcu_packkw: float = 0.0
    mcu_packkw_factor: float = 0.001
    mcu_packkw_unit: str = "kW"

    # PGN 0xFF22 MCU_CellSummary
    mcu_cellcount: int = 0
    mcu_lowestcellv: float = 0.0
    mcu_lowestcellv_factor: float = 0.1
    mcu_lowestcellv_unit: str = "mV"
    mcu_meancellv: float = 0.0
    mcu_meancellv_factor: float = 0.1
    mcu_meancellv_unit: str = "mV"
    mcu_highestcellv: float = 0.0
    mcu_highestcellv_factor: float = 0.1
    mcu_highestcellv_unit: str = "mV"

    # PGN 0xFF24 MCU_SOCSummary
    mcu_soc: int = 0
    mcu_soc_unit: str = "%"
    mcu_packcurkwh: float = 0.0
    mcu_packcurkwh_factor: float = 0.1
    mcu_packcurkwh_unit: str = "kWh"
    mcu_packmaxkwh: float = 0.0
    mcu_packmaxkwh_factor: float = 0.1
    mcu_packmaxkwh_unit: str = "kWh"

    # PGN 0xFF11 BMS_Config1
    bms_hvc: float = 0.0
    bms_hvc_factor: float = 0.1
    bms_hvc_unit: str = "mV"
    bms_lvc: float = 0.0
    bms_lvc_factor: float = 0.1
    bms_lvc_unit: str = "mV"
    bms_bvmin: float = 0.0
    bms_bvmin_factor: float = 0.1
    bms_bvmin_unit: str = "mV"


@dataclass
class DBCRequest:
    request_rate: hex = 0x0A
    repeat_count: hex = 0x14
    b7: hex = 0x00
    mcu_summary: hex = 0xFF20
    mcu_pack_summary: hex = 0xFF21
    mcu_cell_summary: hex = 0xFF22
    mcu_soc_summary: hex = 0xFF24
    bms_config1: hex = 0xFF11
