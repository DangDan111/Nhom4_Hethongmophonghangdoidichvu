class PriorityQueueHeap:
    def __init__(self, max_size=50):
        self.max_size = max_size
        self.heap = []

    def push(self, khach_hang):
        if self.is_full():
            return False
        self.heap.append(khach_hang)
        self._heapify_up(len(self.heap) - 1)
        return True

    def pop(self):
        if self.is_empty():
            return None
        if len(self.heap) == 1:
            return self.heap.pop()
        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._heapify_down(0)
        return root

    def peek(self):
        if self.is_empty():
            return None
        return self.heap[0]

    def is_empty(self):
        return len(self.heap) == 0

    def is_full(self):
        return len(self.heap) >= self.max_size

    def size(self):
        return len(self.heap)

    def to_list(self):
        ban_sao = PriorityQueueHeap(self.max_size)
        ban_sao.heap = self.heap.copy()
        ket_qua = []
        while not ban_sao.is_empty():
            ket_qua.append(ban_sao.pop())
        return ket_qua

    def _heapify_up(self, index):
        while index > 0:
            parent = (index - 1) // 2
            if self._uu_tien_cao_hon(self.heap[index], self.heap[parent]):
                self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
                index = parent
            else:
                break

    def _heapify_down(self, index):
        while True:
            left = index * 2 + 1
            right = index * 2 + 2
            smallest = index

            if left < len(self.heap) and self._uu_tien_cao_hon(self.heap[left], self.heap[smallest]):
                smallest = left
            if right < len(self.heap) and self._uu_tien_cao_hon(self.heap[right], self.heap[smallest]):
                smallest = right
            if smallest == index:
                break

            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            index = smallest

    def _uu_tien_cao_hon(self, a, b):
        if a.muc_do_uu_tien != b.muc_do_uu_tien:
            return a.muc_do_uu_tien < b.muc_do_uu_tien
        if a.thoi_gian_den != b.thoi_gian_den:
            return a.thoi_gian_den < b.thoi_gian_den
        return a.id < b.id
