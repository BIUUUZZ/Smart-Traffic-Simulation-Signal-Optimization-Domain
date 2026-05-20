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


# ─────────────────────────────────────────────
# Priority Queue Kendaraan per Persimpangan
# ─────────────────────────────────────────────
class IntersectionQueue:
    """
    Priority Queue kendaraan untuk satu persimpangan.

    Urutan prioritas: AMBULANS > BUS > MOBIL > MOTOR
    Tie-break          : FIFO berdasarkan arrival_time

    Key komparasi: (priority, arrival_time)

    Big-O:
        enqueue : O(log n)
        dequeue : O(log n)
        peek    : O(1)
    """

    def __init__(self, intersection_name: str):
        self.name = intersection_name
        self._heap = MinHeap(
            key_fn=lambda v: (v.priority, v.arrival_time)
        )
        self._total_in  = 0
        self._total_out = 0

    def enqueue(self, vehicle: Vehicle) -> None:
        """
        Tambah kendaraan ke antrian.
        Big-O: O(log n)
        """
        self._heap.push(vehicle)
        self._total_in += 1

    def dequeue(self) -> Vehicle:
        """
        Ambil kendaraan dengan prioritas tertinggi.
        Tie-break FIFO (arrival_time terkecil duluan).
        Big-O: O(log n)
        """
        if self._heap.is_empty():
            raise IndexError(f"Antrian {self.name} kosong")
        vehicle = self._heap.pop()
        self._total_out += 1
        return vehicle

    def peek(self) -> Vehicle:
        """Lihat kendaraan berikutnya tanpa menghapus. Big-O: O(1)"""
        return self._heap.peek()

    def size(self) -> int:
        return self._heap.size

    def is_empty(self) -> bool:
        return self._heap.is_empty()

    def get_all_sorted(self) -> list:
        """
        Kembalikan semua kendaraan dalam urutan prioritas (non-destructive).
        Big-O: O(n log n)
        """
        temp = MinHeap(key_fn=lambda v: (v.priority, v.arrival_time))
        temp._data = list(self._heap._data)
        result = []
        import copy
        snapshot = MinHeap(key_fn=lambda v: (v.priority, v.arrival_time))
        snapshot._data = list(self._heap._data)
        # rebuild heap property
        n = len(snapshot._data)
        for i in range(n // 2 - 1, -1, -1):
            snapshot._sift_down(i)
        while not snapshot.is_empty():
            result.append(snapshot.pop())
        return result

    def stats(self) -> dict:
        return {
            "intersection" : self.name,
            "current_size" : self.size(),
            "total_in"     : self._total_in,
            "total_out"    : self._total_out,
        }

    def __repr__(self) -> str:
        return f"IntersectionQueue({self.name}, size={self.size()})"


# ─────────────────────────────────────────────
# Manajer antrian semua persimpangan
# ─────────────────────────────────────────────
class TrafficQueueManager:
    """
    Manajer Priority Queue untuk seluruh jaringan persimpangan.
    Setiap persimpangan punya IntersectionQueue sendiri.
    """

    def __init__(self, intersection_names: list):
        self._queues: dict[str, IntersectionQueue] = {
            name: IntersectionQueue(name)
            for name in intersection_names
        }

    def masuk(self, intersection: str, vehicle: Vehicle) -> None:
        """Tambah kendaraan ke antrian persimpangan."""
        if intersection not in self._queues:
            raise KeyError(f"Persimpangan '{intersection}' tidak ditemukan")
        vehicle.arrival_time = time.time()
        self._queues[intersection].enqueue(vehicle)

    def berangkat(self, intersection: str) -> Vehicle:
        """Keluarkan kendaraan dengan prioritas tertinggi."""
        if intersection not in self._queues:
            raise KeyError(f"Persimpangan '{intersection}' tidak ditemukan")
        return self._queues[intersection].dequeue()

    def antrian(self, intersection: str) -> IntersectionQueue:
        """Akses langsung ke antrian suatu persimpangan."""
        return self._queues[intersection]

    def status_all(self) -> list:
        """Status semua antrian, diurutkan dari tersibuk."""
        stats = [q.stats() for q in self._queues.values()]
        stats.sort(key=lambda s: s["current_size"], reverse=True)
        return stats

    def __repr__(self) -> str:
        total = sum(q.size() for q in self._queues.values())
        return f"TrafficQueueManager(intersections={len(self._queues)}, total_vehicles={total})"


# ─────────────────────────────────────────────
# Eksperimen Runtime
# ─────────────────────────────────────────────
def run_experiments() -> None:
    """
    Eksperimen enqueue/dequeue untuk N = 10, 25, 100 kendaraan.
    """
    print("\n" + "="*60)
    print("EKSPERIMEN RUNTIME - MODUL 2: PRIORITY QUEUE")
    print("="*60)
    print(f"{'N kendaraan':<14} {'enqueue (s)':<18} {'dequeue (s)':<15}")
    print("-"*50)

    for n in [10, 25, 100]:
        random.seed(17)
        q = IntersectionQueue("TEST")

        # Enqueue
        vehicles = []
        for i in range(n):
            vtype = random.choice(VEHICLE_TYPES)
            v = Vehicle(vtype, "A1", "B2", arrival_time=float(i))
            vehicles.append(v)

        t0 = time.perf_counter()
        for v in vehicles:
            q.enqueue(v)
        t_enq = time.perf_counter() - t0

        # Dequeue
        t0 = time.perf_counter()
        while not q.is_empty():
            q.dequeue()
        t_deq = time.perf_counter() - t0

        print(f"{n:<14} {t_enq:<18.6f} {t_deq:<15.6f}")

    print("="*60)
    print("Big-O: enqueue O(log n), dequeue O(log n)")
    print("="*60)


