# ============================================================
# dijkstra.py
# Smart Traffic Simulation – Dijkstra Algorithm
# ============================================================

import sys
import os
import time
import random

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from data_structures.graph import TrafficGraph, build_traffic_graph
from data_structures.priority_queue import MinHeap


INF = float("inf")


# ============================================================
# DIJKSTRA RESULT
# ============================================================
class DijkstraResult:
    """
    Menyimpan hasil lengkap satu pemanggilan Dijkstra.
    """

    def __init__(self, source: str, dist: dict, prev: dict, nodes: list):
        self.source = source
        self.dist = dist
        self.prev = prev
        self.nodes = nodes

    def path_to(self, destination: str) -> list:
        """
        Rekonstruksi jalur dari source ke destination.
        """
        if destination not in self.prev:
            if destination == self.source:
                return [self.source]
            return []

        path = []
        current = destination

        while current != self.source:
            path.append(current)
            current = self.prev[current]

        path.append(self.source)
        path.reverse()

        return path

    def distance_to(self, destination: str) -> float:
        """
        Ambil jarak shortest path ke destination.
        """
        return self.dist.get(destination, INF)

    def unreachable(self) -> list:
        """
        Node yang tidak bisa dijangkau dari source.
        """
        return [
            node
            for node in self.nodes
            if self.dist.get(node, INF) == INF
        ]

    def all_distances(self) -> dict:
        return self.dist

    def __repr__(self):
        return (
            f"DijkstraResult(source={self.source}, "
            f"reachable={len(self.nodes) - len(self.unreachable())})"
        )


# ============================================================
# DIJKSTRA SOLVER
# ============================================================
class DijkstraSolver:
    """
    Solver shortest path menggunakan algoritma Dijkstra.
    """

    def __init__(self, graph: TrafficGraph):
        self.graph = graph

    def solve(self, source: str) -> DijkstraResult:
        """
        Jalankan Dijkstra dari source.
        Big-O: O((V + E) log V)
        """

        if source not in self.graph:
            raise ValueError(f"Source '{source}' tidak ada di graph")

        dist = {
            node: INF
            for node in self.graph.nodes
        }

        prev = {}

        dist[source] = 0

        pq = MinHeap()
        pq.push((0, source))

        visited = set()

        while not pq.is_empty():

            current_dist, current = pq.pop()

            if current in visited:
                continue

            visited.add(current)

            for neighbor, weight in self.graph.neighbors(current):

                new_dist = current_dist + weight

                if new_dist < dist[neighbor]:
                    dist[neighbor] = new_dist
                    prev[neighbor] = current

                    pq.push((new_dist, neighbor))

        return DijkstraResult(
            source,
            dist,
            prev,
            self.graph.nodes
        )

    # ========================================================
    # Query Shortest Path
    # ========================================================
    def shortest_path(self, source: str, destination: str):

        result = self.solve(source)

        return (
            result.distance_to(destination),
            result.path_to(destination)
        )

    # ========================================================
    # Top-K shortest destination
    # ========================================================
    def top_k_routes(self, source: str, k: int = 5):

        result = self.solve(source)

        routes = []

        for node in self.graph.nodes:

            if node == source:
                continue

            d = result.distance_to(node)

            if d != INF:
                routes.append((
                    node,
                    d,
                    result.path_to(node)
                ))

        routes.sort(key=lambda x: x[1])

        return routes[:k]

    # ========================================================
    # Route Recommendation
    # ========================================================
    def route_recommendation(
        self,
        source: str,
        destination: str,
        congested: list | None = None
    ):

        congested = congested or []

        result = self.solve(source)

        path = result.path_to(destination)

        if any(node in congested for node in path):
            return INF, []

        return (
            result.distance_to(destination),
            path
        )


# ============================================================
# EXPERIMENT
# ============================================================
def run_experiments():

    print("\n" + "=" * 60)
    print("EKSPERIMEN RUNTIME - MODUL DIJKSTRA")
    print("=" * 60)

    g = build_traffic_graph(17)

    solver = DijkstraSolver(g)

    print(f"{'QUERY':<20} {'WAKTU (s)':<15}")
    print("-" * 60)

    queries = [
        ("A1", "E5"),
        ("A2", "D4"),
        ("B1", "E3"),
        ("C2", "A5"),
        ("D1", "B5"),
    ]

    for src, dst in queries:

        t0 = time.perf_counter()

        dist, path = solver.shortest_path(src, dst)

        runtime = time.perf_counter() - t0

        print(
            f"{src} -> {dst:<12} "
            f"{runtime:<15.6f}"
        )

    print("=" * 60)
    print("Kompleksitas:")
    print("  Dijkstra + MinHeap → O((V + E) log V)")
    print("=" * 60)


# ============================================================
# DEMO
# ============================================================
if __name__ == "__main__":

    print("=" * 60)
    print("MODUL 3 - DIJKSTRA SHORTEST PATH")
    print("SMART TRAFFIC SIMULATION")
    print("=" * 60)

    graph = build_traffic_graph(seed=17)

    solver = DijkstraSolver(graph)

    source = "A1"
    destination = "E5"

    dist, path = solver.shortest_path(
        source,
        destination
    )

    print(f"\nShortest Path {source} -> {destination}")
    print(f"Jarak : {dist} meter")
    print(f"Path  : {' -> '.join(path)}")

    print("\nTop 5 Rute Terdekat dari A1:")
    top5 = solver.top_k_routes("A1", 5)

    for node, d, p in top5:
        print(f"  {node:<4} | {d:<5} meter | {p}")

    run_experiments()