# ============================================================
# test_queue.py
# Unit Test Priority Queue Kendaraan
# Jalankan: pytest test/test_queue.py -v
# ============================================================

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.data_structures.priority_queue import (
    IntersectionQueue,
    Vehicle,
    VEHICLE_PRIORITY
)


# ─────────────────────────────────────────────
# Helper
# ─────────────────────────────────────────────
def buat_kendaraan(jenis: str):
    return Vehicle(
        vehicle_type=jenis,
        origin="A1",
        destination="B2",
        arrival_time=0.0
    )


def buat_queue(*kendaraan_list):
    q = IntersectionQueue("TEST")
    for kendaraan in kendaraan_list:
        q.enqueue(kendaraan)
    return q


# ══════════════════════════════════════════════
# KELOMPOK 1 — kondisi awal / queue kosong
# ══════════════════════════════════════════════

def test_queue_baru_pasti_kosong():
    q = IntersectionQueue("A1")

    assert q.is_empty() is True
    assert q.size() == 0


def test_dequeue_queue_kosong_error():
    q = IntersectionQueue("A1")

    try:
        q.dequeue()
        assert False
    except IndexError:
        assert True


def test_peek_queue_kosong_error():
    q = IntersectionQueue("A1")

    try:
        q.peek()
        assert False
    except IndexError:
        assert True


# ══════════════════════════════════════════════
# KELOMPOK 2 — enqueue & dequeue dasar
# ══════════════════════════════════════════════

def test_enqueue_satu_kendaraan():
    q = IntersectionQueue("A1")

    mobil = buat_kendaraan("MOBIL")

    q.enqueue(mobil)

    assert q.size() == 1
    assert q.is_empty() is False


def test_enqueue_lalu_dequeue():
    q = IntersectionQueue("A1")

    mobil = buat_kendaraan("MOBIL")

    q.enqueue(mobil)

    hasil = q.dequeue()

    assert hasil.vehicle_type == "MOBIL"


def test_size_naik_setiap_enqueue():
    q = IntersectionQueue("A1")

    for i in range(1, 6):
        q.enqueue(buat_kendaraan("MOBIL"))

        assert q.size() == i


def test_size_turun_setiap_dequeue():
    q = IntersectionQueue("A1")

    for _ in range(5):
        q.enqueue(buat_kendaraan("MOBIL"))

    for sisa in [4, 3, 2, 1, 0]:
        q.dequeue()

        assert q.size() == sisa


# ══════════════════════════════════════════════
# KELOMPOK 3 — prioritas kendaraan
# ══════════════════════════════════════════════

def test_ambulans_lebih_prioritas_dari_motor():
    q = IntersectionQueue("A1")

    motor = buat_kendaraan("MOTOR")
    ambulans = buat_kendaraan("AMBULANS")

    q.enqueue(motor)
    q.enqueue(ambulans)

    hasil = q.dequeue()

    assert hasil.vehicle_type == "AMBULANS"


def test_bus_lebih_prioritas_dari_mobil():
    q = IntersectionQueue("A1")

    mobil = buat_kendaraan("MOBIL")
    bus = buat_kendaraan("BUS")

    q.enqueue(mobil)
    q.enqueue(bus)

    hasil = q.dequeue()

    assert hasil.vehicle_type == "BUS"


def test_urutan_prioritas_lengkap():
    q = IntersectionQueue("A1")

    q.enqueue(buat_kendaraan("MOTOR"))
    q.enqueue(buat_kendaraan("MOBIL"))
    q.enqueue(buat_kendaraan("BUS"))
    q.enqueue(buat_kendaraan("AMBULANS"))

    hasil = []

    while not q.is_empty():
        hasil.append(q.dequeue().vehicle_type)

    assert hasil == [
        "AMBULANS",
        "BUS",
        "MOBIL",
        "MOTOR"
    ]


# ══════════════════════════════════════════════
# KELOMPOK 4 — FIFO tie-break
# ══════════════════════════════════════════════

def test_fifo_jika_prioritas_sama():
    q = IntersectionQueue("A1")

    k1 = Vehicle("MOBIL", "A1", "B1", arrival_time=1.0)
    k2 = Vehicle("MOBIL", "A1", "B1", arrival_time=2.0)
    k3 = Vehicle("MOBIL", "A1", "B1", arrival_time=3.0)

    q.enqueue(k1)
    q.enqueue(k2)
    q.enqueue(k3)

    assert q.dequeue().vehicle_id == k1.vehicle_id
    assert q.dequeue().vehicle_id == k2.vehicle_id
    assert q.dequeue().vehicle_id == k3.vehicle_id


def test_banyak_ambulans_fifo():
    q = IntersectionQueue("A1")

    a1 = Vehicle("AMBULANS", "A1", "B1", arrival_time=1.0)
    a2 = Vehicle("AMBULANS", "A1", "B1", arrival_time=2.0)
    a3 = Vehicle("AMBULANS", "A1", "B1", arrival_time=3.0)

    q.enqueue(a1)
    q.enqueue(a2)
    q.enqueue(a3)

    assert q.dequeue().vehicle_id == a1.vehicle_id


# ══════════════════════════════════════════════
# KELOMPOK 5 — peek
# ══════════════════════════════════════════════

def test_peek_tidak_menghapus():
    q = IntersectionQueue("A1")

    bus = buat_kendaraan("BUS")

    q.enqueue(bus)

    hasil = q.peek()

    assert hasil.vehicle_type == "BUS"
    assert q.size() == 1


# ══════════════════════════════════════════════
# KELOMPOK 6 — get_all_sorted & stats
# ══════════════════════════════════════════════

def test_get_all_sorted_tidak_mengubah_isi():
    q = IntersectionQueue("A1")

    q.enqueue(buat_kendaraan("BUS"))

    semua = q.get_all_sorted()

    assert len(semua) == 1
    assert q.size() == 1


def test_get_all_sorted_terurut_prioritas():
    q = IntersectionQueue("A1")

    q.enqueue(buat_kendaraan("MOTOR"))
    q.enqueue(buat_kendaraan("MOBIL"))
    q.enqueue(buat_kendaraan("BUS"))
    q.enqueue(buat_kendaraan("AMBULANS"))

    hasil = q.get_all_sorted()

    assert hasil[0].vehicle_type == "AMBULANS"
    assert hasil[-1].vehicle_type == "MOTOR"


def test_stats_benar():
    q = IntersectionQueue("A1")

    q.enqueue(buat_kendaraan("BUS"))
    q.enqueue(buat_kendaraan("MOBIL"))

    q.dequeue()

    stats = q.stats()

    assert stats["intersection"] == "A1"
    assert stats["current_size"] == 1
    assert stats["total_in"] == 2
    assert stats["total_out"] == 1


# ══════════════════════════════════════════════
# KELOMPOK 7 — skala besar
# ══════════════════════════════════════════════

def test_enqueue_100_kendaraan():
    q = IntersectionQueue("A1")

    vehicle_types = list(VEHICLE_PRIORITY.keys())

    for i in range(100):
        jenis = vehicle_types[i % 4]

        q.enqueue(
            Vehicle(
                jenis,
                "A1",
                "B1",
                arrival_time=float(i)
            )
        )

    assert q.size() == 100

    prev_priority = 0

    while not q.is_empty():
        kendaraan = q.dequeue()

        assert kendaraan.priority >= prev_priority

        prev_priority = kendaraan.priority