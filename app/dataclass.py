from dataclasses import dataclass


@dataclass
class CanData:
    runtime: int = 0
    voltage: float = 0.0
    battery_current: float = 0.0
    speed: float = 0.0
    soc: int = 0

@dataclass
class DBCRequest:
    request_rate: hex =0x0A
    repeat_count:hex =0x14
    b7: hex =0x00
