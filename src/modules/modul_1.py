"""
pipeline/modul1_jaringan_jalan.py
═══════════════════════════════════════════════════════
PIPELINE MODUL 1 – Graph Jaringan Jalan Kota
Topik 7: Smart Traffic Simulation & Signal Optimization
ELT60213 Algoritma dan Struktur Data
═══════════════════════════════════════════════════════

PERAN DALAM PIPELINE:
  Membangun dan mengelola peta jaringan jalan kota.
  Modul ini adalah FONDASI — semua modul lain bergantung
  pada graf yang dihasilkan di sini.

ALUR:
  1. Bangun graf 25 persimpangan + ~40 segmen jalan (seed=17)
  2. Tampilkan info jaringan (node, edge, degree tiap simpul)
  3. Deteksi persimpangan terisolasi via DFS
  4. Sediakan fungsi query untuk modul lain

STRUKTUR DATA YANG DIPAKAI:
  → TrafficGraph (Adjacency List berbasis Linked List)
  → DFS untuk deteksi isolasi
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(_file_), ".."))

from data_structures.graph import TrafficGraph, build_traffic_graph


# ═══════════════════════════════════════════════
# PIPELINE UTAMA
# ═══════════════════════════════════════════════

def jalankan_pipeline(tampil_detail: bool = True) -> TrafficGraph:
    """
    Jalankan pipeline Modul 1: bangun dan validasi jaringan jalan.

    Returns:
        TrafficGraph siap pakai untuk modul-modul berikutnya.
    """

    garis = "─" * 52

    print(f"\n{'═'*52}")
    print(f"  PIPELINE MODUL 1 – JARINGAN JALAN KOTA")
    print(f"{'═'*52}")

    # ── TAHAP 1: Bangun Graf ───────────────────
    print(f"\n  [TAHAP 1] Membangun jaringan jalan (seed=17)...")
    graf = build_traffic_graph(seed=17)
    print(f"  ✓ Graf berhasil dibangun")
    print(f"    Persimpangan (node) : {graf.node_count}")
    print(f"    Segmen jalan (edge) : {graf.edge_count // 2} undirected")
    print(f"    Total directed edge : {graf.edge_count}")

    # ── TAHAP 2: Validasi Konektivitas ─────────
    print(f"\n  [TAHAP 2] Validasi konektivitas jaringan...")
    terhubung = graf.is_connected()
    terisolasi = graf.get_isolated_nodes()
    print(f"  ✓ Status konektivitas : {'TERHUBUNG PENUH ✓' if terhubung else 'ADA ISOLASI ⚠️'}")
    if terisolasi:
        print(f"  ⚠️ Node terisolasi     : {terisolasi}")
    else:
        print(f"    Node terisolasi     : tidak ada")