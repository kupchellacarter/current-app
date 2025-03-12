from dataclasses import dataclass


@dataclass
class CanData:
    runtime: int = 0
    # mcu_chargedenergy
    # mcu_chargestate
    # mcu_plugstate
    # mcu_fault_notlocked
    # mcu_fault_thermovertemp
    # mcu_fault_lvc
    # mcu_fault_hvc
    # mcu_fault_thermcensus
    # mcu_fault_cellcensus
    # mcu_fault_hardware
    # mcu_fault_illegalconfig

@dataclass
class DBCRequest:
    request_rate: hex =0x0A
    repeat_count:hex =0x14
    b7: hex =0x00
