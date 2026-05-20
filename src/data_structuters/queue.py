import time
import random



# ─────────────────────────────────────────────
# Konstanta Prioritas Kendaraan
# ─────────────────────────────────────────────
VEHICLE_PRIORITY = {
    "AMBULANS": 1,
    "BUS":      2,
    "MOBIL":    3,
    "MOTOR":    4,
}

VEHICLE_TYPES = list(VEHICLE_PRIORITY.keys())


# ─────────────────────────────────────────────
# Data Class Kendaraan
# ─────────────────────────────────────────────
class Vehicle:
    """Representasi satu kendaraan dalam simulasi."""

    _id_counter = 0   # counter global untuk ID unik

    def __init__(self, vehicle_type: str, origin: str, destination: str,
                 arrival_time: float = 0.0):
        Vehicle._id_counter += 1
        self.vehicle_id   = Vehicle._id_counter
        self.vehicle_type = vehicle_type.upper()
        self.origin       = origin
        self.destination  = destination
        self.arrival_time = arrival_time          # waktu masuk antrian (FIFO tie-break)
        self.priority     = VEHICLE_PRIORITY.get(self.vehicle_type, 99)

    def __repr__(self) -> str:
        return (f"Vehicle(id={self.vehicle_id}, type={self.vehicle_type}, "
                f"prio={self.priority}, {self.origin}→{self.destination})")

