import time
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from graph import build_traffic_graph


# ─────────────────────────────────────────────
# Node BST
# ─────────────────────────────────────────────
class BSTNode:
    """Satu node dalam Binary Search Tree."""

    def __init__(self, key: str, data: dict = None):
        self.key   = key          # nama persimpangan (string)
        self.data  = data or {}   # metadata persimpangan (opsional)
        self.left  = None         # anak kiri  (key < self.key)
        self.right = None         # anak kanan (key > self.key)

    def __repr__(self) -> str:
        return f"BSTNode({self.key})"


# ─────────────────────────────────────────────
# Binary Search Tree
# ─────────────────────────────────────────────
class IntersectionBST:
    """
    BST untuk indeks persimpangan berdasarkan nama (string).

    Properti BST:
    - Semua node di subtree kiri < root
    - Semua node di subtree kanan > root
    - In-order traversal → urutan alfabet

    Big-O:
        insert  : O(log n) rata-rata, O(n) worst-case (pohon condong)
        search  : O(log n) rata-rata, O(n) worst-case
        delete  : O(log n) rata-rata
        inorder : O(n)
        height  : O(n)
    """

    def __init__(self):
        self._root: BSTNode | None = None
        self._size: int = 0

    # ── Insert ──────────────────────────────────
    def insert(self, key: str, data: dict = None) -> bool:
        """
        Sisipkan node baru ke BST.
        Big-O: O(log n) rata-rata
        Returns: True jika berhasil, False jika key sudah ada.
        """
        if self._root is None:
            self._root = BSTNode(key, data)
            self._size += 1
            return True
        return self._insert_recursive(self._root, key, data)

    def _insert_recursive(self, node: BSTNode, key: str, data: dict) -> bool:
        if key < node.key:
            if node.left is None:
                node.left = BSTNode(key, data)
                self._size += 1
                return True
            return self._insert_recursive(node.left, key, data)
        elif key > node.key:
            if node.right is None:
                node.right = BSTNode(key, data)
                self._size += 1
                return True
            return self._insert_recursive(node.right, key, data)
        else:
            # Key sudah ada → update data
            node.data.update(data or {})
            return False

    # ── Search ──────────────────────────────────
    def search(self, key: str) -> BSTNode | None:
        """
        Cari persimpangan berdasarkan nama.
        Big-O: O(log n) rata-rata
        Returns: BSTNode jika ditemukan, None jika tidak.
        """
        return self._search_recursive(self._root, key)

    def _search_recursive(self, node: BSTNode | None, key: str) -> BSTNode | None:
        if node is None:
            return None
        if key == node.key:
            return node
        elif key < node.key:
            return self._search_recursive(node.left, key)
        else:
            return self._search_recursive(node.right, key)

    def contains(self, key: str) -> bool:
        """Cek apakah key ada di BST. Big-O: O(log n) rata-rata"""
        return self.search(key) is not None

    # ── Delete ──────────────────────────────────
    def delete(self, key: str) -> bool:
        """
        Hapus node dengan key dari BST.
        Big-O: O(log n) rata-rata
        """
        root, deleted = self._delete_recursive(self._root, key)
        self._root = root
        if deleted:
            self._size -= 1
        return deleted

    def _delete_recursive(self, node: BSTNode | None, key: str):
        if node is None:
            return node, False

        deleted = False
        if key < node.key:
            node.left, deleted = self._delete_recursive(node.left, key)
        elif key > node.key:
            node.right, deleted = self._delete_recursive(node.right, key)
        else:
            deleted = True
            # Kasus 1: node daun
            if node.left is None and node.right is None:
                return None, deleted
            # Kasus 2: satu anak
            if node.left is None:
                return node.right, deleted
            if node.right is None:
                return node.left, deleted
            # Kasus 3: dua anak → ganti dengan successor (min di subtree kanan)
            successor = self._find_min(node.right)
            node.key  = successor.key
            node.data = successor.data
            node.right, _ = self._delete_recursive(node.right, successor.key)

        return node, deleted

    def _find_min(self, node: BSTNode) -> BSTNode:
        """Temukan node dengan key terkecil di subtree. Big-O: O(log n)"""
        while node.left is not None:
            node = node.left
        return node

    def _find_max(self, node: BSTNode) -> BSTNode:
        """Temukan node dengan key terbesar di subtree. Big-O: O(log n)"""
        while node.right is not None:
            node = node.right
        return node

    # ── Traversal ───────────────────────────────
    def inorder(self) -> list:
        """
        In-order traversal → daftar persimpangan terurut alfabet.
        Big-O: O(n)
        """
        result = []
        self._inorder_recursive(self._root, result)
        return result

    def _inorder_recursive(self, node: BSTNode | None, result: list) -> None:
        if node is None:
            return
        self._inorder_recursive(node.left, result)
        result.append((node.key, node.data))
        self._inorder_recursive(node.right, result)

    def preorder(self) -> list:
        """Pre-order traversal. Big-O: O(n)"""
        result = []
        self._preorder_recursive(self._root, result)
        return result

    def _preorder_recursive(self, node: BSTNode | None, result: list) -> None:
        if node is None:
            return
        result.append(node.key)
        self._preorder_recursive(node.left, result)
        self._preorder_recursive(node.right, result)

    def range_query(self, low: str, high: str) -> list:
        """
        Kembalikan semua persimpangan dengan nama antara low dan high (inklusif).
        Big-O: O(log n + k) di mana k = jumlah hasil
        """
        result = []
        self._range_recursive(self._root, low, high, result)
        return result

    def _range_recursive(self, node: BSTNode | None,
                         low: str, high: str, result: list) -> None:
        if node is None:
            return
        if low <= node.key <= high:
            self._range_recursive(node.left, low, high, result)
            result.append((node.key, node.data))
            self._range_recursive(node.right, low, high, result)
        elif node.key < low:
            self._range_recursive(node.right, low, high, result)
        else:
            self._range_recursive(node.left, low, high, result)

    # ── Properti ────────────────────────────────
    def height(self) -> int:
        """Tinggi pohon. Big-O: O(n)"""
        return self._height_recursive(self._root)

    def _height_recursive(self, node: BSTNode | None) -> int:
        if node is None:
            return 0
        return 1 + max(
            self._height_recursive(node.left),
            self._height_recursive(node.right)
        )

    @property
    def size(self) -> int:
        return self._size

    def is_empty(self) -> bool:
        return self._root is None

    def min_key(self) -> str | None:
        if self._root is None:
            return None
        return self._find_min(self._root).key

    def max_key(self) -> str | None:
        if self._root is None:
            return None
        return self._find_max(self._root).key

    # ── Visualisasi sederhana ────────────────────
    def print_tree(self, node: BSTNode = None, prefix: str = "",
                   is_left: bool = True) -> None:
        """Tampilkan struktur pohon secara visual."""
        if node is None:
            node = self._root
        if node is None:
            print("(empty)")
            return

        connector = "├── " if is_left else "└── "
        print(prefix + connector + node.key)

        children_prefix = prefix + ("│   " if is_left else "    ")
        if node.left or node.right:
            if node.left:
                self.print_tree(node.left, children_prefix, True)
            else:
                print(children_prefix + "├── (null)")
            if node.right:
                self.print_tree(node.right, children_prefix, False)
            else:
                print(children_prefix + "└── (null)")

    def __repr__(self) -> str:
        return f"IntersectionBST(size={self._size}, height={self.height()})"


# ─────────────────────────────────────────────
# Builder: Bangun BST dari Graf
# ─────────────────────────────────────────────
def build_intersection_bst(graph) -> IntersectionBST:
    """
    Bangun BST indeks persimpangan dari TrafficGraph.
    Data tiap node menyimpan degree persimpangan.
    """
    bst = IntersectionBST()
    for name in graph.nodes:
        bst.insert(name, {"degree": graph.degree(name)})
    return bst


# ─────────────────────────────────────────────
# Eksperimen Runtime
# ─────────────────────────────────────────────
def run_experiments() -> None:
    """Eksperimen insert/search BST untuk N = 10, 25, 100."""
    import random
    import string

    print("\n" + "="*60)
    print("EKSPERIMEN RUNTIME - MODUL 4: BST")
    print("="*60)
    print(f"{'N node':<10} {'insert (s)':<18} {'search (s)':<18} {'inorder (s)'}")
    print("-"*60)

    for n in [10, 25, 100]:
        random.seed(17)
        keys = [f"{''.join(random.choices(string.ascii_uppercase, k=2))}{i}"
                for i in range(n)]

        bst = IntersectionBST()

        # Insert
        t0 = time.perf_counter()
        for k in keys:
            bst.insert(k)
        t_ins = time.perf_counter() - t0

        # Search (semua key)
        t0 = time.perf_counter()
        for k in keys:
            bst.search(k)
        t_srch = time.perf_counter() - t0

        # Inorder
        t0 = time.perf_counter()
        bst.inorder()
        t_inord = time.perf_counter() - t0

        print(f"{n:<10} {t_ins:<18.6f} {t_srch:<18.6f} {t_inord:.6f}")

    print("="*60)
    print("Big-O: insert O(log n), search O(log n), inorder O(n)")
    print("="*60)


# ─────────────────────────────────────────────
# Demo standalone
# ─────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("MODUL 4: BST INDEKS PERSIMPANGAN")
    print("Topik 7 – Smart Traffic Simulation")
    print("=" * 60)

    g = build_traffic_graph(seed=17)
    bst = build_intersection_bst(g)

    print(f"\nBST dibangun: {bst}")
    print(f"Tinggi pohon : {bst.height()}")
    print(f"Key minimum  : {bst.min_key()}")
    print(f"Key maksimum : {bst.max_key()}")

    # Search
    target = "C3"
    node = bst.search(target)
    if node:
        print(f"\nDitemukan '{target}': degree={node.data.get('degree')}")
    else:
        print(f"\n'{target}' tidak ditemukan")

    # Inorder (terurut)
    print(f"\nDaftar persimpangan terurut (inorder):")
    inorder_list = [key for key, _ in bst.inorder()]
    print("  " + ", ".join(inorder_list))

    # Range query
    low, high = "B1", "C5"
    print(f"\nRange query '{low}' – '{high}':")
    for key, data in bst.range_query(low, high):
        print(f"  {key}: degree={data.get('degree', 0)}")

    # Delete
    bst.delete("C3")
    print(f"\nSetelah delete 'C3': size={bst.size}, contains='C3':{bst.contains('C3')}")

    # Visualisasi pohon kecil (5 node saja)
    small_bst = IntersectionBST()
    for k in ["C3", "B1", "D5", "A2", "C1"]:
        small_bst.insert(k)
    print("\nStruktur BST kecil (demo):")
    small_bst.print_tree()

    run_experiments()