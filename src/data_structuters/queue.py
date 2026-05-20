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


# ─────────────────────────────────────────────
# Min-Heap (dari nol)
# ─────────────────────────────────────────────
class MinHeap:
    """
    Min-Heap generik berbasis array.
    Komparasi menggunakan key_fn(item) yang harus mengembalikan tuple
    sehingga mendukung multi-key (priority, arrival_time) untuk tie-break FIFO.

    Big-O:
        push    : O(log n)
        pop     : O(log n)
        peek    : O(1)
        size    : O(1)
    """

    def __init__(self, key_fn=None):
        self._data: list = []
        self._key_fn = key_fn if key_fn else lambda x: x

    # ── Internal helpers ────────────────────────────
    def _key(self, idx: int):
        return self._key_fn(self._data[idx])

    def _swap(self, i: int, j: int) -> None:
        self._data[i], self._data[j] = self._data[j], self._data[i]

    def _parent(self, i: int) -> int:
        return (i - 1) // 2

    def _left(self, i: int) -> int:
        return 2 * i + 1

    def _right(self, i: int) -> int:
        return 2 * i + 2

    def _sift_up(self, i: int) -> None:
        """Naikkan elemen ke posisi yang benar. Big-O: O(log n)"""
        while i > 0:
            p = self._parent(i)
            if self._key(i) < self._key(p):
                self._swap(i, p)
                i = p
            else:
                break

    def _sift_down(self, i: int) -> None:
        """Turunkan elemen ke posisi yang benar. Big-O: O(log n)"""
        n = len(self._data)
        while True:
            smallest = i
            l, r = self._left(i), self._right(i)
            if l < n and self._key(l) < self._key(smallest):
                smallest = l
            if r < n and self._key(r) < self._key(smallest):
                smallest = r
            if smallest != i:
                self._swap(i, smallest)
                i = smallest
            else:
                break

    # ── Public API ──────────────────────────────────
    def push(self, item) -> None:
        """Tambah elemen baru. Big-O: O(log n)"""
        self._data.append(item)
        self._sift_up(len(self._data) - 1)

    def pop(self):
        """Hapus dan kembalikan elemen terkecil. Big-O: O(log n)"""
        if not self._data:
            raise IndexError("pop from empty heap")
        # swap root dan elemen terakhir
        self._swap(0, len(self._data) - 1)
        item = self._data.pop()
        if self._data:
            self._sift_down(0)
        return item

    def peek(self):
        """Lihat elemen terkecil tanpa menghapus. Big-O: O(1)"""
        if not self._data:
            raise IndexError("peek from empty heap")
        return self._data[0]

    @property
    def size(self) -> int:
        return len(self._data)

    def is_empty(self) -> bool:
        return len(self._data) == 0

    def __repr__(self) -> str:
        return f"MinHeap(size={self.size})"


