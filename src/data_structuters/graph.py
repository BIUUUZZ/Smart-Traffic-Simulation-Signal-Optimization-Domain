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

