import time
import sys
import os

# Import dari modul lain dalam proyek
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from data_structures.graph import TrafficGraph, build_traffic_graph
from data_structures.priority_queue import MinHeap


# ─────────────────────────────────────────────
# Konstanta
# ─────────────────────────────────────────────
INF = float("inf")


# ─────────────────────────────────────────────
# Hasil Dijkstra
# ─────────────────────────────────────────────
class DijkstraResult:
    """Menyimpan hasil lengkap satu pemanggilan Dijkstra."""

    def __init__(self, source: str, dist: dict, prev: dict, nodes: list):
        self.source = source
        self._dist  = dist   # {node: jarak_minimum}
        self._prev  = prev   # {node: predecessor}
        self._nodes = nodes

    def distance_to(self, target: str) -> float:
        """Kembalikan jarak minimum ke target."""
        return self._dist.get(target, INF)

    def path_to(self, target: str) -> list:
        """
        Rekonstruksi jalur terpendek dari source ke target.
        Big-O: O(V) — trace-back predecessor
        """
        if self._dist.get(target, INF) == INF:
            return []          # tidak terjangkau
        path = []
        curr = target
        while curr is not None:
            path.append(curr)
            curr = self._prev.get(curr)
        path.reverse()
        return path

    def all_distances(self) -> dict:
        """Kembalikan semua jarak sebagai dict."""
        return dict(self._dist)

    def unreachable(self) -> list:
        """Kembalikan daftar node yang tidak terjangkau."""
        return [n for n in self._nodes if self._dist.get(n, INF) == INF]

    def summary_table(self) -> str:
        """Tampilkan tabel ringkasan jarak dari source."""
        lines = [
            f"\n{'Tujuan':<10} {'Jarak (m)':<14} {'Jalur'}",
            "-" * 55,
        ]
        for node in sorted(self._nodes):
            d = self._dist.get(node, INF)
            p = self.path_to(node)
            dist_str = f"{d:.0f}" if d != INF else "∞ (tidak terjangkau)"
            path_str = " → ".join(p) if p else "-"
            lines.append(f"{node:<10} {dist_str:<14} {path_str}")
        return "\n".join(lines)

    def __repr__(self) -> str:
        reachable = sum(1 for d in self._dist.values() if d != INF)
        return (f"DijkstraResult(source={self.source}, "
                f"reachable={reachable}/{len(self._nodes)})")


# ─────────────────────────────────────────────
# Algoritma Dijkstra
# ─────────────────────────────────────────────
class DijkstraSolver:
    """
    Solver Dijkstra menggunakan Min-Heap (dari Modul 2).

    Cara kerja:
    1. Inisialisasi dist[source]=0, semua lain=∞
    2. Masukkan (0, source) ke min-heap
    3. Selama heap tidak kosong:
       a. Keluarkan (d, u) terkecil
       b. Jika d > dist[u] → skip (sudah diproses)
       c. Untuk setiap tetangga v dengan bobot w:
          - Jika dist[u]+w < dist[v] → relaxasi, update heap
    4. Rekonstruksi jalur via predecessor dict

    Big-O: O((V + E) log V) dengan Min-Heap
    """

    def __init__(self, graph: TrafficGraph):
        self.graph = graph

    def solve(self, source: str) -> DijkstraResult:
        """
        Jalankan Dijkstra dari source ke semua node.
        Big-O: O((V + E) log V)

        Returns:
            DijkstraResult dengan jarak dan predecessor
        """
        if source not in self.graph:
            raise ValueError(f"Persimpangan '{source}' tidak ada di graf")

        nodes = self.graph.nodes
        dist  = {n: INF for n in nodes}
        prev  = {n: None for n in nodes}
        dist[source] = 0.0

        # Min-heap: elemen = (jarak, nama_node)
        # key_fn mengambil elemen pertama tuple (jarak)
        heap = MinHeap(key_fn=lambda x: (x[0], x[1]))
        heap.push((0.0, source))

        visited = set()

        while not heap.is_empty():
            d, u = heap.pop()

            if u in visited:
                continue           # sudah diproses dengan jarak lebih kecil
            visited.add(u)

            # Relaxasi semua tetangga
            for v, w in self.graph.neighbors(u):
                alt = d + w
                if alt < dist[v]:
                    dist[v] = alt
                    prev[v] = u
                    heap.push((alt, v))

        return DijkstraResult(source, dist, prev, nodes)

    def shortest_path(self, source: str, target: str) -> tuple:
        """
        Shortcut: hitung jarak dan jalur antara dua node.

        Returns:
            (jarak, [jalur]) atau (INF, []) jika tidak terjangkau
        """
        result = self.solve(source)
        return result.distance_to(target), result.path_to(target)

    def top_k_routes(self, source: str, k: int = 3) -> list:
        """
        Kembalikan k persimpangan terdekat dari source.
        Returns: list of (node, distance, path)
        """
        result = self.solve(source)
        pairs = [
            (n, result.distance_to(n), result.path_to(n))
            for n in self.graph.nodes
            if n != source and result.distance_to(n) != INF
        ]
        pairs.sort(key=lambda x: x[1])
        return pairs[:k]

    def route_recommendation(self, source: str, target: str,
                             congested: list = None) -> tuple:
        """
        Rekomendasikan rute alternatif dengan menghapus sementara
        persimpangan yang macet dari perhitungan.

        Args:
            congested: list persimpangan yang dianggap macet

        Returns:
            (jarak, jalur) tanpa melewati persimpangan macet
        """
        if not congested:
            return self.shortest_path(source, target)

        # Buat subgraf sementara tanpa node macet
        temp = TrafficGraph()
        for n in self.graph.nodes:
            if n not in congested:
                temp.add_intersection(n)
        for n in self.graph.nodes:
            if n in congested:
                continue
            for nbr, w in self.graph.neighbors(n):
                if nbr not in congested:
                    temp.add_road(n, nbr, w, bidirectional=False)

        solver_alt = DijkstraSolver(temp)
        try:
            return solver_alt.shortest_path(source, target)
        except ValueError:
            return INF, []


# ─────────────────────────────────────────────
# Eksperimen Runtime (50 query rute)
# ─────────────────────────────────────────────
def run_experiments(graph: TrafficGraph) -> None:
    """
    Eksperimen 50 query Dijkstra untuk N = 10, 25, 100 node simulatif.
    """
    import random
    print("\n" + "="*60)
    print("EKSPERIMEN RUNTIME - MODUL 3: DIJKSTRA")
    print("="*60)
    print(f"{'N node':<10} {'50 query (s)':<18} {'Rata-rata/query (s)'}")
    print("-"*50)

    for n in [10, 25, 100]:
        # Graf sementara n node
        import sys, os
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
        from graph import TrafficGraph as TG
        g_test = TG()
        nodes = [f"N{i}" for i in range(n)]
        for nd in nodes:
            g_test.add_intersection(nd)
        random.seed(17)
        for _ in range(n * 2):
            s = random.choice(nodes)
            d = random.choice(nodes)
            g_test.add_road(s, d, random.randint(100, 1500))

        solver = DijkstraSolver(g_test)
        t0 = time.perf_counter()
        for _ in range(50):
            src = random.choice(nodes)
            solver.solve(src)
        t_total = time.perf_counter() - t0

        print(f"{n:<10} {t_total:<18.6f} {t_total/50:<.6f}")

    print("="*60)
    print("Big-O: O((V + E) log V) per query Dijkstra")
    print("="*60)


# ─────────────────────────────────────────────
# Demo standalone
# ─────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("MODUL 3: DIJKSTRA RUTE OPTIMAL")
    print("Topik 7 – Smart Traffic Simulation")
    print("=" * 60)

    g = build_traffic_graph(seed=17)
    solver = DijkstraSolver(g)

    # Query tunggal
    src, dst = "A1", "E5"
    dist, path = solver.shortest_path(src, dst)
    print(f"\nRute terpendek {src} → {dst}:")
    print(f"  Jarak : {dist:.0f} meter")
    print(f"  Jalur : {' → '.join(path)}")

    # Semua jarak dari A1
    result = solver.solve("A1")
    print(result.summary_table())

    # Rekomendasi alternatif (A2 dan B2 macet)
    congested = ["A2", "B2"]
    dist_alt, path_alt = solver.route_recommendation(src, dst, congested)
    print(f"\nRute alternatif (hindari {congested}):")
    print(f"  Jarak : {dist_alt:.0f} meter" if dist_alt != INF else "  Tidak ada rute alternatif")
    if path_alt:
        print(f"  Jalur : {' → '.join(path_alt)}")

    # Top-3 terdekat dari A1
    print("\nTop-3 persimpangan terdekat dari A1:")
    for node, d, p in solver.top_k_routes("A1", k=3):
        print(f"  {node}: {d:.0f}m via {' → '.join(p)}")

    run_experiments(g)
    