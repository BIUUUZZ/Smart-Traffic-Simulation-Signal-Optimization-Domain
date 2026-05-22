# ============================================================
# test_dijkstra.py
# Unit test untuk Smart Traffic Dijkstra
# Jalankan: pytest test/dijkstra.py -v
# ============================================================

import sys
import os
import random

sys.path.insert(
    0,
    os.path.join(os.path.dirname(__file__), "..", "src")
)

from data_structures.graph import TrafficGraph, build_traffic_graph
from data_structures.dijkstra import DijkstraSolver, INF


# ══════════════════════════════════════════════
# HELPER
# ══════════════════════════════════════════════

def make_simple_graph():
    """
    A --(4)-- B --(3)-- D
    |         |
   (2)       (1)
    |         |
    C --(5)-- E
    """

    g = TrafficGraph()

    g.add_road("A", "B", 4)
    g.add_road("A", "C", 2)
    g.add_road("B", "D", 3)
    g.add_road("B", "E", 1)
    g.add_road("C", "E", 5)

    return g


# ══════════════════════════════════════════════
# TEST DIJKSTRA RESULT
# ══════════════════════════════════════════════

def test_distance_benar():
    g = make_simple_graph()

    solver = DijkstraSolver(g)
    result = solver.solve("A")

    assert result.distance_to("A") == 0
    assert result.distance_to("B") == 4
    assert result.distance_to("C") == 2
    assert result.distance_to("D") == 7
    assert result.distance_to("E") == 5


def test_path_benar():
    g = make_simple_graph()

    solver = DijkstraSolver(g)
    result = solver.solve("A")

    assert result.path_to("D") == ["A", "B", "D"]
    assert result.path_to("E") == ["A", "B", "E"]
    assert result.path_to("A") == ["A"]


def test_node_tidak_terjangkau():
    g = TrafficGraph()

    g.add_road("X", "Y", 10)
    g.add_intersection("Z")

    solver = DijkstraSolver(g)
    result = solver.solve("X")

    assert result.distance_to("Z") == INF
    assert result.path_to("Z") == []
    assert "Z" in result.unreachable()


def test_all_distances():
    g = make_simple_graph()

    result = DijkstraSolver(g).solve("A")

    all_d = result.all_distances()

    assert isinstance(all_d, dict)
    assert all_d["A"] == 0
    assert all_d["C"] == 2


# ══════════════════════════════════════════════
# TEST SHORTEST PATH
# ══════════════════════════════════════════════

def test_shortest_path():
    g = make_simple_graph()

    solver = DijkstraSolver(g)

    dist, path = solver.shortest_path("A", "D")

    assert dist == 7
    assert path == ["A", "B", "D"]


def test_source_target_sama():
    g = make_simple_graph()

    solver = DijkstraSolver(g)

    dist, path = solver.shortest_path("B", "B")

    assert dist == 0
    assert path == ["B"]


def test_source_tidak_ada():
    g = make_simple_graph()

    solver = DijkstraSolver(g)

    try:
        solver.shortest_path("SALAH", "D")
        assert False
    except ValueError:
        assert True


# ══════════════════════════════════════════════
# TEST TOP K ROUTES
# ══════════════════════════════════════════════

def test_top_k_routes():
    g = make_simple_graph()

    solver = DijkstraSolver(g)

    top3 = solver.top_k_routes("A", k=3)

    assert len(top3) == 3

    assert top3[0][1] <= top3[1][1]
    assert top3[1][1] <= top3[2][1]


# ══════════════════════════════════════════════
# TEST ROUTE RECOMMENDATION
# ══════════════════════════════════════════════

def test_route_recommendation_normal():
    g = make_simple_graph()

    solver = DijkstraSolver(g)

    dist, path = solver.route_recommendation("A", "D")

    assert dist == 7
    assert path == ["A", "B", "D"]


def test_route_recommendation_hindari_macet():
    g = make_simple_graph()

    solver = DijkstraSolver(g)

    dist, path = solver.route_recommendation(
        "A",
        "D",
        congested=["B"]
    )

    assert dist == INF or "B" not in path


