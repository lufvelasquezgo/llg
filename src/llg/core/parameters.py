from dataclasses import dataclass

from llg.core.constants import EnergyUnit


@dataclass
class Parameters:
    energy_unit: EnergyUnit
    damping: float
    gyromagnetic: float
    delta_time: float

    def to_dict(self):
        return {
            "energy_unit": self.energy_unit.value,
            "damping": self.damping,
            "gyromagnetic": self.gyromagnetic,
            "delta_time": self.delta_time,
        }
