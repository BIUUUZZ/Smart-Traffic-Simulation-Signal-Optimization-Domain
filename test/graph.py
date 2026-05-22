# ============================================================
# tests/test_modul1_graph.py
# Unit test untuk Graph Jaringan Jalan (modul1_graph/graph.py)
# Jalankan: pytest tests/test_modul1_graph.py -v
# ============================================================

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(_file_), '..'))

from src.data_structures.graph import (
    EdgeNode,
    AdjacencyList,
    TrafficGraph,
    build_traffic_graph
)


# ── helper ────────────────────────────────────────────────────
def buat_graf_segitiga():
    g = TrafficGraph()
    g.add_road("A", "B", 100)
    g.add_road("B", "C", 200)
    g.add_road("C", "A", 150)
    return g


def buat_graf_lurus():
    """A--(350)--B--(420)--C--(380)--D"""
    g = TrafficGraph()
    g.add_road("A", "B", 350)
    g.add_road("B", "C", 420)
    g.add_road("C", "D", 380)
    return g


# ══════════════════════════════════════════════════════════════
# KELOMPOK 1 — AdjacencyList (Linked List)
# ══════════════════════════════════════════════════════════════

def test_adjacency_list_awal_kosong():
    al = AdjacencyList()
    assert al.size() == 0

def test_adjacency_list_add_menambah_size():
    al = AdjacencyList()
    al.add("B1", 300)
    al.add("C2", 500)
    assert al.size() == 2

def test_adjacency_list_get_all_berisi_destination_yang_ditambah():
    al = AdjacencyList()
    al.add("X", 100)
    al.add("Y", 200)
    dests = [d for d, _ in al.get_all()]
    assert "X" in dests
    assert "Y" in dests

def test_adjacency_list_remove_berhasil():
    al = AdjacencyList()
    al.add("B1", 300)
    al.add("C2", 500)
    hasil = al.remove("B1")
    assert hasil is True
    assert al.size() == 1

def test_adjacency_list_remove_node_tidak_ada_return_false():
    al = AdjacencyList()
    al.add("A", 100)
    assert al.remove("ZZZ") is False

def test_adjacency_list_iterasi_menghasilkan_semua_elemen():
    al = AdjacencyList()
    al.add("X", 100)
    al.add("Y", 200)
    count = sum(1 for _ in al)
    assert count == 2


# ══════════════════════════════════════════════════════════════
# KELOMPOK 2 — TrafficGraph dasar
# ══════════════════════════════════════════════════════════════

def test_graf_baru_pasti_kosong():
    g = TrafficGraph()
    assert g.node_count == 0
    assert g.edge_count == 0

def test_add_intersection_menambah_node():
    g = TrafficGraph()
    g.add_intersection("A1")
    g.add_intersection("B2")
    assert g.node_count == 2
    assert "A1" in g
    assert "B2" in g

def test_add_road_undirected_menambah_dua_arah():
    g = TrafficGraph()
    g.add_road("A", "B", 350, bidirectional=True)
    assert g.has_road("A", "B") is True
    assert g.has_road("B", "A") is True

def test_add_road_directed_hanya_satu_arah():
    g = TrafficGraph()
    g.add_road("X", "Y", 100, bidirectional=False)
    assert g.has_road("X", "Y") is True
    assert g.has_road("Y", "X") is False

def test_get_weight_mengembalikan_bobot_benar():
    g = TrafficGraph()
    g.add_road("A1", "A2", 350)
    assert g.get_weight("A1", "A2") == 350

def test_node_otomatis_ditambah_saat_add_road():
    g = TrafficGraph()
    g.add_road("NEW1", "NEW2", 999)
    assert "NEW1" in g
    assert "NEW2" in g

def test_degree_sesuai_jumlah_tetangga():
    g = TrafficGraph()
    g.add_road("A", "B", 100)
    g.add_road("A", "C", 200)
    assert g.degree("A") == 2
    assert g.degree("B") == 1

def test_neighbors_mengembalikan_semua_tetangga():
    g = TrafficGraph()
    g.add_road("A", "B", 100)
    g.add_road("A", "C", 200)
    nbrs = [n for n, _ in g.neighbors("A")]
    assert "B" in nbrs
    assert "C" in nbrs

def test_edge_count_undirected_dua_directed():
    g = TrafficGraph()
    g.add_road("A", "B", 100)
    assert g.edge_count == 2


# ══════════════════════════════════════════════════════════════
# KELOMPOK 3 — DFS traversal
# ══════════════════════════════════════════════════════════════

def test_dfs_mengunjungi_semua_node():
    g = buat_graf_lurus()
    visited = g.dfs("A")
    assert set(visited) == {"A", "B", "C", "D"}

def test_dfs_dimulai_dari_node_sumber():
    g = buat_graf_lurus()
    visited = g.dfs("A")
    assert visited[0] == "A"

def test_dfs_iteratif_sama_dengan_rekursif():
    g = buat_graf_lurus()
    rek = set(g.dfs("A"))
    itr = set(g.dfs_iterative("A"))
    assert rek == itr

def test_dfs_node_tidak_ada_kembalikan_list_kosong():
    g = buat_graf_lurus()
    assert g.dfs("TIDAKADA") == []


# ══════════════════════════════════════════════════════════════
# KELOMPOK 4 — konektivitas
# ══════════════════════════════════════════════════════════════

def test_is_connected_graf_terhubung():
    g = buat_graf_segitiga()
    assert g.is_connected() is True

def test_is_connected_graf_tidak_terhubung():
    g = TrafficGraph()
    g.add_intersection("X")
    g.add_intersection("Y")       # tidak ada edge X–Y
    assert g.is_connected() is False

def test_get_isolated_nodes_mendeteksi_terisolasi():
    g = TrafficGraph()
    g.add_intersection("SOLO")   # tidak ada edge
    g.add_road("A", "B", 100)
    isolated = g.get_isolated_nodes()
    assert "SOLO" in isolated
    assert "A" not in isolated

def test_remove_intersection_menghapus_node_dan_edge():
    g = TrafficGraph()
    g.add_road("A", "B", 100)
    g.add_road("B", "C", 200)
    g.remove_intersection("B")
    assert "B" not in g
    assert g.has_road("A", "B") is False


# ══════════════════════════════════════════════════════════════
# KELOMPOK 5 — build_traffic_graph (parameter Topik 7)
# ══════════════════════════════════════════════════════════════

def test_build_graf_menghasilkan_25_node():
    g = build_traffic_graph(seed=17)
    assert g.node_count == 25

def test_build_graf_edge_sekitar_40():
    g = build_traffic_graph(seed=17)
    assert 70 <= g.edge_count <= 90    # undirected ~40 = directed ~80

def test_build_graf_terhubung_penuh():
    g = build_traffic_graph(seed=17)
    assert g.is_connected() is True

def test_build_graf_node_a1_dan_e5_ada():
    g = build_traffic_graph(seed=17)
    assert "A1" in g
    assert "E5" in g

def test_build_graf_reprodusibel_dengan_seed_sama():
    g1 = build_traffic_graph(seed=17)
    g2 = build_traffic_graph(seed=17)
    assert g1.edge_count == g2.edge_count
    assert g1.get_weight("A1", "A2") == g2.get_weight("A1", "A2")

def test_build_graf_bobot_a1_a2_350_meter():
    g = build_traffic_graph(seed=17)
    assert g.get_weight("A1", "A2") == 350