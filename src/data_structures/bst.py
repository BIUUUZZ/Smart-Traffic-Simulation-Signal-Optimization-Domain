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

    # ─────────────────────────────
    # SEARCH
    # ─────────────────────────────
    def search(self, key: str):

        return self._search_recursive(self._root, key)

    def _search_recursive(self, node, key):

        if node is None:
            return None

        if key == node.key:
            return node

        elif key < node.key:
            return self._search_recursive(node.left, key)

        else:
            return self._search_recursive(node.right, key)

    def contains(self, key: str) -> bool:
        return self.search(key) is not None

    # ─────────────────────────────
    # DELETE
    # ─────────────────────────────
    def delete(self, key: str) -> bool:

        self._root, deleted = self._delete_recursive(self._root, key)

        if deleted:
            self._size -= 1

        return deleted

    def _delete_recursive(self, node, key):

        if node is None:
            return node, False

        deleted = False

        if key < node.key:

            node.left, deleted = self._delete_recursive(node.left, key)

        elif key > node.key:

            node.right, deleted = self._delete_recursive(node.right, key)

        else:

            deleted = True

            # tidak punya anak
            if node.left is None and node.right is None:
                return None, deleted

            # satu anak
            if node.left is None:
                return node.right, deleted

            if node.right is None:
                return node.left, deleted

            # dua anak
            successor = self._find_min(node.right)

            node.key = successor.key
            node.data = successor.data

            node.right, _ = self._delete_recursive(
                node.right,
                successor.key
            )

        return node, deleted

    # ─────────────────────────────
    # MIN & MAX
    # ─────────────────────────────
    def _find_min(self, node):

        while node.left is not None:
            node = node.left

        return node

    def _find_max(self, node):

        while node.right is not None:
            node = node.right

        return node

    # ─────────────────────────────
    # TRAVERSAL
    # ─────────────────────────────
    def inorder(self):

        result = []

        self._inorder_recursive(self._root, result)

        return result

    def _inorder_recursive(self, node, result):

        if node is None:
            return

        self._inorder_recursive(node.left, result)

        result.append((node.key, node.data))

        self._inorder_recursive(node.right, result)

    def preorder(self):

        result = []

        self._preorder_recursive(self._root, result)

        return result

    def _preorder_recursive(self, node, result):

        if node is None:
            return

        result.append(node.key)

        self._preorder_recursive(node.left, result)

        self._preorder_recursive(node.right, result)

    