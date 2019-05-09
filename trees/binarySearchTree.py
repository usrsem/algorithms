class Node:

    def __init__(self, key, *, parent=None, left=None, right=None):

        self.key = key
        self.parent = parent
        self.left = left
        self.right = right

    def has_right_child(self):

        return self.right is not None

    def has_left_child(self):

        return self.left is not None

    def is_left_child(self):

        return self.parent and self.parent.left == self

    def is_right_child(self):

        return self.parent and self.parent.right == self

    def is_root(self):

        return not self.parent

    def has_any_children(self):

        return self.right or self.left

    def has_both_children(self):

        return self.right and self.left

    def __repr__(self):

        return f'<Node:{self.key}>'

    def __str__(self):

        return self.__repr__()


def assert_node(node):

    assert isinstance(node, Node), \
        f'Node must be an instance of class Node. Passed: {type(node)}'


def right_ancestor(node):

    assert_node(node)

    if node.parent is None:
        return None

    if node.key < node.parent.key:
        return node.parent
    else:
        return right_ancestor(node.parent)


def left_ancestor(node):

    assert_node(node)

    if node.parent is None:
        return None

    if node.key > node.parent.key:
        return node.parent
    else:
        return left_ancestor(node.parent)


def left_descendant(node):

    assert_node(node)

    if node.left is None:
        return node
    else:
        return left_descendant(node.left)


def right_descendant(node):

    assert_node(node)

    if node.right is None:
        return node
    else:
        return right_descendant(node.right)


class BinarySearchTree:

    def __init__(self, root_node=None):

        self.root = root_node
        self.size = 0

    def find(self, key):

        found, node = self._find_or_parent(key)

        if found:
            return node

        return None

    def insert(self, key):

        found, parent = self._find_or_parent(key)

        if not found:
            node = Node(key, parent=parent)
            if parent is not None:
                if parent.key > key:
                    parent.left = node
                else:
                    parent.right = node
            else:  # root node
                self.root = node
            self.size += 1

    def insert_all(self, keys):

        for key in keys:
            self.insert(key)

    def delete(self, node):

        assert_node(node)

        self.size -= 1

        if not node.has_any_children():  # no children
            if node.is_left_child():
                node.parent.left = None
            elif node.is_right_child():
                node.parent.right = None
            else:
                self.root = None
        elif not node.has_both_children():  # only one child
            child = node.left if node.has_left_child() else node.right
            child.parent = node.parent
            if node.is_left_child():
                node.parent.left = child
            elif node.is_right_child():
                node.parent.right = child
            else:
                self.root = child
        else:  # two children
            next_node = self.next(node)

            node.left.parent = next_node
            next_node.left = node.left

            if node.is_left_child():
                node.parent.left = next_node
            elif node.is_right_child():
                node.parent.right = next_node
            else:
                self.root = next_node
            next_node.parent = node.parent

    def delete_by_key(self, key):

        node = self.find(key)
        if node:
            self.delete(node)

    def next(self, node):

        assert_node(node)

        if node.has_right_child():
            return left_descendant(node.right)
        else:
            return right_ancestor(node)

    def prev(self, node):

        assert_node(node)

        if node.has_left_child():
            return right_descendant(node.left)
        else:
            return left_ancestor(node)

    def find_range(self, left, right):

        result = []
        _, node = self._find_or_parent(left)

        while node and node.key <= right:
            if node.key >= left:
                result.append(node)
            node = self.next(node)

        return result

    def nearest_neighbour(self, key):

        found, node = self._find_or_parent(key)

        if found:
            return (self.prev(node), self.next(node))
        elif node.key < key:
            return (node, self.next(node))
        else:
            return (self.prev(node), node)

    def dfs(self, func):

        if self.root is None:
            return

        stack = [self.root]

        while stack:
            node = stack.pop()
            func(node)
            if node.has_right_child():
                stack.append(node.right)
            if node.has_left_child():
                stack.append(node.left)

    def bfs(self, func):

        if self.root is None:
            return

        stack = [self.root]

        while stack:
            node = stack.pop(0)
            func(node)
            if node.has_left_child():
                stack.append(node.left)
            if node.has_right_child():
                stack.append(node.right)

    def max(self):

        raise NotImplementedError()

    def min(self):

        raise NotImplementedError()

    def keys(self):

        keys = []
        self.bfs(lambda node: keys.append(node.key))

        keys.sort()

        return keys

    def _find_or_parent(self, key):

        node = self.root

        if node is None:
            return (False, None)

        while True:
            if node.key == key:
                return (True, node)
            if node.key > key:
                if not node.has_left_child():
                    return (False, node)
                node = node.left
            else:
                if not node.has_right_child():
                    return (False, node)
                node = node.right

    def __repr__(self):

        return f'<BST: root={self.root} size={self.size}>'

    def __str__(self):

        return self.__repr__()


def print_as_list(node):

    print(f'{node} -> {node.left}, {node.right}')
