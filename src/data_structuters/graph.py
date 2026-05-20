import random
import time


# ─────────────────────────────────────────────
# Node untuk Linked List adjacency list
# ─────────────────────────────────────────────
class EdgeNode:
    """Satu node dalam linked list adjacency list."""
    def __init__(self, destination: str, weight: float):
        self.destination = destination   # nama persimpangan tujuan
        self.weight = weight             # bobot jarak (meter)
        self.next = None                 # pointer ke edge berikutnya


# ─────────────────────────────────────────────
# Linked List sederhana untuk adjacency
# ─────────────────────────────────────────────
class AdjacencyList:
    """Linked list yang menyimpan semua tetangga sebuah node."""
    def __init__(self):
        self.head = None
        self._size = 0

    def add(self, destination: str, weight: float) -> None:
        """Tambah edge baru di depan list. Big-O: O(1)"""
        node = EdgeNode(destination, weight)
        node.next = self.head
        self.head = node
        self._size += 1

    def remove(self, destination: str) -> bool:
        """Hapus edge ke destination. Big-O: O(deg)"""
        prev, curr = None, self.head
        while curr:
            if curr.destination == destination:
                if prev:
                    prev.next = curr.next
                else:
                    self.head = curr.next
                self._size -= 1
                return True
            prev, curr = curr, curr.next
        return False

    def get_all(self) -> list:
        """Kembalikan semua (destination, weight) sebagai list. Big-O: O(deg)"""
        result = []
        curr = self.head
        while curr:
            result.append((curr.destination, curr.weight))
            curr = curr.next
        return result

    def size(self) -> int:
        return self._size

    def __iter__(self):
        curr = self.head
        while curr:
            yield curr.destination, curr.weight
            curr = curr.next


# ─────────────────────────────────────────────
# Graf Berbobot (Weighted Directed/Undirected)
# ─────────────────────────────────────────────
class TrafficGraph:
    """
    Graf berbobot menggunakan adjacency list berbasis Linked List.

    Attributes:
        _adj (dict): mapping nama_node -> AdjacencyList
        _nodes (set): kumpulan semua nama persimpangan

    Big-O Summary:
        add_intersection : O(1)
        add_road         : O(1)  [undirected → 2x O(1)]
        neighbors        : O(deg)
        degree           : O(deg)
        has_road         : O(deg)
        dfs              : O(V + E)
        is_connected     : O(V + E)
    """

    def __init__(self):
        self._adj: dict[str, AdjacencyList] = {}
        self._nodes: set = set()
        self._edge_count: int = 0

    # ── Manajemen Node ──────────────────────────────
    def add_intersection(self, name: str) -> None:
        """
        Tambah persimpangan (node) baru.
        Big-O: O(1)
        """
        if name not in self._adj:
            self._adj[name] = AdjacencyList()
            self._nodes.add(name)

    def remove_intersection(self, name: str) -> bool:
        """
        Hapus persimpangan beserta semua edge yang terhubung.
        Big-O: O(V + E) — harus cek semua adj list
        """
        if name not in self._nodes:
            return False
        del self._adj[name]
        self._nodes.remove(name)
        for node in self._nodes:
            if self._adj[node].remove(name):
                self._edge_count -= 1
        return True

    # ── Manajemen Edge ──────────────────────────────
    def add_road(self, src: str, dst: str, weight: float,
                 bidirectional: bool = True) -> None:
        """
        Tambah jalan (edge) antara dua persimpangan.
        Big-O: O(1) untuk directed; O(1) untuk undirected (2 operasi O(1))
        """
        self.add_intersection(src)
        self.add_intersection(dst)
        self._adj[src].add(dst, weight)
        self._edge_count += 1
        if bidirectional:
            self._adj[dst].add(src, weight)
            self._edge_count += 1

    def remove_road(self, src: str, dst: str,
                    bidirectional: bool = True) -> bool:
        """Hapus jalan antara dua persimpangan. Big-O: O(deg)"""
        removed = False
        if src in self._adj:
            removed = self._adj[src].remove(dst)
            if removed:
                self._edge_count -= 1
        if bidirectional and dst in self._adj:
            if self._adj[dst].remove(src):
                self._edge_count -= 1
        return removed

    # ── Query ────────────────────────────────────────
    def neighbors(self, node: str) -> list:
        """
        Kembalikan semua tetangga beserta bobotnya.
        Big-O: O(deg)
        """
        if node not in self._adj:
            return []
        return self._adj[node].get_all()

    def degree(self, node: str) -> int:
        """
        Kembalikan jumlah tetangga (degree) suatu node.
        Big-O: O(deg) — traversal linked list
        """
        if node not in self._adj:
            return 0
        return self._adj[node].size()

    def has_road(self, src: str, dst: str) -> bool:
        """Cek apakah edge src→dst ada. Big-O: O(deg)"""
        if src not in self._adj:
            return False
        for dest, _ in self._adj[src]:
            if dest == dst:
                return True
        return False

    def get_weight(self, src: str, dst: str) -> float | None:
        """Kembalikan bobot edge src→dst. Big-O: O(deg)"""
        if src not in self._adj:
            return None
        for dest, w in self._adj[src]:
            if dest == dst:
                return w
        return None

    # ── DFS (Traversal) ─────────────────────────────
    def dfs(self, start: str) -> list:
        """
        Depth-First Search dari node start.
        Big-O: O(V + E)
        Returns: urutan kunjungan node
        """
        if start not in self._nodes:
            return []
        visited = set()
        order = []
        self._dfs_recursive(start, visited, order)
        return order

    def _dfs_recursive(self, node: str, visited: set, order: list) -> None:
        visited.add(node)
        order.append(node)
        for neighbor, _ in self._adj[node]:
            if neighbor not in visited:
                self._dfs_recursive(neighbor, visited, order)

    def dfs_iterative(self, start: str) -> list:
        """DFS iteratif menggunakan Stack (untuk menghindari rekursi dalam). Big-O: O(V+E)"""
        if start not in self._nodes:
            return []
        visited = set()
        stack = [start]
        order = []
        while stack:
            node = stack.pop()
            if node in visited:
                continue
            visited.add(node)
            order.append(node)
            for neighbor, _ in self._adj[node]:
                if neighbor not in visited:
                    stack.append(neighbor)
        return order

    def is_connected(self) -> bool:
        """
        Cek apakah graf terhubung (semua node dapat dijangkau dari satu sumber).
        Big-O: O(V + E)
        """
        if not self._nodes:
            return True
        start = next(iter(self._nodes))
        visited = self.dfs(start)
        return len(visited) == len(self._nodes)

    def get_isolated_nodes(self) -> list:
        """Kembalikan node yang tidak punya tetangga. Big-O: O(V)"""
        return [n for n in self._nodes if self.degree(n) == 0]

    # ── Properti ────────────────────────────────────
    @property
    def node_count(self) -> int:
        return len(self._nodes)

    @property
    def edge_count(self) -> int:
        return self._edge_count

    @property
    def nodes(self) -> list:
        return sorted(self._nodes)

    def __contains__(self, node: str) -> bool:
        return node in self._nodes

    def __repr__(self) -> str:
        return (f"TrafficGraph(V={self.node_count}, "
                f"E={self.edge_count // 2} undirected edges)")


