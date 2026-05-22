"""
pipeline/modul2_antrian_kendaraan.py
═══════════════════════════════════════════════════════
PIPELINE MODUL 2 – Antrian Kendaraan per Persimpangan
Topik 7: Smart Traffic Simulation & Signal Optimization
ELT60213 Algoritma dan Struktur Data
═══════════════════════════════════════════════════════

PERAN DALAM PIPELINE:
  Mengelola antrian kendaraan di setiap persimpangan.
  Kendaraan masuk dan berangkat berdasarkan prioritas:
  AMBULANS > BUS > MOBIL > MOTOR (tie-break: FIFO)

ALUR:
  1. Inisialisasi antrian untuk semua 25 persimpangan
  2. Simulasikan kendaraan masuk (500 event)
  3. Tampilkan status antrian per persimpangan
  4. Proses keberangkatan berdasarkan prioritas
  5. Laporan statistik akhir

STRUKTUR DATA YANG DIPAKAI:
  → MinHeap (dari nol, tanpa heapq)
  → IntersectionQueue per persimpangan
  → TrafficQueueManager untuk semua persimpangan
"""

import sys
import os
import random
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from data_structures.graph import build_traffic_graph
from data_structures.priority_queue import (
    TrafficQueueManager,
    Vehicle,
    VEHICLE_TYPES
)


# ═══════════════════════════════════════════════
# PIPELINE UTAMA
# ═══════════════════════════════════════════════

def jalankan_pipeline(graf, n_event: int = 500,
                      tampil_detail: bool = True) -> TrafficQueueManager:
    """
    Jalankan pipeline Modul 2: simulasi antrian kendaraan.

    Args:
        graf     : TrafficGraph dari Modul 1
        n_event  : jumlah event kendaraan masuk (default 500)

    Returns:
        TrafficQueueManager dengan state akhir simulasi
    """

    random.seed(17)
    nodes = graf.nodes
    garis = "─" * 52

    print(f"\n{'═'*52}")
    print(f"  PIPELINE MODUL 2 – ANTRIAN KENDARAAN")
    print(f"{'═'*52}")

    # ── TAHAP 1: Inisialisasi ──────────────────
    print(f"\n  [TAHAP 1] Inisialisasi antrian {len(nodes)} persimpangan...")
    manajer = TrafficQueueManager(nodes)
    print(f"  ✓ {len(nodes)} antrian siap (semua kosong)")

    # ── TAHAP 2: Simulasi Kendaraan Masuk ──────
    print(f"\n  [TAHAP 2] Simulasi {n_event} event kendaraan masuk...")
    log_masuk = []   # simpan log untuk ditampilkan
    t_start   = time.perf_counter()

    for i in range(n_event):
        # Pilih persimpangan dan jenis kendaraan secara acak
        asal   = random.choice(nodes)
        tujuan = random.choice([n for n in nodes if n != asal])
        jenis  = random.choice(VEHICLE_TYPES)

        kendaraan = Vehicle(jenis, asal, tujuan,
                            arrival_time=float(i))
        manajer.masuk(asal, kendaraan)

        # Simpan 10 log pertama untuk ditampilkan
        if i < 10:
            log_masuk.append((i+1, jenis, asal, tujuan))

    t_selesai = time.perf_counter() - t_start
    print(f"  ✓ {n_event} kendaraan berhasil masuk antrian")
    print(f"    Waktu proses : {t_selesai:.4f} detik")
    print(f"    Big-O        : O(log n) per enqueue")

    # ── TAHAP 3: Tampilkan Sample Log ──────────
    if tampil_detail:
        print(f"\n  [TAHAP 3] Sample 10 event pertama:")
        print(f"  {garis}")
        print(f"  {'No':<5} {'Jenis':<12} {'Dari':<8} {'Tujuan'}")
        print(f"  {garis}")
        for no, jenis, asal, tujuan in log_masuk:
            print(f"  {no:<5} {jenis:<12} {asal:<8} {tujuan}")
        print(f"  {garis}")

    # ── TAHAP 4: Status Antrian ─────────────────
    print(f"\n  [TAHAP 4] Status antrian per persimpangan (top 8 tersibuk):")
    print(f"  {garis}")
    print(f"  {'Simpul':<10} {'Antrian':<12} {'Berikutnya (prioritas tertinggi)'}")
    print(f"  {garis}")

    status_list = manajer.status_all()
    for s in status_list[:8]:
        nama    = s["intersection"]
        ukuran  = s["current_size"]
        antrian = manajer.antrian(nama)
        if not antrian.is_empty():
            berikut = antrian.peek()
            info    = f"{berikut.vehicle_type} (ID={berikut.vehicle_id})"
        else:
            info = "(kosong)"
        print(f"  {nama:<10} {ukuran:<12} {info}")

    print(f"  {garis}")
    total_kendaraan = sum(s["current_size"] for s in status_list)
    print(f"  Total kendaraan di seluruh antrian: {total_kendaraan}")

    # ── TAHAP 5: Proses Keberangkatan ──────────
    print(f"\n  [TAHAP 5] Simulasi 20 keberangkatan dari persimpangan tersibuk:")
    print(f"  {garis}")

    # Ambil 4 persimpangan tersibuk
    tersibuk = [s["intersection"] for s in status_list[:4]]
    berangkat_log = []

    for _ in range(20):
        simpul = random.choice(tersibuk)
        antrian = manajer.antrian(simpul)
        if not antrian.is_empty():
            kendaraan = manajer.berangkat(simpul)
            berangkat_log.append((simpul, kendaraan))

    for simpul, k in berangkat_log[:10]:
        print(f"  ← {k.vehicle_type:<10} berangkat dari {simpul} "
              f"→ {k.destination}  [prioritas={k.priority}]")

    print(f"  {garis}")
    print(f"  ✓ Urutan keberangkatan sesuai prioritas "
          f"(AMBULANS=1 > BUS=2 > MOBIL=3 > MOTOR=4)")

    # ── TAHAP 6: Statistik Akhir ───────────────
    print(f"\n  [TAHAP 6] Statistik akhir antrian:")
    stats_all = manajer.status_all()
    total_in  = sum(s["total_in"]  for s in stats_all)
    total_out = sum(s["total_out"] for s in stats_all)
    total_now = sum(s["current_size"] for s in stats_all)
    print(f"    Total masuk        : {total_in}")
    print(f"    Total berangkat    : {total_out}")
    print(f"    Masih di antrian   : {total_now}")

    print(f"\n  ✓ Pipeline Modul 2 selesai.")
    print(f"{'═'*52}\n")

    return manajer


# ═══════════════════════════════════════════════
# FUNGSI QUERY UNTUK MODUL LAIN
# ═══════════════════════════════════════════════

def jumlah_antrian(manajer: TrafficQueueManager, simpul: str) -> int:
    """Berapa kendaraan yang sedang antri di simpul ini."""
    return manajer.antrian(simpul).size()


def kendaraan_berikutnya(manajer: TrafficQueueManager, simpul: str):
    """Lihat kendaraan yang akan berangkat berikutnya (tanpa menghapus)."""
    q = manajer.antrian(simpul)
    return q.peek() if not q.is_empty() else None


def simpul_tersibuk(manajer: TrafficQueueManager, top_n: int = 5) -> list:
    """Kembalikan top-N simpul dengan antrian terbanyak."""
    stats = manajer.status_all()
    return [(s["intersection"], s["current_size"]) for s in stats[:top_n]]


# ═══════════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════════

if __name__ == "__main__":
    from pipeline.modul1_jaringan_jalan import jalankan_pipeline
    graf    = pipeline1(tampil_detail=False)
    manajer = jalankan_pipeline(graf, n_event=500, tampil_detail=True)

    print("  [QUERY] Simpul tersibuk (Top-5):")
    for simpul, jumlah in simpul_tersibuk(manajer, 5):
        print(f"    {simpul}: {jumlah} kendaraan")