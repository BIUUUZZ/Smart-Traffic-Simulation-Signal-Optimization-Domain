import time
from graph import build_traffic_graph


# ─────────────────────────────────────────────
# Node BST
# ─────────────────────────────────────────────
class BSTNode:
    """Satu node dalam Binary Search Tree."""

    def __init__(self, key: str, data: dict = None):
        self.key = key
        self.data = data or {}
        self.left = None
        self.right = None

    def __repr__(self) -> str:
        return f"BSTNode({self.key})"


# ─────────────────────────────────────────────
# Binary Search Tree
# ─────────────────────────────────────────────
class IntersectionBST:

    def __init__(self):
        self._root = None
        self._size = 0

    # ─────────────────────────────
    # INSERT
    # ─────────────────────────────
    def insert(self, key: str, data: dict = None) -> bool:

        if self._root is None:
            self._root = BSTNode(key, data)
            self._size += 1
            return True

        return self._insert_recursive(self._root, key, data)

    def _insert_recursive(self, node, key, data):

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
            node.data.update(data or {})
            return False

   