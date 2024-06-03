class HuffmanNode:
    def __init__(self, char, frequency):
        self.char = char
        self.frequency = frequency
        self.left = None
        self.right = None
class MinHeap:
    def __init__(self):
        # list of nodes
        self.heap = []
    def parent(self, i):
        return (i-1)//2
    def left_child(self, index):
        return 2 * index + 1

    def right_child(self, index):
        return 2 * index + 2

    def has_left_child(self, index):
        return self.left_child(index) < len(self.heap)

    def has_right_child(self, index):
        return self.right_child(index) < len(self.heap)

    def has_parent(self, index):
        return self.parent(index) >= 0

    def swap(self, index_one, index_two):
        self.heap[index_one], self.heap[index_two] = self.heap[index_two], self.heap[index_one]
    def heapify_up(self):
        index = len(self.heap) - 1
        #if parent is bigger than current
        while self.has_parent(index) and self.compare(self.heap[self.parent(index)], self.heap[index]) > 0:
            self.swap(index, self.parent(index))
            index = self.parent(index)
    def heapify_down(self):
        index = 0
        while self.has_left_child(index):
            #check is right child is smaller
            smaller_child_index = self.left_child(index)
            if self.has_right_child(index) and self.compare(self.heap[self.right_child(index)], self.heap[smaller_child_index]) < 0:
                smaller_child_index = self.right_child(index)
            #if current index is smaller than smaller child, all is good
            if self.compare(self.heap[index], self.heap[smaller_child_index]) < 0:
                break
            else:
                self.swap(index, smaller_child_index)
            index = smaller_child_index
    def add(self, letter: tuple[str, int]):
        self.heap.append(letter)
        self.heapify_up()
    def poll(self) -> HuffmanNode:
        if len(self.heap) == 0:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()
        item = self.heap[0]
        self.heap[0] = self.heap.pop()
        self.heapify_down()
        return item

    def compare(self, node1: HuffmanNode, node2: HuffmanNode) -> int:
        """
        return -1 if node 1 < node 2
        return 1 if node1 > node2
        """
        if node1.frequency < node2.frequency:
            return -1
        elif node1.frequency > node2.frequency:
            return 1
        else:
            if node1.char < node2.char:
                return -1
            elif node1.char > node2.char:
                return 1
            else:
                return 0
    def __str__(self):
        return str(self.heap)

def get_letters_frequencies_from_file(filename) -> list[HuffmanNode]:
    letters_frequencies = []
    with open(filename) as f:
        n = int(f.readline().strip())
        for letter_frequency in f:
            letter = letter_frequency.split(' ')[0]
            frequency = int(letter_frequency.split(' ')[1])
            letters_frequencies.append(HuffmanNode(letter, frequency))
    return letters_frequencies
def build_huffman_tree(letters_frequencies: list[HuffmanNode]):
    heap = MinHeap()
    nodes = get_letters_frequencies_from_file('huffman.txt')
    print(letters_frequencies)
    for node in letters_frequencies:
        heap.add(node)
    headNode = None
    while len(heap.heap) > 0:
        left = heap.poll()
        right = heap.poll()
        if right is None:
            return headNode
        else:
            newHead = HuffmanNode(left.char + right.char, left.frequency + right.frequency)
            newHead.left = left
            newHead.right = right
            heap.add(newHead)
            headNode = newHead
    return headNode
def get_codes_from_huffman_tree(headNode: HuffmanNode) -> dict[str, str]:
    codes = {}
    def traverse(node: HuffmanNode, code = ''):
        if node:
            if not node.left and not node.right:
                codes[node.char] = code
            traverse(node.left, code + '0')
            traverse(node.right, code + '1')
    traverse(headNode)
    return codes

if __name__ == '__main__':
    letters_frequencies = get_letters_frequencies_from_file('huffman.txt')
    huffmanTreeHead = build_huffman_tree(letters_frequencies)
    codes = get_codes_from_huffman_tree(huffmanTreeHead)
    for char, code in codes.items():
        print(char,' ', code)


