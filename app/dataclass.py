from dataclasses import dataclass
import cantools


@dataclass
class CanData:

    # OBDii Handled
    runtime: str = "00:00:00"

    # From PGN 0xFF20 MCU_Summary
    mcu_chargedenergy: float = 0.0
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
    mcu_packcurrent: float = 0.0
    mcu_packkw: float = 0.0

    # PGN 0xFF22 MCU_CellSummary
    mcu_cellcount: int = 0
    mcu_lowestcellv: float = 0.0
    mcu_meancellv: float = 0.0
    mcu_highestcellv: float = 0.0

    # PGN 0xFF24 MCU_SOCSummary
    mcu_soc: int = 0
    mcu_packcurkwh: float = 0.0
    mcu_packmaxkwh: float = 0.0

    # PGN 0xFF11 BMS_Config1
    bms_hvc: float = 0.0
    bms_lvc: float = 0.0
    bms_bvmin: float = 0.0

    # Factors


@dataclass
class DBCRequest:
    request_rate: hex = 0x0A
    repeat_count: hex = 0x14
    b7: hex = 0x00
    mcu_soc_summary: hex = 0xFF24
