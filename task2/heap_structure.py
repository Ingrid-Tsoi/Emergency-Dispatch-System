# heap_structure.py

class MaxHeap:
    def __init__(self):
        self.heap = []

    # Push item into heap
    def push(self, incident):
        self.heap.append(incident)
        self._heapify_up(len(self.heap) - 1)

    # Pop highest priority incident
    def pop(self):
        if not self.heap:
            return None
        self._swap(0, len(self.heap) - 1)
        max_item = self.heap.pop()
        self._heapify_down(0)
        return max_item

    # -----------------------------------
    # Helpers
    # -----------------------------------
    def _parent(self, i): return (i - 1) // 2
    def _left(self, i): return 2 * i + 1
    def _right(self, i): return 2 * i + 2

    def _swap(self, a, b):
        self.heap[a], self.heap[b] = self.heap[b], self.heap[a]

    def _heapify_up(self, i):
        while i > 0:
            p = self._parent(i)
            if self.heap[i].priority > self.heap[p].priority:
                self._swap(i, p)
                i = p
            else:
                break

    def _heapify_down(self, i):
        size = len(self.heap)
        while True:
            left = self._left(i)
            right = self._right(i)
            largest = i

            if left < size and self.heap[left].priority > self.heap[largest].priority:
                largest = left
            if right < size and self.heap[right].priority > self.heap[largest].priority:
                largest = right

            if largest == i:
                break

            self._swap(i, largest)
            i = largest


# Sorting example for Task 2 report
def heap_sort(incidents):
    heap = MaxHeap()
    for inc in incidents:
        heap.push(inc)

    sorted_list = []
    while True:
        item = heap.pop()
        if item is None:
            break
        sorted_list.append(item)

    return sorted_list