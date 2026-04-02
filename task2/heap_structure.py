class MaxHeap:
    def __init__(self):
        self.heap = []

    # -------------------------
    # Push
    # -------------------------
    def push(self, incident):
        self.heap.append(incident)
        self._heapify_up(len(self.heap) - 1)

    # -------------------------
    # Pop (max priority)
    # -------------------------
    def pop(self):
        if len(self.heap) == 0:
            return None

        # swap root with last
        self._swap(0, len(self.heap) - 1)
        max_item = self.heap.pop()

        # restore heap
        self._heapify_down(0)

        return max_item

    # -------------------------
    # Heapify Up
    # -------------------------
    def _heapify_up(self, index):
        while index > 0:
            parent = (index - 1) // 2

            if self.heap[index].priority > self.heap[parent].priority:
                self._swap(index, parent)
                index = parent
            else:
                break

    # -------------------------
    # Heapify Down
    # -------------------------
    def _heapify_down(self, index):
        size = len(self.heap)

        while True:
            left = 2 * index + 1
            right = 2 * index + 2
            largest = index

            # compare left
            if left < size and self.heap[left].priority > self.heap[largest].priority:
                largest = left

            # compare right
            if right < size and self.heap[right].priority > self.heap[largest].priority:
                largest = right

            # if no change → done
            if largest == index:
                break

            self._swap(index, largest)
            index = largest

    # -------------------------
    # Swap helper
    # -------------------------
    def _swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    # -------------------------
    # Build heap (for rebuild)
    # -------------------------
    def build(self, items):
        self.heap = items[:]

        # start from last non-leaf node
        for i in range(len(self.heap)//2 - 1, -1, -1):
            self._heapify_down(i)

    # -------------------------
    # Check empty
    # -------------------------
    def is_empty(self):
        return len(self.heap) == 0
    

# ------------------------==
# Heap Sort Algorithm
# ------------------------==
def heap_sort(items):
    heap = MaxHeap()
    
    # Build heap
    heap.build(items.copy())

    sorted_list = []

    # Extract max repeatedly
    while not heap.is_empty():
        sorted_list.append(heap.pop())

    return sorted_list