from dataclasses import dataclass


@dataclass
class CanData:
    runtime: int = 0
    battery_voltage: float = 0.0
    battery_current: float = 0.0
    speed: float = 0.0
    soc: int = 0
