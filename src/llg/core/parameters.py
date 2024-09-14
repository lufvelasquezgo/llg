from __future__ import annotations

from dataclasses import dataclass

from llg.core.constants import EnergyUnit


@dataclass
class Parameters:
    energy_unit: EnergyUnit
    damping: float
    gyromagnetic: float
    delta_time: float

    def __post_init__(self):
        if self.energy_unit is EnergyUnit.MEV:
            self.kb = 0.08618
        elif self.energy_unit is EnergyUnit.JOULE:
            self.kb = 1.38064852e-23
        elif self.energy_unit is EnergyUnit.ADIM:
            self.kb = 1.0
        else:
            raise ValueError("Invalid energy unit.")

    def to_dict(self):
        return {
            "energy_unit": self.energy_unit.value,
            "damping": self.damping,
            "gyromagnetic": self.gyromagnetic,
            "delta_time": self.delta_time,
            "kb": self.kb,
        }

    @classmethod
    def from_dict(cls, parameters_dict) -> Parameters:
        return cls(
            energy_unit=EnergyUnit(parameters_dict["energy_unit"]),
            damping=parameters_dict["damping"],
            gyromagnetic=parameters_dict["gyromagnetic"],
            delta_time=parameters_dict["delta_time"],
        )
