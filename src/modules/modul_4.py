"""
pipeline/modul4_indeks_persimpangan.py
═══════════════════════════════════════════════════════
PIPELINE MODUL 4 – Indeks Persimpangan (BST)
Topik 7: Smart Traffic Simulation & Signal Optimization
ELT60213 Algoritma dan Struktur Data
═══════════════════════════════════════════════════════

PERAN DALAM PIPELINE:
  Menyediakan lookup cepat persimpangan berdasarkan nama.
  Juga menyimpan metadata (degree, jumlah antrian, siklus lampu)
  untuk tiap persimpangan dalam struktur BST.

ALUR:
  1. Bangun BST dari semua 25 persimpangan
  2. Simpan metadata: degree + jumlah kendaraan antri
  3. Demo pencarian (search, range query)
  4. Tampilkan daftar terurut (inorder)
  5. Update data realtime dari simulasi

STRUKTUR DATA YANG DIPAKAI:
  → IntersectionBST (Binary Search Tree dari nol)
  → BSTNode dengan data dict metadata
"""

import sys
import os
import random

ROOT_SRC = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_SRC not in sys.path:
    sys.path.insert(0, ROOT_SRC)

from modules.data_structures.graph import build_traffic_graph # type: ignore
from modules.data_structures.bst import IntersectionBST, build_intersection_bst # pyright: ignore[reportMissingImports]


# ═══════════════════════════════════════════════
# PIPELINE UTAMA
# ═══════════════════════════════════════════════

def jalankan_pipeline(graf, manajer=None,
                      tampil_detail: bool = True) -> IntersectionBST:
    """
    Jalankan pipeline Modul 4: bangun dan kelola indeks BST.

    Args:
        graf    : TrafficGraph dari Modul 1
        manajer : TrafficQueueManager dari Modul 2 (opsional)

    Returns:
        IntersectionBST yang sudah terisi metadata
    """

    random.seed(17)
    garis = "─" * 52

    print(f"\n{'═'*52}")
    print(f"  PIPELINE MODUL 4 – INDEKS PERSIMPANGAN (BST)")
    print(f"{'═'*52}")

    # ── TAHAP 1: Bangun BST ────────────────────
    print(f"\n  [TAHAP 1] Membangun BST indeks persimpangan...")
    bst = build_intersection_bst(graf)
    print(f"  ✓ BST berhasil dibangun")
    print(f"    Jumlah node : {bst.size}")
    print(f"    Tinggi pohon: {bst.height()} "
          f"(ideal log₂(25)≈4.6, worst=25)")
    print(f"    Node minimum: {bst.min_key()}")
    print(f"    Node maksimum: {bst.max_key()}")

    # ── TAHAP 2: Update Metadata Antrian ───────
    print(f"\n  [TAHAP 2] Update metadata antrian kendaraan...")
    if manajer:
        for nama in graf.nodes:
            node = bst.search(nama)
            if node:
                q_size = manajer.antrian(nama).size()
                node.data["antrian"] = q_size
                node.data["status"]  = (
                    "MACET" if q_size > 15 else
                    "RAMAI" if q_size > 7  else
                    "NORMAL"
                )
        print(f"  ✓ Metadata antrian diupdate dari Modul 2")
    else:
        # Simulasi data antrian acak jika Modul 2 tidak ada
        for nama in graf.nodes:
            node = bst.search(nama)
            if node:
                q = random.randint(0, 25)
                node.data["antrian"] = q
                node.data["status"]  = (
                    "MACET" if q > 15 else
                    "RAMAI" if q > 7  else "NORMAL"
                )
        print(f"  ✓ Metadata antrian disimulasi (random seed=17)")

    # ── TAHAP 3: Demo Pencarian ────────────────
    print(f"\n  [TAHAP 3] Demo pencarian BST (Big-O: O(log n) avg):")
    print(f"  {garis}")
    target_list = ["A1", "C3", "E5", "B2", "ZZ_TIDAKADA"]
    for target in target_list:
        node = bst.search(target)
        if node:
            print(f"  DITEMUKAN '{target}' → "
                  f"degree={node.data.get('degree',0)}, "
                  f"antrian={node.data.get('antrian',0)}, "
                  f"status={node.data.get('status','?')}")
        else:
            print(f"  TIDAK ADA '{target}'")
    print(f"  {garis}")

    # ── TAHAP 4: Daftar Terurut (Inorder) ──────
    if tampil_detail:
        print(f"\n  [TAHAP 4] Daftar persimpangan terurut (inorder, O(n)):")
        print(f"  {garis}")
        print(f"  {'Simpul':<8} {'Degree':<8} {'Antrian':<10} {'Status'}")
        print(f"  {garis}")
        for nama, data in bst.inorder():
            print(f"  {nama:<8} {data.get('degree',0):<8} "
                  f"{data.get('antrian',0):<10} "
                  f"{data.get('status','?')}")
        print(f"  {garis}")

    # ── TAHAP 5: Range Query ───────────────────
    print(f"\n  [TAHAP 5] Range query persimpangan B1 – C5:")
    hasil_range = bst.range_query("B1", "C5")
    print(f"  Ditemukan {len(hasil_range)} persimpangan dalam rentang B1–C5:")
    for nama, data in hasil_range:
        antrian = data.get("antrian", 0)
        bar = "█" * min(antrian, 20)
        print(f"    {nama}: antrian={antrian} {bar}")

    # ── TAHAP 6: Identifikasi Persimpangan Kritis ──
    print(f"\n  [TAHAP 6] Persimpangan kritis (status MACET):")
    macet_list = [
        (nama, data) for nama, data in bst.inorder()
        if data.get("status") == "MACET"
    ]
    if macet_list:
        for nama, data in macet_list:
            print(f"  ⚠ {nama}: {data.get('antrian',0)} kendaraan mengantri")
    else:
        print(f"  ✓ Tidak ada persimpangan kritis saat ini")

    print(f"\n  ✓ Pipeline Modul 4 selesai.")
    print(f"{'═'*52}\n")

    return bst


# ═══════════════════════════════════════════════
# FUNGSI QUERY UNTUK MODUL LAIN
# ═══════════════════════════════════════════════

def cari_persimpangan(bst: IntersectionBST, nama: str) -> dict | None:
    """Lookup persimpangan, return data-nya atau None."""
    node = bst.search(nama)
    return node.data if node else None


def daftar_terurut(bst: IntersectionBST) -> list:
    """Kembalikan semua persimpangan terurut alfabet beserta datanya."""
    return bst.inorder()


def persimpangan_dalam_zona(bst: IntersectionBST,
                            awal: str, akhir: str) -> list:
    """Kembalikan persimpangan dalam rentang nama awal–akhir."""
    return bst.range_query(awal, akhir)


# ═══════════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════════

if __name__ == "__main__":
    try:
        from .modul_1  import jalankan_pipeline as pipeline1
        from .modul_2 import  jalankan_pipeline as pipeline2
    except ImportError:
        from modul_1  import jalankan_pipeline as pipeline1
        from modul_2 import  jalankan_pipeline as pipeline2

    graf    = pipeline1(tampil_detail=False)
    manajer = pipeline2(graf, n_event=500, tampil_detail=False)
    bst     = jalankan_pipeline(graf, manajer, tampil_detail=True)