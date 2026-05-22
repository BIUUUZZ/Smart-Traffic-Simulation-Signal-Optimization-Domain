"""
pipeline/modul3_rute_optimal.py
═══════════════════════════════════════════════════════
PIPELINE MODUL 3 – Rute Optimal Kendaraan (Dijkstra)
Topik 7: Smart Traffic Simulation & Signal Optimization
ELT60213 Algoritma dan Struktur Data
═══════════════════════════════════════════════════════

PERAN DALAM PIPELINE:
  Mencari rute jarak minimum antar persimpangan.
  Digunakan untuk navigasi kendaraan dan
  rekomendasi rute alternatif saat kemacetan.

ALUR:
  1. Inisialisasi Dijkstra solver dengan graf
  2. Jalankan 50 query rute (sesuai parameter sistem)
  3. Tampilkan hasil: jarak + jalur tiap query
  4. Deteksi persimpangan macet → rute alternatif
  5. Tabel perbandingan rute normal vs alternatif

STRUKTUR DATA YANG DIPAKAI:
  → DijkstraSolver (MinHeap dari Modul 2)
  → DijkstraResult (jarak + rekonstruksi path)
"""

import sys
import os
import random
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from data_structures.graph import build_traffic_graph
from data_structures.dijkstra import DijkstraSolver, INF


# ═══════════════════════════════════════════════
# PIPELINE UTAMA
# ═══════════════════════════════════════════════

def jalankan_pipeline(graf, manajer=None,
                      tampil_detail: bool = True) -> DijkstraSolver:
    """
    Jalankan pipeline Modul 3: pencarian rute optimal.

    Args:
        graf    : TrafficGraph dari Modul 1
        manajer : TrafficQueueManager dari Modul 2
                  (opsional, untuk deteksi kemacetan)

    Returns:
        DijkstraSolver yang bisa dipakai modul lain
    """

    random.seed(17)
    nodes  = graf.nodes
    garis  = "─" * 58
    solver = DijkstraSolver(graf)

    print(f"\n{'═'*58}")
    print(f"  PIPELINE MODUL 3 – RUTE OPTIMAL (DIJKSTRA)")
    print(f"{'═'*58}")

    # ── TAHAP 1: Inisialisasi ──────────────────
    print(f"\n  [TAHAP 1] Inisialisasi Dijkstra solver...")
    print(f"  ✓ Solver siap | V={graf.node_count} | E={graf.edge_count//2}")
    print(f"    Big-O per query : O((V + E) log V)")

    # ── TAHAP 2: 50 Query Rute ─────────────────
    print(f"\n  [TAHAP 2] Menjalankan 50 query rute (sesuai parameter sistem)...")
    query_results = []
    t_start = time.perf_counter()

    possible_pairs = [(src, dst) for src in nodes for dst in nodes if src != dst]
    if len(possible_pairs) <= 50:
        pasang_query = possible_pairs
    else:
        pasang_query = random.sample(possible_pairs, 50)

    n_query = len(pasang_query)
    for src, dst in pasang_query:
        dist, path = solver.shortest_path(src, dst)
        query_results.append((src, dst, dist, path))

    t_total = time.perf_counter() - t_start
    terjangkau = sum(1 for _, _, d, _ in query_results if d < INF)

    if n_query == 0:
        print(f"  ✓ Tidak ada query yang dijalankan.")
    else:
        print(f"  ✓ {n_query} query selesai dalam {t_total:.4f} detik")
        print(f"    Rata-rata per query : {t_total/n_query:.6f} detik")
        print(f"    Rute terjangkau     : {terjangkau}/{n_query}")

    # ── TAHAP 3: Tampilkan Sample ──────────────
    if tampil_detail:
        print(f"\n  [TAHAP 3] Sample 10 hasil query:")
        print(f"  {garis}")
        print(f"  {'#':<4} {'Dari':<6} {'Tujuan':<8} {'Jarak(m)':<12} {'Jalur'}")
        print(f"  {garis}")
        for i, (src, dst, dist, path) in enumerate(query_results[:10], 1):
            jarak_str = f"{dist:.0f}" if dist < INF else "∞"
            jalur_str = " → ".join(path) if path else "-"
            # Potong kalau terlalu panjang
            if len(jalur_str) > 35:
                jalur_str = jalur_str[:32] + "..."
            print(f"  {i:<4} {src:<6} {dst:<8} {jarak_str:<12} {jalur_str}")
        print(f"  {garis}")

    # ── TAHAP 4: Rute Terpendek & Terpanjang ──
    valid = [(d, p, s, t) for s, t, d, p in query_results if d < INF]
    if valid:
        valid.sort(key=lambda x: x[0])
        d_min, p_min, s_min, t_min = valid[0]
        d_max, p_max, s_max, t_max = valid[-1]

        print(f"\n  [TAHAP 4] Statistik 50 query:")
        print(f"    Rute TERPENDEK : {s_min} → {t_min}")
        print(f"                   Jarak={d_min:.0f}m | "
              f"Jalur: {' → '.join(p_min)}")
        print(f"    Rute TERPANJANG: {s_max} → {t_max}")
        print(f"                   Jarak={d_max:.0f}m | "
              f"Hop={len(p_max)-1} persimpangan")
        jarak_rata = sum(d for d,_,_,_ in valid) / len(valid)
        print(f"    Rata-rata jarak: {jarak_rata:.0f} meter")

    # ── TAHAP 5: Rute Alternatif Kemacetan ─────
    print(f"\n  [TAHAP 5] Simulasi rute alternatif saat kemacetan:")

    # Deteksi kemacetan: pakai data antrian jika ada, atau pakai default
    if manajer:
        status = manajer.status_all()
        macet  = [s["intersection"] for s in status[:3]
                  if s["current_size"] > 5]
    else:
        macet = ["B2", "C3", "D3"]   # default simulasi kemacetan

    print(f"  Persimpangan macet : {macet}")

    contoh_src, contoh_dst = "A1", "E5"
    d_normal, p_normal     = solver.shortest_path(contoh_src, contoh_dst)
    d_alt, p_alt           = solver.route_recommendation(
                                 contoh_src, contoh_dst, congested=macet)

    print(f"\n  Rute {contoh_src} → {contoh_dst}:")
    print(f"  {garis}")
    print(f"  NORMAL    : {' → '.join(p_normal)}")
    print(f"              Jarak = {d_normal:.0f} meter")
    if d_alt < INF and p_alt:
        print(f"  ALTERNATIF: {' → '.join(p_alt)}")
        print(f"              Jarak = {d_alt:.0f} meter "
              f"(+{d_alt-d_normal:.0f}m lebih jauh)")
    else:
        print(f"  ALTERNATIF: Tidak ada rute yang menghindari {macet}")
    print(f"  {garis}")

    # ── TAHAP 6: Top-3 Terdekat dari beberapa titik ──
    if tampil_detail:
        print(f"\n  [TAHAP 6] Top-3 persimpangan terdekat dari A1, C3, E5:")
        for titik in ["A1", "C3", "E5"]:
            top3 = solver.top_k_routes(titik, k=3)
            print(f"\n    Dari {titik}:")
            for node, dist, path in top3:
                print(f"      → {node}: {dist:.0f}m "
                      f"({' → '.join(path)})")

    print(f"\n  ✓ Pipeline Modul 3 selesai.")
    print(f"{'═'*58}\n")

    return solver


# ═══════════════════════════════════════════════
# FUNGSI QUERY UNTUK MODUL LAIN
# ═══════════════════════════════════════════════

def cari_rute(solver: DijkstraSolver,
              asal: str, tujuan: str) -> tuple:
    """Shortcut pencarian rute untuk modul lain."""
    return solver.shortest_path(asal, tujuan)


def rute_darurat(solver: DijkstraSolver,
                 asal: str, tujuan: str,
                 hindari: list = None) -> tuple:
    """
    Rute khusus darurat (AMBULANS) yang menghindari kemacetan.
    Dipanggil oleh Modul 6 CLI saat AMBULANS butuh rute cepat.
    """
    return solver.route_recommendation(asal, tujuan, congested=hindari)


# ═══════════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════════

if __name__ == "__main__":
    # Use relative imports to work when running as a module inside the package,
    # with fallback to absolute imports when executed as a script.
    try:
        from .modul_1  import jalankan_pipeline as pipeline1
        from .modul_2 import  jalankan_pipeline as pipeline2
    except ImportError:
        from modul_1  import jalankan_pipeline as pipeline1
        from modul_2 import  jalankan_pipeline as pipeline2

    graf    = pipeline1(tampil_detail=False)
    manajer = pipeline2(graf, n_event=500, tampil_detail=False)
    solver  = jalankan_pipeline(graf, manajer, tampil_detail=True)