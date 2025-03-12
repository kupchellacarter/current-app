from dataclasses import dataclass
import cantools


@dataclass
class CanData:
    runtime: int = 0
    mcu_chargedenergy: float = 0.0
    mcu_chargestate: cantools.database.namedsignalvalue.NamedSignalValue
    mcu_plugstate: cantools.database.namedsignalvalue.NamedSignalValue
    mcu_fault_notlocked: int = 0
    mcu_fault_thermundertemp: int = 0
    mcu_fault_thermovertemp: int = 0
    mcu_fault_lvc: int = 0
    mcu_fault_hvc: int = 0
    mcu_fault_thermcensus: int = 0
    mcu_fault_cellcensus: int = 0
    mcu_fault_hardware: int = 0
    mcu_fault_illegalconfig: int = 0
    mcu_soc: int = 0
    mcu_packcurkwh: float = 0.0
    mcu_packmaxkwh: float = 0.0
    mcu_version: int = 0
    mcu_revision: int = 0
    mcu_bms_arch: cantools.database.namedsignalvalue.NamedSignalValue

@dataclass
class DBCRequest:
    request_rate: hex =0x0A
    repeat_count:hex =0x14
    b7: hex =0x00
