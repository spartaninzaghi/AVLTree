"""
Project 6
CSE 331 FS23
Gabriel Sotelo
starter.py
"""
import math
from typing import TypeVar, Generator, List, Tuple, Optional
from collections import deque
import json
from queue import SimpleQueue

# for more information on typehinting, check out https://docs.python.org/3/library/typing.html
T = TypeVar("T")  # represents generic type
# represents a Node object (forward-declare to use in Node __init__)
Node = TypeVar("Node")
# represents a custom type used in application
AVLWrappedDictionary = TypeVar("AVLWrappedDictionary")


class Node:
    """
    Implementation of an BST and AVL tree node.
    Do not modify.
    """
    # preallocate storage: see https://stackoverflow.com/questions/472000/usage-of-slots
    __slots__ = ["value", "parent", "left", "right", "height"]

    def __init__(self, value: T, parent: Node = None,
                 left: Node = None, right: Node = None) -> None:
        """
        Construct an AVL tree node.

        :param value: value held by the node object
        :param parent: ref to parent node of which this node is a child
        :param left: ref to left child node of this node
        :param right: ref to right child node of this node
        """
        self.value = value
        self.parent, self.left, self.right = parent, left, right
        self.height = 0

    def __repr__(self) -> str:
        """
        Represent the AVL tree node as a string.

        :return: string representation of the node.
        """
        return f"<{str(self.value)}>"

    def __str__(self) -> str:
        """
        Represent the AVL tree node as a string.

        :return: string representation of the node.
        """
        return repr(self)


####################################################################################################

class BinarySearchTree:
    """
    Implementation of an BSTree.
    Modify only below indicated line.
    """

    # preallocate storage: see https://stackoverflow.com/questions/472000/usage-of-slots
    __slots__ = ["origin", "size"]

    def __init__(self) -> None:
        """
        Construct an empty BST tree.
        """
        self.origin = None
        self.size = 0

    def __repr__(self) -> str:
        """
        Represent the BSTree as a string.

        :return: string representation of the BST tree
        """
        if self.origin is None:
            return "Empty BST Tree"

        lines = pretty_print_binary_tree(self.origin, 0, False, '-')[0]
        return "\n" + "\n".join((line.rstrip() for line in lines))

    def __str__(self) -> str:
        """
        Represent the BSTree as a string.

        :return: string representation of the BSTree
        """
        return repr(self)

    def visualize(self, filename="bst_visualization.svg"):
        """
        Generates an svg image file of the binary tree.

        :param filename: The filename for the generated svg file. Should end with .svg.
        Defaults to output.svg
        """
        svg_string = svg(self.origin, node_radius=20)
        print(svg_string, file=open(filename, 'w'))
        return svg_string

    ########################################
    # Implement functions below this line. #
    ########################################

    def height(self, root: Node) -> int:
        """
        Get the height of the node, `root`
        :param root: The root node of the BST
        :return: The height of `root`
        """
        # Null parent has -1 height
        if root is None:
            return -1
        return root.height

    def max(self, root: Node) -> Optional[Node]:
        """
        Return the node containing the maximum value in the BST
        :param root: The subtree whose maximum node is to be determined
        :return: The root of the the resulting subtree post removal
        """
        if root and root.right:
            return self.max(root.right)
        return root

    def insert(self, root: Node, val: T) -> None:
        """
        Inserts a node with the value `val` into the subtree rooted at
        root & returns the root of the balanced subtree after the insertion

        :param root: The root of the subtree where the value is to be inserted
        :param val: The value to insert
        :return: None
        """
        #  -------- Case 0 : Value becomes root of empty BST --------
        if root is None:
            self.origin = Node(val)
            self.size += 1
            return

        # ----- Case 1A : Value becomes left child of parent ------
        if val < root.value:
            if root.left is None:
                root.left = Node(val, root)
                self.size += 1
            else:
                self.insert(root.left, val)

        # ----- Case 1B : Value becomes right child of parent -----
        elif val > root.value:
            if root.right is None:
                root.right = Node(val, root)
                self.size += 1
            else:
                self.insert(root.right, val)

        # Case 2: Value already in BST, do nothing
        else:
            return None

        # Adjust the node height to the new max value
        root.height = 1 + max(self.height(root.left), self.height(root.right))

        # Adjust the origin height to its new max value
        self.origin.height = 1 + max(self.height(self.origin.left), self.height(self.origin.right))

    def remove(self, root: Node, val: T) -> Optional[Node]:
        """
        Removes the node containing the specified value from the subtree
        rooted at `root` and returns the root of the subtree after removal

        :param root: The root of the subtree where the value is to be removed
        :param val: The value to remove
        :return: The root of the the resulting subtree post removal
        """
        found_node = self.search(root, val)
        # ------------  CASE 0 : Unsuccessful Search ------------
        if found_node is None or found_node.value != val:
            pass # do nothing
        # ---------------- CASE 1 : Leaf Node -------------------
        elif found_node.right is None and found_node.left is None:
            par = found_node.parent
            # Update parent (reset origin if parent is origin & update parent's L/R child)
            if par is None:
                self.origin = None
            elif par.right and par.right.value == val:
                par.right = None
            else:
                par.left = None
            self.size -= 1
            par.height = 1 + max(self.height(par.left), self.height(par.right))
        # ---------------- CASE 2 : One Child -----------------
        elif found_node.right is None or found_node.left is None:
            par = found_node.parent
            child = found_node.right if found_node.right else found_node.left
            # Update parent (promote single child to position of current node)
            if par is None:
                self.origin = child
            elif par.right and par.right.value == val:
                par.right = child
            else:
                par.left = child
            child.parent = par # Update child (promote single child)
            self.size -= 1
            par.height = 1 + max(self.height(par.left), self.height(par.right))
        # -------------- CASE 3 : Two children (else) -------------
        else:
            successor = self.max(found_node.left)   # Successor is max node in its left subtree.
            self.remove(successor, successor.value) # Temporarily Remove Successor from BST
            found_node.value = successor.value      # placing it at the position of the root


    def search(self, root: Node, val: T) -> Optional[Node]:
        """
        Searches for and returns the node containing the value `val`
        in the subtree rooted at `root`. If `val` is not found in the
        subtree, the potential parent of `val` is returned

        :param root: The root of the subtree in which to search for `val`
        :param val: The value to search for
        :return: The node containing `val` if found else potential parent
        """
        # Case 0 : ------- Empty BST or Value Found --------
        if root is None or val == root.value:
            return root

        # Case 1A : --------- Recurse left subtree ---------
        if val < root.value:
            if root.left:  # root has left subtree
                return self.search(root.left, val)
            return root  # root lacks left subtree

        # Case 1B : --------- Recurse Right Subtree --------
        else:
            if root.right:  # root has left subtree
                return self.search(root.right, val)
            return root  # root lacks right subtree




class AVLTree:
    """
    Implementation of an AVL tree.
    Modify only below indicated line.
    """

    __slots__ = ["origin", "size"]

    def __init__(self) -> None:
        """
        Construct an empty AVL tree.
        """
        self.origin = None
        self.size = 0

    def __repr__(self) -> str:
        """
        Represent the AVL tree as a string.

        :return: string representation of the AVL tree
        """
        if self.origin is None:
            return "Empty AVL Tree"

        return super(AVLTree, self).__repr__()

    def __str__(self) -> str:
        """
        Represent the AVLTree as a string.

        :return: string representation of the BSTree
        """
        return repr(self)

    def visualize(self, filename="avl_tree_visualization.svg"):
        """
        Generates an svg image file of the binary tree.

        :param filename: The filename for the generated svg file. Should end with .svg.
        Defaults to output.svg
        """
        svg_string = svg(self.origin, node_radius=20)
        print(svg_string, file=open(filename, 'w'))
        return svg_string

    ########################################
    # Implement functions below this line. #
    ########################################

    def height(self, root: Node) -> int:
        """
        Get the height of the node, `root`
        :param root: The root node of the AVL
        :return: The height of `root`
        """
        # Null parent has -1 height
        if root is None:
            return -1
        return root.height

    def left_rotate(self, root: Node) -> Optional[Node]:
        """
        Rotate a right-right (RR) imbalanced subtree to the left
        :param root: The subtree to left rotate
        :return: The root of the left rotated subtree
        """
        # Left rotation successor : Right child of unbalanced node
        successor = root.right if root else None
        sacrifice = successor.left if successor else None

        # If the unbalanced node has a valid right child to succeed it
        if successor:
            # Successor takes root's place
            successor.parent = root.parent

            # If root is not the origin
            if root.parent:
                if root is root.parent.left:
                    root.parent.left = successor  # make successor left child of root's parent
                else:
                    root.parent.right = successor # make successor right child of root's parent
            else:
                self.origin = successor

            # Demote the unbalanced root to be successor's left child
            root.parent = successor
            successor.left = root

            # Give the successor's left child to the demoted root as its right child
            root.right = sacrifice
            if sacrifice:
                sacrifice.parent = root

            # # update root as the successor
            # root = successor

            # Adjust the node height to the new max value
            root.height = 1 + max(self.height(root.left), self.height(root.right))

            # Adjust the origin height to its new max value
            successor.height = 1 + max(self.height(successor.left), self.height(successor.right))
            return successor

        return root

    def right_rotate(self, root: Node) -> Optional[Node]:
        """
        Rotate a left-left (LL) imbalanced subtree to the right
        :param root: The subtree to right rotate
        :return: The root of the right rotated subtree
        """
        # Right rotation successor : Left child of unbalanced node
        successor = root.left if root else None
        sacrifice = successor.right if successor else None

        if successor:
            # Successor takes root's place
            successor.parent = root.parent

            # Root is not origin
            if root.parent:
                # Root is left child of its parent
                if root is root.parent.left:
                    root.parent.left = successor  # make successor left child of root's parent
                else:
                    root.parent.right = successor # make successor right child of root's parent
            else:
                self.origin = successor

            # Demote root to be successor's right child
            root.parent = successor
            successor.right = root

            # Give the successor's right child to the demoted root as its left child
            root.left = sacrifice
            if sacrifice:
                sacrifice.parent = root

            # # update root as the successor
            # root = successor

            # Adjust the node height to the new max value
            root.height = 1 + max(self.height(root.left), self.height(root.right))

            # Adjust the origin height to its new max value
            successor.height = 1 + max(self.height(successor.left), self.height(successor.right))
            return successor

        return root

    def balance_factor(self, root: Node) -> int:
        """
        Determine the balace factor of `root`, given by the height of its
        left subtree minus the height of its right subtree
        :param root: The node whose balance factor is to be determined
        :return: An integer representing the balance factor of `root`
        """
        return self.height(root.left) - self.height(root.right) if root else 0

    def rebalance(self, root: Node) -> Optional[Node]:
        """
        Perform appropriate appropriate rotations to balance `root`
        if it exhibits LL, RR, LR, or RL imbalance
        :param root: The node to rebalance
        :return: The root the new, potentially rebalanced subtree
        """
        # Case 0
        if -1 <= self.balance_factor(root) <= 1:
            return root

        # CASE 1 | LL : Right Rotation to balance
        if self.balance_factor(root) > 1:
            if self.balance_factor(root.left) <= -1:
                root_of_1st_rot = self.left_rotate(root.left) # CASE 3 | LR 2X Rotation
                return self.right_rotate(root_of_1st_rot.parent)
            return self.right_rotate(root)

        # CASE 2 | RR: Left Rotation to balance
        elif self.balance_factor(root) < -1:
            if self.balance_factor(root.right) >= 1:
                root_of_1st_rot = self.right_rotate(root.right) # CASE 4 | RL 2X Rotation
                return self.left_rotate(root_of_1st_rot.parent)
            return self.left_rotate(root)

    def insert(self, root: Node, val: T) -> Optional[Node]:
        """
        Inserts a node with the value `val` into the subtree rooted at
        root & returns the root of the balanced subtree after the insertion

        :param root: The root of the subtree where the value is to be inserted
        :param val: The value to insert
        :return: The root of the balanced subtree post insertion
        """
        #  -------- Case 0 : Value becomes root of empty BST --------
        if root is None:
            self.origin = Node(val)
            self.size += 1
            return self.origin

        # ----- Case 1A : Value becomes left child of parent ------
        elif val < root.value:
            if root.left is None:
                root.left = Node(val, root)
                self.size += 1
            else:
                self.insert(root.left, val) # recurse left subtree of root

        # ----- Case 1B : Value becomes right child of parent -----
        elif val > root.value:
            if root.right is None:
                root.right = Node(val, root)
                self.size += 1
            else:
                self.insert(root.right, val) # recurse right subtree of root

        # Case 2: Value already in BST, do nothing
        else:
            pass

        # Adjust the node height to its new max value
        root.height = 1 + max(self.height(root.left), self.height(root.right))

        # Adjust the origin height to its new max value
        self.origin.height = 1 + max(self.height(self.origin.left), self.height(self.origin.right))

        return self.rebalance(root)

    def remove(self, root: Node, val: T) -> Optional[Node]:
        """
        Removes the node containing the specified value from the subtree
        rooted at `root`, balances the subtree as needed, and returns the
        root of the resulting subtree post removal

        :param root: The root of the subtree where the value is to be removed
        :param val: The value to remove
        :return: The root of the the resulting subtree post removal
        """
        if root is None:  # Leaf reached
            return None
        elif val < root.value:  # Value in left subtree
            root.left = self.remove(root.left, val)
        elif val > root.value:  # Value in right subtree
            root.right = self.remove(root.right, val)
        else:
            # Value found : Delete it
            if root.left is None:
                if root.parent is None:  # update origin
                    self.origin = root.right
                if root.right is not None:  # update right child as parent
                    root.right.parent = root.parent
                self.size -= 1
                return root.right
            elif root.right is None:
                if root.parent is None:  # update origin
                    self.origin = root.left
                if root.left is not None:  # update left child as parent
                    root.left.parent = root.parent
                self.size -= 1
                return root.left
            else:
                # two children: swap with predecessor and delete predecessor
                predecessor = self.max(root.left)
                root.value = predecessor.value
                root.left = self.remove(root.left, predecessor.value)

        # update height and rebalance every node that was traversed in recursive deletion
        root.height = 1 + max(self.height(root.left), self.height(root.right))
        return self.rebalance(root)

    def min(self, root: Node) -> Optional[Node]:
        """
        Return the node containing the minimum value in the AVL
        :param root: The subtree whose minimum is to be determined
        :return: The node with the minimum value in the AVL
        """
        if root and root.left:
            return self.min(root.left)
        return root

    def max(self, root: Node) -> Optional[Node]:
        """
        Return the node containing the maximum value in the AVL
        :param root: The subtree whose maximum node is to be determined
        :return: The node with the maximum value in the AVL
        """
        if root and root.right:
            return self.max(root.right)
        return root

    def search(self, root: Node, val: T) -> Optional[Node]:
        """
        Searches for and returns the node containing the value `val`
        in the subtree rooted at `root`. If `val` is not found in the
        subtree, the potential parent of `val` is returned

        :param root: The root of the subtree in which to search for `val`
        :param val: The value to search for
        :return: The node containing `val` if found else potential parent
        """
        # Case 0 : ------- Empty BST or Value Found --------
        if root is None or val == root.value:
            return root

        # Case 1A : --------- Recurse left subtree ---------
        if val < root.value:
            if root.left:  # root has left subtree
                return self.search(root.left, val)
            return root  # root lacks left subtree

        # Case 1B : --------- Recurse Right Subtree --------
        else:
            if root.right:  # root has left subtree
                return self.search(root.right, val)
            return root  # root lacks right subtree

    def inorder(self, root: Node) -> Generator[Node, None, None]:
        """
        perform an inorder traversal (left, current, right) of the subtree
        rooted at `root`, generating the nodes one at a time using a Python
        generator
        :param root: The root of the subtree to traverse
        :return: An inorder generator
        """
        if root is not None:
            yield from self.inorder(root.left)
            yield root
            yield from self.inorder(root.right)

    def __iter__(self) -> Generator[Node, None, None]:
        """
        Make the AVL tree iterable
        :return: A generator to enable iteration
        """
        yield from self.inorder(self.origin)

    def preorder(self, root: Node) -> Generator[Node, None, None]:
        """
        Perform a preorder traversal (current, left, right) of the subtree
        rooted at `root`, generating the nodes one at a time using a Python
        generator
        :param root: The root of the subtree to traverse
        :return: A pre order generator
        """
        if root:
            yield root
            yield from self.preorder(root.left)
            yield from self.preorder(root.right)

    def postorder(self, root: Node) -> Generator[Node, None, None]:
        """
        Perform a postorder traversal (left, right, current) of the subtree
        rooted at `root`, generating the nodes one at a time using a Python
        generator
        :param root: The root of the subtree to traverse
        :return: A post order generator
        """
        if root:
            yield from self.postorder(root.left)
            yield from self.postorder(root.right)
            yield root


    def levelorder(self, root: Node) -> Generator[Node, None, None]:
        """
        Perform a level-order (breadth-first) traversal of the subtree
        rooted at `root`, generating the nodes one at a time using a
        Python generator
        :param root: The root of the subtree to traverse
        :return: A level order generator
        """
        if root is None:
            return

        sq = SimpleQueue()
        sq.put(root)

        while not sq.empty():
            curr = sq.get()

            if curr:
                yield curr
                sq.put(curr.left)
                sq.put(curr.right)


####################################################################################################


class AVLWrappedDictionary:
    """
    Implementation of a helper class which will be used as tree node values in the
    NearestNeighborClassifier implementation.
    """
    # preallocate storage: see https://stackoverflow.com/questions/472000/usage-of-slots
    __slots__ = ["key", "dictionary"]

    def __init__(self, key: float) -> None:
        """
        Construct a AVLWrappedDictionary with a key to search/sort on and a dictionary to hold data.

        :param key: floating point key to be looked up by.
        """
        self.key = key
        self.dictionary = {}

    def __repr__(self) -> str:
        """
        Represent the AVLWrappedDictionary as a string.

        :return: string representation of the AVLWrappedDictionary.
        """
        pprinted_dict = json.dumps(self.dictionary, indent=2)
        return f"key: {self.key} dict:{self.dictionary}"

    def __str__(self) -> str:
        """
        Represent the AVLWrappedDictionary as a string.

        :return: string representation of the AVLWrappedDictionary.
        """
        return repr(self)

    def __eq__(self, other: AVLWrappedDictionary) -> bool:
        """
        Implement == operator to compare 2 AVLWrappedDictionaries by key only.

        :param other: other AVLWrappedDictionary to compare with
        :return: boolean indicating whether keys of AVLWrappedDictionaries are equal
        """
        return abs(self.key - other.key) < 1e-6

    def __lt__(self, other: AVLWrappedDictionary) -> bool:
        """
        Implement < operator to compare 2 AVLWrappedDictionarys by key only.

        :param other: other AVLWrappedDictionary to compare with
        :return: boolean indicating ordering of AVLWrappedDictionaries
        """
        return self.key < other.key and not abs(self.key - other.key) < 1e-6

    def __gt__(self, other: AVLWrappedDictionary) -> bool:
        """
        Implement > operator to compare 2 AVLWrappedDictionaries by key only.

        :param other: other AVLWrappedDictionary to compare with
        :return: boolean indicating ordering of AVLWrappedDictionaries
        """
        return self.key > other.key and not abs(self.key - other.key) < 1e-6


class NearestNeighborClassifier:
    """
    Implementation of a one-dimensional nearest-neighbor classifier with AVL tree lookups.
    Modify only below indicated line.
    """
    # preallocate storage: see https://stackoverflow.com/questions/472000/usage-of-slots
    __slots__ = ["resolution", "tree"]

    def __init__(self, resolution: int) -> None:
        """
        Construct a one-dimensional nearest neighbor classifier with AVL tree lookups.
        Data are assumed to be floating point values in the closed interval [0, 1].

        :param resolution: number of decimal places the data will be rounded to, effectively
                           governing the capacity of the model - for example, with a resolution of
                           1, the classifier could maintain up to 11 nodes, spaced 0.1 apart - with
                           a resolution of 2, the classifier could maintain 101 nodes, spaced 0.01
                           apart, and so on - the maximum number of nodes is bounded by
                           10^(resolution) + 1.
        """
        self.tree = AVLTree()
        self.resolution = resolution

        # pre-construct lookup tree with AVLWrappedDictionary objects storing (key, dictionary)
        # pairs, but which compare with <, >, == on key only
        for i in range(10 ** resolution + 1):
            w_dict = AVLWrappedDictionary(key=(i / 10 ** resolution))
            self.tree.insert(self.tree.origin, w_dict)

    def __repr__(self) -> str:
        """
        Represent the NearestNeighborClassifier as a string.

        :return: string representation of the NearestNeighborClassifier.
        """
        return f"NNC(resolution={self.resolution}):\n{self.tree}"

    def __str__(self) -> str:
        """
        Represent the NearestNeighborClassifier as a string.

        :return: string representation of the NearestNeighborClassifier.
        """
        return repr(self)

    def visualize(self, filename: str = "nnc_visualization.svg") -> str:
        svg_string = svg(self.tree.origin, 48, nnc_mode=True)
        print(svg_string, file=open(filename, 'w'))
        return svg_string

    ########################################
    # Implement functions below this line. #
    ########################################

    def key(self, k: float) -> float:
        """
        Generate a valid key that can be wrapped in an AVLWrappedDictionary
        and searched for in the NNC's AVL tree. The valid key is rounded to
        the precision specified by the resolution
        :param k: The key to round
        :return: The key rounded to precision of the resolution
        """
        return round(k, self.resolution)

    def feature(self, k: float) -> AVLWrappedDictionary:
        """
        Generate a valid feature key that can be searched for in the NNC's AVL tree
        :param k: The key that owns the generated AVLWrappedDictionary feature
        :return: `k` wrapped in an AVLWrappedDictionary
        """
        return AVLWrappedDictionary(key=self.key(k))

    def get_valid_keys(self, x: float, delta: float) -> set[float]:
        """
        Generate a set of keys that are within the range of `± delta` of `x`
        :param x: The feature key to train the NNC model on
        :return: A set of keys that are valid neighbors or `x`
        """
        return { self.key(x) + delta * i for i in range(-1, 2)
                 if 0 <= self.key(x) + delta * i <= 1 } # Set eliminates duplicate keys


    def fit(self, data: List[Tuple[float, str]]) -> None:
        """
        Train the NNC's AVL tree using a training dataset of  `(x,y)` pairs, where `x`
        is a feature and `y` is the target label.
        :param data: The training data as a list of `(feature, label)` or `(x,y)` pairs
        :return: None
        """
        for x, y in data:
            labels = self.tree.search(self.tree.origin, self.feature(x)).value
            if labels.key != self.key(x) : continue
            labels.dictionary[y] = labels.dictionary[y] + 1 if y in labels.dictionary else 1


    def predict(self, x: float, delta: float) -> str:
        """
        Predict the modal (most frequent) label for a testing  dataset of `x` values based
        on the patterns learned during the training phase using the `fit()` method of the NNC
        :param x: The feature key to train the NNC model on
        :param delta: The allowable distance of `x'`s neighbors away from x in the NNC's AVL tree
        :return: The modal (most frequent) label
        """
        counts = {}                                    # Because of x+delta, x, x-delta the
        for neighbor in self.get_valid_keys(x, delta): # for loop only ever iterates up to 3 times
            labels = self.tree.search(self.tree.origin, self.feature(neighbor)).value # O(logn)
            if labels.key != self.key(neighbor):
                continue
            for y in labels.dictionary:
                counts[y] = counts[y] + labels.dictionary[y] if y in counts else labels.dictionary[y]
        return max(counts, key=counts.get) if counts else None  # same runtime as using for loop for max

        # l = self.key(x) - delta
        # m = self.key(x)
        # h = self.key(x) + delta
        #
        # low_neighbor = self.tree.search(self.tree.origin, self.feature(l)).value if 0 <= l <= 1 else None
        # mid_neighbor = self.tree.search(self.tree.origin, self.feature(m)).value if 0 <= m <= 1 else None
        # hgh_neighbor = self.tree.search(self.tree.origin, self.feature(h)).value if 0 <= h <= 1 else None
        #
        # if low_neighbor:
        #     for y in low_neighbor.dictionary:
        #         if y in counts:
        #             counts[y] += low_neighbor.dictionary[y]
        #         else:
        #             counts[y] = low_neighbor.dictionary[y]
        #
        # if mid_neighbor:
        #     for y in mid_neighbor.dictionary:
        #         if y in counts:
        #             counts[y] += mid_neighbor.dictionary[y]
        #         else:
        #             counts[y] = mid_neighbor.dictionary[y]
        #
        # if hgh_neighbor:
        #     for y in hgh_neighbor.dictionary:
        #         if y in counts:
        #             counts[y] += hgh_neighbor.dictionary[y]
        #         else:
        #             counts[y] = hgh_neighbor.dictionary[y]
        # return max(counts, key=counts.get) if counts else None  # same runtime as using for loop for max


####################################################################################################


"""
For the curious students, the following functions are used to visualize and compare the performance
of BinarySearchTree and AVLTree under extreme conditions. You do not need to modify (or run) these 
functions, but you are welcome to play around with them if you wish. 

You should know that AVLTree is faster than BinarySearchTree in the worst case, but how much faster?
The following functions will help you answer this question, shall you choose to try them out.

Uncomment the line under "if __name__ == '__main__':" to run the performance comparison (after completing
the rest of the project) and you will be greeted with a plot of the results. The function will require
matplotlib, make sure to install it if you do not have it already.
"""


def compare_times(structure: dict, sizes: List[int], trial: int) -> dict:
    """
    Comparing time on provide data structures in the worst case of BST tree
    :param structure: provided data structures
    :param sizes: size of test input
    :param trial: number of trials to test
    :return: dict with list of average times per input size for each algorithm
    """
    import sys
    import time
    result = {}
    sys.stdout.write('\r')
    sys.stdout.write('Start...\n')
    total = len(sizes) * len(structure)
    count = 0
    for algorithm, value in structure.items():
        ImplementedTree = value
        if algorithm not in result:
            result[algorithm] = []
        for size in sizes:
            sum_times = 0
            for _ in range(trial):
                tree = ImplementedTree()
                start = time.perf_counter()
                for i in range(size):
                    tree.insert(tree.origin, i)
                for i in range(size, -1, -1):
                    tree.remove(tree.origin, i)
                end = time.perf_counter()
                sum_times += (end - start)
            count += 1
            result[algorithm].append(sum_times / trial)
            sys.stdout.write("[{:<20s}] {:d}%\n".format('=' * ((count * 20) // total),
                                                        count * 100 // total))
            sys.stdout.flush()
    return result


def plot_time_comparison():
    """
    Use compare_times to make a time comparison of normal binary search tree and AVL tree
    in a worst case scenario.
    Requires matplotlib. Comment this out if you do not wish to install matplotlib.
    """
    import matplotlib.pyplot as plt
    import sys
    sys.setrecursionlimit(2010)
    structures = {
        "bst": BinarySearchTree,
        "avl": AVLTree
    }
    sizes = [4, 5, 6, 7, 8, 9, 10, 25, 50, 100, 300, 500, 1000, 2000]
    trials = 5
    data = compare_times(structures, sizes, trials)

    plt.style.use('seaborn-colorblind')
    plt.figure(figsize=(12, 8))

    for structure in structures:
        plt.plot(sizes, data[structure], label=structure)
    plt.legend()
    plt.xlabel("Input Size")
    plt.ylabel("Time to Sort (sec)")
    plt.title("BST vs AVL")
    plt.show()


_SVG_XML_TEMPLATE = """
<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
<style>
    .value {{
        font: 300 16px monospace;
        text-align: center;
        dominant-baseline: middle;
        text-anchor: middle;
    }}
    .dict {{
        font: 300 16px monospace;
        dominant-baseline: middle;
    }}
    .node {{
        fill: lightgray;
        stroke-width: 1;
    }}
</style>
<g stroke="#000000">
{body}
</g>
</svg>
"""

_NNC_DICT_BOX_TEXT_TEMPLATE = """<text class="dict" y="{y}" xml:space="preserve">
    <tspan x="{label_x}" dy="1.2em">{label}</tspan>
    <tspan x="{bracket_x}" dy="1.2em">{{</tspan>
    {values}
    <tspan x="{bracket_x}" dy="1.2em">}}</tspan>
</text>
"""


def pretty_print_binary_tree(root: Node, curr_index: int, include_index: bool = False,
                             delimiter: str = "-", ) -> \
        Tuple[List[str], int, int, int]:
    """
    Taken from: https://github.com/joowani/binarytree

    Recursively walk down the binary tree and build a pretty-print string.
    In each recursive call, a "box" of characters visually representing the
    current (sub)tree is constructed line by line. Each line is padded with
    whitespaces to ensure all lines in the box have the same length. Then the
    box, its width, and start-end positions of its root node value repr string
    (required for drawing branches) are sent up to the parent call. The parent
    call then combines its left and right sub-boxes to build a larger box etc.
    :param root: Root node of the binary tree.
    :type root: binarytree.Node | None
    :param curr_index: Level-order_ index of the current node (root node is 0).
    :type curr_index: int
    :param include_index: If set to True, include the level-order_ node indexes using
        the following format: ``{index}{delimiter}{value}`` (default: False).
    :type include_index: bool
    :param delimiter: Delimiter character between the node index and the node
        value (default: '-').
    :type delimiter:
    :return: Box of characters visually representing the current subtree, width
        of the box, and start-end positions of the repr string of the new root
        node value.
    :rtype: ([str], int, int, int)
    .. _Level-order:
        https://en.wikipedia.org/wiki/Tree_traversal#Breadth-first_search
    """
    if root is None:
        return [], 0, 0, 0

    line1 = []
    line2 = []
    if include_index:
        node_repr = "{}{}{}".format(curr_index, delimiter, root.value)
    else:
        if type(root.value) == AVLWrappedDictionary:
            node_repr = f'{root.value},h={root.height},' \
                        f'⬆{str(root.parent.value.key) if root.parent else "None"}'
        else:
            node_repr = f'{root.value},h={root.height},' \
                        f'⬆{str(root.parent.value) if root.parent else "None"}'

    new_root_width = gap_size = len(node_repr)

    # Get the left and right sub-boxes, their widths, and root repr positions
    l_box, l_box_width, l_root_start, l_root_end = pretty_print_binary_tree(
        root.left, 2 * curr_index + 1, include_index, delimiter
    )
    r_box, r_box_width, r_root_start, r_root_end = pretty_print_binary_tree(
        root.right, 2 * curr_index + 2, include_index, delimiter
    )

    # Draw the branch connecting the current root node to the left sub-box
    # Pad the line with whitespaces where necessary
    if l_box_width > 0:
        l_root = (l_root_start + l_root_end) // 2 + 1
        line1.append(" " * (l_root + 1))
        line1.append("_" * (l_box_width - l_root))
        line2.append(" " * l_root + "/")
        line2.append(" " * (l_box_width - l_root))
        new_root_start = l_box_width + 1
        gap_size += 1
    else:
        new_root_start = 0

    # Draw the representation of the current root node
    line1.append(node_repr)
    line2.append(" " * new_root_width)

    # Draw the branch connecting the current root node to the right sub-box
    # Pad the line with whitespaces where necessary
    if r_box_width > 0:
        r_root = (r_root_start + r_root_end) // 2
        line1.append("_" * r_root)
        line1.append(" " * (r_box_width - r_root + 1))
        line2.append(" " * r_root + "\\")
        line2.append(" " * (r_box_width - r_root))
        gap_size += 1
    new_root_end = new_root_start + new_root_width - 1

    # Combine the left and right sub-boxes with the branches drawn above
    gap = " " * gap_size
    new_box = ["".join(line1), "".join(line2)]
    for i in range(max(len(l_box), len(r_box))):
        l_line = l_box[i] if i < len(l_box) else " " * l_box_width
        r_line = r_box[i] if i < len(r_box) else " " * r_box_width
        new_box.append(l_line + gap + r_line)

    # Return the new box, its width and its root repr positions
    return new_box, len(new_box[0]), new_root_start, new_root_end


def svg(root: Node, node_radius: int = 16, nnc_mode=False) -> str:
    """
    Taken from: https://github.com/joowani/binarytree

    Generate SVG XML.
    :param root: Generate SVG for tree rooted at root
    :param node_radius: Node radius in pixels (default: 16).
    :type node_radius: int
    :return: Raw SVG XML.
    :rtype: str
    """
    tree_height = root.height
    scale = node_radius * 3
    xml = deque()
    nodes_for_nnc_visualization: list[AVLWrappedDictionary] = []

    def scale_x(x: int, y: int) -> float:
        diff = tree_height - y
        x = 2 ** (diff + 1) * x + 2 ** diff - 1
        return 1 + node_radius + scale * x / 2

    def scale_y(y: int) -> float:
        return scale * (1 + y)

    def add_edge(parent_x: int, parent_y: int, node_x: int, node_y: int) -> None:
        xml.appendleft(
            '<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>'.format(
                x1=scale_x(parent_x, parent_y),
                y1=scale_y(parent_y),
                x2=scale_x(node_x, node_y),
                y2=scale_y(node_y),
            )
        )

    def add_node(node_x: int, node_y: int, node: Node) -> None:
        x, y = scale_x(node_x, node_y), scale_y(node_y)
        xml.append(
            f'<circle class="node" cx="{x}" cy="{y}" r="{node_radius}"/>')

        if nnc_mode:
            nodes_for_nnc_visualization.append(node.value)
            xml.append(
                f'<text class="value" x="{x}" y="{y + 5}">key={node.value.key}</text>')
        else:
            xml.append(
                f'<text class="value" x="{x}" y="{y + 5}">{node.value}</text>')

    current_nodes = [root.left, root.right]
    has_more_nodes = True
    y = 1

    add_node(0, 0, root)

    while has_more_nodes:

        has_more_nodes = False
        next_nodes: List[Node] = []

        for x, node in enumerate(current_nodes):
            if node is None:
                next_nodes.append(None)
                next_nodes.append(None)
            else:
                if node.left is not None or node.right is not None:
                    has_more_nodes = True

                add_edge(x // 2, y - 1, x, y)
                add_node(x, y, node)

                next_nodes.append(node.left)
                next_nodes.append(node.right)

        current_nodes = next_nodes
        y += 1

    svg_width = scale * (2 ** tree_height)
    svg_height = scale * (2 + tree_height)
    if nnc_mode:

        line_height = 20
        box_spacing = 10
        box_margin = 5
        character_width = 10

        max_key_count = max(
            map(lambda obj: len(obj.dictionary), nodes_for_nnc_visualization))
        box_height = (max_key_count + 3) * line_height + box_margin

        def max_length_item_of_node_dict(node: AVLWrappedDictionary):
            # Check if dict is empty so max doesn't throw exception
            if len(node.dictionary) > 0:
                item_lengths = map(lambda pair: len(
                    str(pair)), node.dictionary.items())
                return max(item_lengths)
            return 0

        max_value_length = max(
            map(max_length_item_of_node_dict, nodes_for_nnc_visualization))
        box_width = max(max_value_length * character_width, 110)

        boxes_per_row = svg_width // box_width
        rows_needed = math.ceil(
            len(nodes_for_nnc_visualization) / boxes_per_row)

        nodes_for_nnc_visualization.sort(key=lambda node: node.key)
        for index, node in enumerate(nodes_for_nnc_visualization):
            curr_row = index // boxes_per_row
            curr_column = index % boxes_per_row

            box_x = curr_column * (box_width + box_spacing)
            box_y = curr_row * (box_height + box_spacing) + svg_height
            box = f'<rect x="{box_x}" y="{box_y}" width="{box_width}" ' \
                  f'height="{box_height}" fill="white" />'
            xml.append(box)

            value_template = '<tspan x="{value_x}" dy="1.2em">{key}: {value}</tspan>'
            text_x = box_x + 10

            def item_pair_to_svg(pair):
                return value_template.format(key=pair[0], value=pair[1], value_x=text_x + 10)

            values = map(item_pair_to_svg, node.dictionary.items())
            text = _NNC_DICT_BOX_TEXT_TEMPLATE.format(
                y=box_y,
                label=f"key = {node.key}",
                label_x=text_x,
                bracket_x=text_x,
                values='\n'.join(values)
            )
            xml.append(text)

        svg_width = boxes_per_row * (box_width + box_spacing * 2)
        svg_height += rows_needed * (box_height + box_spacing * 2)

    return _SVG_XML_TEMPLATE.format(
        width=svg_width,
        height=svg_height,
        body="\n".join(xml),
    )


if __name__ == "__main__":
    # plot_time_comparison()
    pass
