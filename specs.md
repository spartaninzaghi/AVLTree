# Project 6: AVL Trees

**Due: November 16th, 2023 @ 9:00pm**

_This is not a team project. Do not copy someone else’s work._

## Assignment Overview

[AVL trees](https://en.wikipedia.org/wiki/AVL_tree), named after computer scientists Georgy Adelson-Velsky and Evgenii Landis who introduced them in 1962, are a type of self-balancing [binary search tree (BST)](https://en.wikipedia.org/wiki/Binary_search_tree) designed to maintain operations in logarithmic time irrespective of data insertion and deletion patterns. Their introductory paper, "[An algorithm for the organization of information](https://zhjwpku.com/assets/pdf/AED2-10-avl-paper.pdf)," stands as a testament to their enduring relevance, especially in applications requiring a space-efficient data structure with quick insertion, search, and deletion capabilities.

![AVL Tree Animation](img/avl.gif)

A critical issue often encountered with traditional BSTs is their tendency to become _unbalanced_ depending on the order of data insertion and deletion, leading to operations taking linear time instead of logarithmic. For instance, inserting data in a sorted (or reverse-sorted) sequence results in a BST that resembles a linked list, with leaves growing predominantly in one direction.

![BST Balancing Issue](img/balance.png)

While this may not pose significant challenges with small datasets, the performance gap between logarithmic and linear time becomes staggeringly evident when dealing with large databases comprising thousands or millions of records.

![Logarithmic vs. Linear Growth](img/bigogrowth.png)

By self-balancing, AVL trees ensure that operations consistently take logarithmic time, providing a robust solution to the issues faced by traditional BSTs. In this project, you are tasked with implementing both a traditional BST and an AVL tree from the ground up in Python. Utilizing the AVL tree, you will address a machine learning-inspired application problem.

## Assignment Notes

1. **Generators for Space-Efficient Traversal**: In this project, you will employ Python `Generator` objects for tree traversal. This approach is notably space-efficient compared to returning a list of nodes (`List[Node]`), as it consumes _O(1)_ space instead of _O(n)_. Generators yield nodes sequentially and on-demand, providing a streamlined and memory-efficient solution. For a comprehensive introduction to Python generators, you can refer to [this article](https://realpython.com/introduction-to-python-generators/).

2. **Updating Heights and Balancing**: A prevalent mistake in this project is the omission or incorrect update of node heights, as well as improper tree rebalancing within insert and remove functions. Ensure to meticulously read the notes we've provided under each function's description in the specifications. Reflect on how recursion and the call stack can be leveraged to rebalance the tree, especially in relation to the node you've just inserted or removed.

3. **Simplifying AVL Trees**: While AVL Trees are inherently complex, breaking down each function into specific cases or checks can significantly simplify the implementation. Consider all possible scenarios for each operation, such as checking if the node you're working on is the root, or verifying the presence of a right node before proceeding with `node.right`. Ensure that you're updating the correct pointers throughout the process.

4. **Leveraging the Debugger**: Don’t hesitate to use the debugger; it is an invaluable tool, especially for deciphering the behavior of complex functions. Taking the time to familiarize yourself with its features will pay off, helping you verify whether your code is executing as expected and identifying any discrepancies in your logic.

5. **Utilizing Visualization Functions**: To aid in understanding your tree's structure, we have provided visualization and printing functions. You can easily visualize your tree by calling `tree.visualize()` on an instance of BinarySearch, AVLTree, or NearestNeighborClassifier. While we've done our best to ensure the accuracy of these visualizations, we acknowledge that they may not be flawless. If you encounter any issues, please let us know.

6. **Avoiding Global Variables**: Utilizing global variables (with the `nonlocal` keyword) in your implementation will result in a deduction of 20 points.

7. **Maintaining Function Signatures**: Altering the signatures of provided functions will lead to a deduction of 2 points per instance, accumulating up to a maximum of 20 points.

8. **Considering Inheritance**: Although this project could benefit from a reduction in duplicate code through the use of inheritance, we opted to keep the syntax straightforward and avoid additional object-oriented complexity. Nonetheless, it's a valuable exercise to ponder how the AVLTree class might be implemented as a subclass of the BinarySearchTree class, promoting code reuse between the two.

9. **Performance Comparison**: After completing the implementation of all BinarySearchTree and AVLTree functions, running the `solution.py` file will present a performance comparison between the two types of trees, showcasing the efficiency gains achieved with AVL Trees.

## Assignment Specifications

#### class Node:

This class implements a tree node, utilized by the `BinarySearchTree` and `AVLTree` classes.

_DO NOT MODIFY the following attributes/functions_

- **Attributes**:
  - **`value: T`**: The value held by the `Node`. It can be of any type, such as `str`, `int`, `float`, `dict`, or even a more complex object.
  - **`parent: Node`**: A reference to this `Node`'s parent `Node`. It may be `None` if the node has no parent.
  - **`left: Node`**: A reference to this `Node`'s left child `Node`. It may be `None` if the node has no left child.
  - **`right: Node`**: A reference to this `Node`'s right child `Node`. It may be `None` if the node has no right child.
  - **`height: int`**: The number of levels of `Node`s below this one. The height of a leaf `Node` is considered to be 0.

- **Methods**:
  - **`__init__(self, value: T, parent: Node = None, left: Node = None, right: Node = None) -> None`**:
    - This constructor initializes an AVL Tree node with the provided values.
    - Parameters:
      - **`value: T`**: The value to be held by the `Node`.
      - **`parent: Node`**: A reference to this `Node`'s parent `Node`. Defaults to `None`.
      - **`left: Node`**: A reference to this `Node`'s left child `Node`. Defaults to `None`.
      - **`right: Node`**: A reference to this `Node`'s right child `Node`. Defaults to `None`.
    - Returns: `None`.

  - **`__str__(self) -> str`** and **`__repr__(self) -> str`**:
    - These methods represent the `Node` as a string in the format `<value_held_by_node>`. For example, `<7>` would represent a `Node` object holding an integer value of 7, while `<None>` would represent a `Node` object holding a value of `None`.
    - These methods are automatically called when printing a `Node` to the console, and also when a `Node` is displayed in a debugger.
    - To invoke these methods, use `str(node)` instead of calling `node.__str__()` directly.
    - Returns: `str`.

#### class BinarySearchTree:

This class implements a traditional Binary Search Tree (BST).

_DO NOT MODIFY the following attributes/functions_

- **Attributes**:
  - **`origin: Node`**: The root node of the entire `BSTree`. It might be `None` if the tree is empty. The term `origin` helps distinguish between the root of the entire tree and the root of a subtree within the tree. Essentially, any `Node` in a `BSTree` can be considered as the root of a subtree comprising all the nodes below it, and `origin` refers to the highest root in the tree.
  - **`size: int`**: The total number of nodes present in the `BSTree`.

- **Methods**:
  - **`__init__(self) -> None`**:
    - Constructs an empty `BSTree`, initializing `origin` to `None` and `size` to 0.
    - Returns: `None`.
    
  - **`__str__(self) -> str`** and **`__repr__(self) -> str`**:
    - Returns a neatly formatted string representation of the binary search tree. Each node in this representation follows the format `{value},h={height},⬆{parent.value}`.
    - These methods are automatically called when the tree is printed to the console or when a node is displayed in a debugger.
    - Use `str(tree)` instead of `tree.__str__()` to invoke these methods.
    - Returns: `str`.

  - **`visualize(self, filename="bst_visualization.svg") -> str`**:
    - Generates an SVG image file representing the binary search tree.
    - `filename: str`: The name of the file to save the SVG image as. It should have a `.svg` extension. Defaults to "bst_visualization.svg".
    - Returns: The SVG string as `str`.

_IMPLEMENT the following functions_

- **`height(self, root: Node) -> int`**:
  - Calculates and returns the height of a subtree in the `BSTree`, handling the case where `root` is `None`. Note that an empty subtree has a height of -1.
  - This method is simple to implement, particularly if you recall that a `Node`'s height (if it exists) is stored in its `height` attribute.
  - This function is not directly tested as it is very straightforward, but it will be utilized by other functions.
  - Time / Space Complexity: O(1) / O(1).
  - `root: Node`: The root of the subtree whose height is to be calculated.
  - Returns: The height of the subtree at `root`, or -1 if `root` is `None`.

- **`insert(self, root: Node, val: T) -> None`**:
  - Inserts a node with the value `val` into the subtree rooted at `root`, returning the root of the balanced subtree after the insertion.
  - If `val` already exists in the tree, the function does nothing.
  - Make sure to update the `size` and `origin` attributes of the `BSTree` object, and properly set the parent/child pointers when inserting a new `Node`.
  - This method is simpler to implement when done recursively.
  - Time / Space Complexity: O(h) / O(1), where *h* is the height of the tree.
  - `root: Node`: The root of the subtree where `val` is to be inserted.
  - `val: T`: The value to insert.
  - Returns: None.

- **`remove(self, root: Node, val: T) -> Node`**:
  - Removes the node with the value `val` from the subtree rooted at `root`, and returns the root of the subtree after the removal.
  - If `val` does not exist in the `BSTree`, the function does nothing.
  - Update `size` and `origin` attributes of the `BSTree` object, and correctly update the parent/child pointers and `height` attributes of affected `Node` objects.
  - Take into account the [three distinct cases of BST removal](https://en.wikipedia.org/wiki/Binary_search_tree#Deletion) when implementing this method.
  - If you are removing a node with two children, swap the value of this node with its predecessor, and then recursively remove the predecessor node (which will have the value to be removed after the swap and is guaranteed to be a leaf).
    - While it is technically possible to swap with the successor node in cases of two-child removal, our tests will assume you will swap with the predecessor.
  - Time / Space Complexity: O(h) / O(1), where *h* is the height of the tree.
  - `root: Node`: The root of the subtree from which to delete `val`.
  - `val: T`: The value to be deleted.
  - Returns: The root of the new subtree after the removal (could be the original root).

- **`search(self, root: Node, val: T) -> Node`**:
  - Searches for and returns the `Node` containing the value `val` in the subtree rooted at `root`.
  - If `val` is not present in the subtree, the function returns the `Node` below which `val` would be inserted as a child. For example, in a BST 1-2-3 tree (with 2 as the root and 1, 3 as children), `search(node_2, 0)` would return `node_1` because the value 0 would be inserted as a left child of `node_1`.
  - This method is simplest to implement recursively.
  - Time / Space Complexity: O(h) / O(1), where *h* is the height of the tree.
  - `root: Node`: The root of the subtree in which to search for `val`.
  - `val: T`: The value to search for.
  - Returns: The `Node` containing `val`, or the `Node` below which `val` would be inserted as a child if it does not exist.

#### class AVLTree

This class implements a self-balancing Binary Search Tree (BST) to ensure faster operation times.

##### Attributes (Do not modify)
- **origin (Node):** The root node of the AVLTree, which could potentially be `None`. This helps distinguish between the root of the entire AVLTree and the root of any subtree within it. Essentially, any Node within the AVLTree can be seen as the root of its own subtree, with `origin` being the root of them all.
- **size (int):** The total number of nodes present in the AVLTree.

##### Methods (Do not modify)
- **\_\_init\_\_(self) -> None:**
  - Creates an empty AVLTree, setting `origin` to `None` and `size` to zero.
  - **Returns:** None

- **\_\_str\_\_(self) -> str** and **\_\_repr\_\_(self) -> str:**
  - Provides a visually pleasing string representation of the binary tree, formatting each node as `{value},h={height},⬆{parent.value}`.
  - Python will automatically use this method when a Node is printed to the console, and PyCharm will use it when displaying a Node in the debugger.
  - To invoke this method, use `str(node)` instead of `node.__str__()`.
  - **Returns:** A string representation of the AVLTree.

- **visualize(self, filename="avl_tree_visualization.svg") -> str:**
  - Generates an SVG image file representing the binary tree.
  - **Parameters:** 
    - **filename (str):** The name for the output SVG file. Defaults to "avl_tree_visualization.svg".
  - **Returns:** The SVG string.

##### Methods to Implement
- **height(self, root: Node) -> int:**
  - Calculates the height of a subtree in the AVL tree, handling cases where `root` might be `None`. Remember, the height of an empty subtree is defined as -1.
  - **Parameters:** 
    - **root (Node):** The root node of the subtree whose height you wish to determine.
  - **Returns:** The height of the subtree rooted at `root`.
  - **Time / Space Complexity:** O(1) / O(1)

- **left_rotate(self, root: Node) -> Node**
  - This method performs a left rotation on the subtree rooted at `root`, returning the new root of the subtree after the rotation.
  - **Parameters:**
    - **root (Node):** The root node of the subtree that is to be rotated.
  - **Returns:** The root of the new subtree post-rotation.
  - **Time / Space Complexity:** O(1) / O(1)

- **right_rotate(self, root: Node) -> Node**
  - This method performs a right rotation on the subtree rooted at `root`, returning the new root of the subtree after the rotation.
  - It should be almost identical in implementation to `left_rotate`, differing only in a few lines of code.
  - **Parameters:**
    - **root (Node):** The root node of the subtree that is to be rotated.
  - **Returns:** The root of the new subtree post-rotation.
  - **Time / Space Complexity:** O(1) / O(1)

- **balance_factor(self, root: Node) -> int**
  - This method computes the balance factor of the subtree rooted at `root`.
  - The balance factor is calculated as `h_L - h_R`, where `h_L` is the height of the left subtree, and `h_R` is the height of the right subtree.
  - In a properly balanced AVL tree, all nodes should have a balance factor in the set {-1, 0, +1}. A balance factor of -2 or +2 triggers a rebalance.
  - For an empty subtree (where `root` is `None`), the balance factor is 0.
  - To maintain time complexity, update the `height` attribute of each node during insertions/deletions/rebalances, allowing you to use `h_L = left.height` and `h_R = right.height` directly.
  - **Parameters:**
    - **root (Node):** The root node of the subtree on which to compute the balance factor.
  - **Returns:** An integer representing the balance factor of `root`.
  - **Time / Space Complexity:** O(1) / O(1)

- **rebalance(self, root: Node) -> Node**
  - This function rebalances the subtree rooted at `root` if it is unbalanced, and returns the root of the resulting subtree post-rebalancing.
  - A subtree is considered unbalanced if the balance factor `b` of the `root` satisfies `b >= 2 or b <= -2`.
  - There are four types of imbalances possible in an AVL tree, each requiring a specific sequence of rotations to restore balance. You can find more details on these [here](https://en.wikipedia.org/wiki/AVL_tree#Rebalancing).
  - **Parameters:**
    - **root (Node):** The root of the subtree that potentially needs rebalancing.
  - **Returns:** The root of the new, potentially rebalanced subtree.
  - **Time / Space Complexity:** O(1) / O(1)

- **insert(self, root: Node, val: T) -> Node**
  - This function inserts a new node with value `val` into the subtree rooted at `root`, balancing the subtree as necessary, and returns the root of the resulting subtree.
  - If a node with value `val` already exists in the tree, the function does nothing.
  - This function updates the `size` and `origin` attributes of the `AVLTree`, sets the parent/child pointers correctly when inserting the new `Node`, updates the `height` attribute of affected nodes, and calls `rebalance` on all affected ancestor nodes.
  - The function is most easily implemented recursively.
  - **Parameters:**
    - **root (Node):** The root of the subtree where `val` is to be inserted.
    - **val (T):** The value to be inserted.
  - **Returns:** The root of the new, balanced subtree.
  - **Time / Space Complexity:** O(log n) / O(1)

- **remove(self, root: Node, val: T) -> Node**
  - This function removes the node with value `val` from the subtree rooted at `root`, balances the subtree as necessary, and returns the root of the resulting subtree.
  - If a node with value `val` does not exist in the tree, the function does nothing.
  - The function updates the `size` and `origin` attributes of the `AVLTree`, sets the parent/child pointers correctly, updates the `height` attribute of affected nodes, and calls `rebalance` on all affected ancestor nodes.
  - The removal process depends on whether the node to be removed has zero, one, or two children, with different strategies for each case. In the case of a node with two children, the function swaps its value with that of its predecessor (the maximum value node of its left subtree), and then recursively removes the predecessor node.
  - The function is implemented recursively.
  - **Parameters:**
    - **root (Node):** The root of the subtree from which `val` is to be removed.
    - **val (T):** The value to be removed.
  - **Returns:** The root of the new, balanced subtree.
  - **Time / Space Complexity:** O(log n) / O(1)

- **min(self, root: Node) -> Node**
  - This function searches for and returns the `Node` containing the smallest value within the subtree rooted at `root`.
  - The implementation of this function is most straightforward when done recursively.
  - **Parameters:**
    - **root (Node):** The root of the subtree within which to search for the minimum value.
  - **Returns:** A `Node` object that holds the smallest value in the subtree rooted at `root`.
  - **Time / Space Complexity:** O(log n) / O(1)

- **max(self, root: Node) -> Node**
  - This function searches for and returns the `Node` containing the largest value within the subtree rooted at `root`.
  - Like the min function, the implementation of this function is most straightforward when done recursively.
  - **Parameters:**
    - **root (Node):** The root of the subtree within which to search for the maximum value.
  - **Returns:** A `Node` object that holds the largest value in the subtree rooted at `root`.
  - **Time / Space Complexity:** O(log n) / O(1)

- **search(self, root: Node, val: T) -> Node**
  - This function searches for the `Node` with the value `val` within the subtree rooted at `root`.
  - If the value `val` does not exist within this subtree, the function will return the `Node` under which `val` would be inserted if it were added to the tree. For instance, in a balanced binary search tree of 1-2-3 (where 2 is the root, and 1 and 3 are left and right children respectively), calling `search(node_2, 0)` would return `node_1`, because if we were to insert 0 into this tree, it would be added as the left child of 1.
  - The implementation of this function is most straightforward when done recursively.
  - **Parameters:**
    - **root (Node):** The root of the subtree within which to search for `val`.
    - **val (T):** The value to be searched for within the subtree rooted at `root`.
  - **Returns:** A `Node` object containing `val` if it exists within the subtree, and if not, the `Node` under which `val` would be inserted as a child.
  - **Time / Space Complexity:** O(log n) / O(1)

- **inorder(self, root: Node) -> Generator[Node, None, None]**
  - This function performs an inorder traversal (left, current, right) of the subtree rooted at `root`, generating the nodes one at a time using a [Python generator](https://realpython.com/introduction-to-python-generators/).
  - Use `yield` to produce individual nodes as they are encountered, and `yield from` for recursive calls to `inorder`.
  - Ensure that `None`-type nodes are not yielded.
  - **Important**: To pass the test case for this function, you must also make the AVLTree class iterable, enabling the usage of `for node in avltree` to iterate over the tree in an inorder manner.
  - **Time / Space Complexity:** O(n) / O(1). Although the entire tree is traversed, the generator yields nodes one at a time, resulting in constant space complexity.
  - **Parameters:**
    - **root (Node):** The root node of the current subtree being traversed.
  - **Returns:** A generator yielding the nodes of the subtree in inorder.

- **\_\_iter\_\_(self) -> Generator[Node, None, None]**
  - This method makes the AVL tree class iterable, allowing you to use it in loops like `for node in tree`.
  - For the iteration to work, this function should be implemented such that it returns the generator from the inorder traversal of the tree.
  - **Returns:** A generator yielding the nodes of the tree in inorder.
  - **Implementation Note:** This function should be one line, calling the `inorder` function.

- **preorder(self, root: Node) -> Generator[Node, None, None]**
  - This function performs a preorder traversal (current, left, right) of the subtree rooted at `root`, generating the nodes one at a time using a [Python generator](https://realpython.com/introduction-to-python-generators/).
  - Use `yield` to produce individual nodes as they are encountered, and `yield from` for recursive calls to `preorder`.
  - Ensure that `None`-type nodes are not yielded.
  - **Time / Space Complexity:** O(n) / O(1). Although the entire tree is traversed, the generator yields nodes one at a time, resulting in constant space complexity.
  - **Parameters:**
    - **root (Node):** The root node of the current subtree being traversed.
  - **Returns:** A generator yielding the nodes of the subtree in preorder.

- **postorder(self, root: Node) -> Generator[Node, None, None]**
  - This function performs a postorder traversal (left, right, current) of the subtree rooted at `root`, generating the nodes one at a time using a [Python generator](https://realpython.com/introduction-to-python-generators/).
  - Utilize `yield` to produce individual nodes as they are encountered, and `yield from` for recursive calls to `postorder`.
  - Ensure that `None`-type nodes are not yielded.
  - **Time / Space Complexity:** O(n) / O(1). The entire tree is traversed, but the use of a generator yields nodes one at a time, maintaining constant space complexity.
  - **Parameters:**
    - **root (Node):** The root node of the current subtree being traversed.
  - **Returns:** A generator yielding the nodes of the subtree in postorder. A `StopIteration` exception is raised once all nodes have been yielded.

- **levelorder(self, root: Node) -> Generator[Node, None, None]**
  - This function performs a level-order (breadth-first) traversal of the subtree rooted at `root`, generating the nodes one at a time using a [Python generator](https://realpython.com/introduction-to-python-generators/).
  - Use the `queue.SimpleQueue` class for maintaining the queue of nodes during the traversal. [Refer to the official documentation for more information.](https://docs.python.org/3/library/queue.html#queue.SimpleQueue)
  - Utilize `yield` to produce individual nodes as they are encountered.
  - Ensure that `None`-type nodes are not yielded.
  - **Time / Space Complexity:** O(n) / O(n). The entire tree is traversed, and due to the nature of level-order traversal, the queue can grow to O(n), particularly in a [perfect binary tree](https://www.programiz.com/dsa/perfect-binary-tree) scenario.
  - **Parameters:**
    - **root (Node):** The root node of the current subtree being traversed.
  - **Returns:** A generator yielding the nodes of the subtree in level-order. A `StopIteration` exception is raised once all nodes have been yielded.

# Application: Implementation of AVL Trees in _k_-Nearest Neighbors

Welcome to [SpartaHack 9](https://spartahack.com), hosted by Michigan State University, where innovation meets creativity! We are thrilled to have hundreds of students from various schools nationwide join us for this prestigious hackathon event. The event has garnered immense popularity, evident from the overwhelming number of applications we have received. Each application provides valuable insights into the applicant, such as their previous hackathon experiences, completed projects, proficiency in programming languages, and preferred teammates.

[![](img/sh9.png)](https://spartahack.com)

Yet, this influx of applications poses a significant challenge. Reviewing each application manually to decide on acceptance or rejection is a daunting task. It is not only time-consuming but also prone to unconscious biases. As time is of the essence, we recognize the urgent need for an automated approach to streamline the application process.

Reflecting on the success of the previous edition, SpartaHack 8, we are inspired to adopt a data-driven strategy. Last year, each application underwent a thorough review, resulting in a clear outcome: acceptance or rejection. This presents a unique opportunity to leverage past data to enhance the current application review process. We propose using the _k_-Nearest Neighbors algorithm to analyze this year's applications in light of the previous year's data. This approach will enable us to predict the outcome of each application based on its similarity to past applicants, ensuring a fair and efficient selection process.

Excited by this innovative solution, we are eager to implement the [_k_-Nearest Neighbor](https://en.wikipedia.org/wiki/K-nearest_neighbors_algorithm) algorithm and transform the [SpartaHack 9](https://spartahack.com) application process. We anticipate creating a selection system that is not only quick and fair but also free from human biases. The journey to automating the approval/rejection process promises have a tremendous positive impact!

### Background Information

In the realm of data science, [classification](https://en.wikipedia.org/wiki/Statistical_classification) is a crucial task that involves sorting data into distinct categories. Take, for instance, email filtering: determining whether an email is "spam" or "not spam" is a classic example of a classification problem. In the past, such problems were often tackled using _rule-based_ classifiers, which required conditional statements to set the rules for classification. However, these rule-based systems were cumbersome to implement, difficult to maintain, and challenging to fine-tune for accuracy.

This is where [machine learning](https://en.wikipedia.org/wiki/Machine_learning)-based classifiers come into play, offering a more sophisticated and adaptable solution. Unlike their rule-based counterparts, machine learning classifiers learn to categorize new data by identifying patterns in previously-observed, labeled data.

The [_k_-Nearest Neighbor](https://en.wikipedia.org/wiki/K-nearest_neighbors_algorithm) classifier stands out as a prime example of a machine learning-based classifier. It works by comparing a new data point to its _k_ closest neighbors that have known class labels. In the case of SpartaHack 9, you will be implementing two key functions within a custom `NearestNeighborClassifier` class to bring this algorithm to life.

![k-Nearest Neighbors Algorithm Visualization](img/knn.png)

### Problem Description

In this task, you will work with the `NearestNeighborClassifier`, a one-dimensional _k_-Nearest Neighbors algorithm, to make predictions based on given datasets. The process involves two main functions:

1. `fit()`: This function trains the classifier using a _training_ dataset of `(x, y)` pairs, where `x` is a feature (a float) and `y` is the target label (a string).
2. `predict()`: This function predicts the class labels for a _testing_ dataset of `x` values based on the patterns learned during the training phase.

#### Dataset Description:
- **Training Data**: `List[tuple(float, str)]` - A list of `(x: float, y: str)` tuples.
- **Testing Data**: `x` values (floats).

### Example: Predicting Seasons from Temperature

Consider a practical scenario where we have collected a dataset comprising pairs of daily high temperatures and the corresponding seasons. The dataset is represented as `(temperature, season)` pairs, where:
- `temperature` (denoted as `x`) is a float value ranging from 0 to 1, indicating normalized temperature readings.
- `season` (denoted as `y`) is a string value representing one of the four seasons: "spring", "summer", "fall", or "winter".

In this example, the goal of our `NearestNeighborClassifier` is to learn from this data in order to make season predictions based on temperature input.

#### Learning from Data: The `fit()` Function
- The `fit()` function will take this dataset and establish associations between temperature values and seasons.
  - Lower temperature values (closer to 0) will be associated with "winter".
  - Higher temperature values (closer to 1) will be associated with "summer".
  - Mid-range temperature values will be associated with "spring" and "fall".

By processing this dataset, the classifier learns the patterns and tendencies of temperature readings corresponding to each season.

#### Making Predictions: The `predict()` Function
- Once the classifier has been trained with `fit()`, you can use the `predict()` function to estimate the season for a new temperature reading.
  - You provide a temperature value `x` as input.
  - The function outputs the most likely season `y` based on the learned associations.

#### Practical Example:
If our classifier has learned properly, providing a low temperature reading (e.g., `0.1`) to `predict()` should output "winter", while a high temperature reading (e.g., `0.9`) should output "summer". Mid-range values should result in "spring" or "fall", depending on the exact distributions and associations learned during the training phase.

In summary, this example illustrates how the `NearestNeighborClassifier` can be applied to establish meaningful associations between data points and make informed predictions based on those associations.


#### class NearestNeighborClassifier

**Important: Please do not modify the following attributes and functions.**

- **Attributes**
  - **tree (AVLTree):** A data structure used to store the labeled training data. This attribute gets populated in the `fit()` method and is utilized in the `predict()` method for making predictions.
  - **resolution (int):** This determines the precision of the temperature values in our dataset. Specifically, it indicates the number of decimal places we consider for rounding the temperature values.

- **Methods**
  - **\_\_init\_\_(self, resolution: int) -> None:**
    - Purpose: Initialize the NearestNeighborClassifier object.
    - Details: The initialization involves creating `10**resolution + 1` nodes in the `self.tree`. Each node stores an `AVLWrappedDictionary` object.
      - Example: If `resolution` is set to 1, we will create 11 nodes corresponding to the keys `0, 0.1, 0.2, ..., 1.0`. If `resolution` is 2, we will have 101 nodes with keys ranging from `0` to `1.0`, incremented by `0.01`.
    - Parameters: 
      - **resolution (int):** The precision level for rounding temperature values.
    - Returns: 
      - None

  - **\_\_str\_\_(self) -> str** and **\_\_repr\_\_(self) -> str:**
    - Purpose: Provide a string representation of the NearestNeighborClassifier object.
    - Returns:
      - A string (`str`).

  - **visualize(self, filename="nnc_visualization.svg") -> None:**
    - Purpose: Generate a visualization of the NearestNeighborClassifier tree structure and save it as an SVG file.
    - Parameters:
      - **filename (str):** The name of the file to save the visualization. It defaults to "nnc_visualization.svg".
    - Returns:
      - None

**Functions to Implement:**

> Implement `fit` and `predict` methods in `NearestNeighborClassifier`

To provide clarity, let's discuss the `fit` and `predict` methods using a more generic example, while still referencing the `(temperature, season)` example for illustrative purposes. It’s important to note that the `NearestNeighborClassifier` can be applied to various types of data, not just temperatures and seasons.

- `fit(self, data: List[Tuple[float, str]]) -> None`

  The `fit` method is used to train the classifier with a dataset, helping it learn the associations between features `x` (float values) and target labels `y` (string values).

  - **Process:**
    - Iterate through each `(x, y)` pair in the dataset.
    - Round the `x` value to the specified precision (based on `self.resolution`).
    - Find the corresponding node in the tree using the rounded `x` value as a key.
    - Access the `AVLWrappedDictionary` object at this node.
    - Update the count of the label `y` in this dictionary.

  - **Example with Seasons:**
    - Consider a dataset of `(temperature, season)` pairs. In this case, `x` is a temperature, and `y` is a season.
    - If a particular temperature is associated with winter multiple times in the dataset, the count of "winter" in the corresponding dictionary will increase.
    - This process helps the classifier learn from the training data.

  - **Complexity:**
    - Time: O(n log n)
    - Space: O(n)

  - **Parameters:**
    - **data (List[Tuple[float, str]]):** A list of `(x, y)` pairs.

  - **Returns:**
    - None

- `predict(self, x: float, delta: float) -> str`

  The `predict` method predicts the target label `y` for a given feature value `x`.

  - **Process:**
    - Round the `x` value to the specified precision (based on `self.resolution`).
    - Search for nodes in the tree whose keys are within `± delta` of the rounded `x` value.
    - Access the `AVLWrappedDictionary` objects at these nodes.
    - Determine the most common label `y` across all these dictionaries.

  - **Example with Seasons:**
    - If we input a temperature value, the classifier will look for temperatures in the training data that are close to the input and use the seasons associated with those temperatures to predict the season for the input temperature.

  - **Notes:**
    - The method effectively predicts `y` based on the most common `y` values observed in the training data for `x` values close to the input.
    - If there are no data points close to the input, the function returns `None`.

  - **Complexity:**
    - Time: O(k log n)
    - Space: O(1)

  - **Parameters:**
    - **x (float):** Feature value to be predicted.
    - **delta (float):** Range to search for neighboring feature values.

  - **Returns:**
    - A string (`str`) representing the predicted target label `y`.

In conclusion, these methods enable the `NearestNeighborClassifier` to learn from provided data and make predictions based on that learning. While the `(temperature, season)` example serves as a good illustration, it’s crucial to understand that these methods are applicable to a wide variety of data types and problem domains.


# AVLWrappedDictionary Class

## Overview
The `AVLWrappedDictionary` class is a utility class designed to wrap a dictionary and a floating point key together so that it can be stored in an AVL Tree, maintaining a balanced binary search tree structure. This setup is particularly useful when you want to store data in a sorted manner and perform range queries efficiently.

## Attributes
-  `key: float`: This is a floating point value used as a key to sort and look up the `AVLWrappedDictionary` object in the AVL Tree.

- `dictionary: dict`: This is a standard Python dictionary object that is stored within the `AVLWrappedDictionary`.

## Methods
- `__init__(self, key: float) -> None`
  - **Description:** Initializes a new instance of `AVLWrappedDictionary`, taking a floating point `key` as a parameter.
  - **Parameters:**
    - `key: float` - The key used to order this object within the AVL Tree.
  - **Returns:** None

- `__str__(self) -> str` and `__repr__(self) -> str`
  - **Description:** Represents the `AVLWrappedDictionary` as a string, facilitating easier debugging and visualization.
  - **Returns:** A string representation of the `AVLWrappedDictionary`.

- `__eq__(self, other: AVLWrappedDictionary) -> bool`
- `__gt__(self, other: AVLWrappedDictionary) -> bool`
- `__lt__(self, other: AVLWrappedDictionary) -> bool`
  - **Description:** Compares this `AVLWrappedDictionary` to another, based on their keys.
  - **Parameters:**
    - `other: AVLWrappedDictionary` - The other `AVLWrappedDictionary` to compare to.
  - **Returns:** A boolean indicating the result of the comparison.


#### Example

Imagine we have a set of applicant data for [SpartaHack 9](https://spartahack.com), and we want to classify the applicants into two categories: accepted and rejected. Each candidate's expertise, denoted as `x`, is measured on a scale from `[0, 1]`. This measurement is used to predict their class label `y`, which can be either `"accepted"` or `"rejected"`.

Here's the labeled dataset we have:

```
data = [(0.18, "rejected"), (0.21, "rejected"), (0.29, "rejected"),
        (0.49, "rejected"), (0.51, "accepted"), (0.53, "accepted"),
        (0.97, "accepted"), (0.98, "accepted"), (0.99, "accepted")]
```


We will use a `NearestNeighborClassifier` with a `resolution` of 1. After fitting our model with the `fit(data)` method, the classifier's tree would look like this:

![Classifier's Tree](img/nnc.png)

Next, consider a new set of applicants with the following expertise measurements:

```python
test_applicants = [0.1, 0.2, 0.5, 0.8, 0.9]
```

Our task is to predict the class label `y` for each value of `x` in `test_applicants`, with a `delta` value of 0.1. Here's what happens for each prediction:

- `predict(x=0.1, delta=0.1)`: The classifier looks at nodes with keys `{0, 0.1, 0.2}`. It finds 2 `"rejected"` and 0 `"accepted"` instances. Prediction: `"rejected"`.
- `predict(x=0.2, delta=0.1)`: The classifier looks at nodes with keys `{0.1, 0.2, 0.3}`. It finds 3 `"rejected"` and 0 `"accepted"` instances. Prediction: `"rejected"`.
- `predict(x=0.5, delta=0.1)`: The classifier looks at nodes with keys `{0.4, 0.5, 0.6}`. It finds 1 `"rejected"` and 2 `"accepted"` instances. Prediction: `"accepted"`.
- `predict(x=0.8, delta=0.1)`: The classifier looks at nodes with keys `{0.7, 0.8, 0.9}`. It finds 0 `"rejected"` and 0 `"accepted"` instances. Prediction: `None` (since there are no instances to base the prediction on).
- `predict(x=0.9, delta=0.1)`: The classifier looks at nodes with keys `{0.8, 0.9, 1}`. It finds 0 `"rejected"` and 3 `"accepted"` instances. Prediction: `"accepted"`.

In summary, running the following code:

```python
nnc = NearestNeighborClassifier(resolution=1)
nnc.fit(data)
predictions = nnc.predict(test_applicants)
```

Would yield:

```python
predictions = ["rejected", "rejected", "accepted", None, "accepted"]
```

Additional test cases and a precise input/output syntax can be found in the provided test cases.

Note: The test cases include a `plot` flag variable, which allows for optional visualization of the training and testing data using `numpy` and `matplotlib`.



# **Submission Guidelines**

### **Deliverables:**

For each project, a `solution.py` file will be provided. Ensure to write your Python code within this file. For best results:
- 📥 **Download** both `solution.py` and `tests.py` to your local machine.
- 🛠️ Use **PyCharm** for a smoother coding and debugging experience.

### **How to Work on a Project Locally:**

Choose one of the two methods below:

---

#### **APPROACH 1: Using D2L for Starter Package**
1. 🖥️ Ensure PyCharm is installed.
2. 📦 **Download** the starter package from the *Projects* tab on D2L. *(See the tutorial video on D2L if needed)*.
3. 📝 Write your code and, once ready, 📤 **upload** your `solution.py` to Codio. *(Refer to the D2L tutorial video for help)*.

---

#### **APPROACH 2: Directly from Codio**
1. 📁 On your PC, create a local folder like `Project01`.
2. 📥 **Download** `solution.py` from Codio.
3. 📥 **Download** `tests.py` from Codio for testing purposes.
4. 🛠️ Use PyCharm for coding.
5. 📤 **Upload** the `solution.py` back to Codio after ensuring the existing file is renamed or deleted.
6. 🔚 Scroll to the end in Codio's Guide editor and click the **Submit** button.

---

### **Important:**
- Always **upload** your solution and **click** the 'Submit' button as directed.
- All project submissions are due on Codio. **Any submission after its deadline is subject to late penalties** .
  
**Tip:** While Codio can be used, we recommend working locally for a superior debugging experience in PyCharm. Aim to finalize your project locally before submitting on Codio.

#### Grading

- Tests (70)
  - `BinarySearchTree`: \_\_/6
    - `insert`: \_\_/2
    - `remove`: \_\_/2
    - `search`: \_\_/2
  - `AVLTree`: \_\_/44
    - `rotate`: \_\_/5
    - `balance_factor`: \_\_/1
    - `rebalance`: \_\_/8
    - `insert`: \_\_/8
    - `remove`: \_\_/8
    - `min`: \_\_/1
    - `max`: \_\_/1
    - `search`: \_\_/8
    - `inorder`/`__iter__`: \_\_/1
    - `preorder`: \_\_/1
    - `postorder`: \_\_/1
    - `levelorder`: \_\_/1
    - `avl_comprehensive` (no points, but useful as a sanity check)
  - `NearestNeighborClassifier`: \_\_/20
    - `nnc`: \_\_/20
    - `nnc_comprehensive`: (no points, but useful as a sanity check)

**Note on Comprehensive Testing:**

We have included a comprehensive test for each function, which is worth 0 points. We **strongly recommend** you to utilize these tests as they are designed to thoroughly check your functions for any logical flaws. While these tests do not directly contribute to your score, if your solution fails to pass a comprehensive test for a specific function during our assessment, **half of the manual points allocated for that function will be deducted**. This is to emphasize the importance of not only meeting basic requirements but also ensuring robustness and correctness in your code. Consider these comprehensive tests as tools for ensuring quality and resilience in your solutions.

**Additional Note on Scenario Generation:**

While we make every effort to generate test cases that encompass every possible scenario, there might be times when some edge cases are inadvertently overlooked. Nevertheless, should we identify any scenario where your submitted logic doesn't hold, even if it's not part of our provided test cases, we reserve the right to deduct from the manual points. This highlights the significance of crafting logic that doesn't merely pass the given tests, but is genuinely resilient and correctly addresses the problem's entirety. Always strive to think beyond the provided cases, ensuring that your solutions are comprehensive and robust.

- Manual (30)
  - Time and space complexity points are **all-or-nothing** for each function. If you fail to meet time **or** space complexity in a given function, you do not receive manual points for that function.
  - Loss of 1 point per missing docstring (max 3 point loss)
  - Loss of 2 points per changed function signature (max 20 point loss)
  - Loss of 20 points (flat-rate) for use of global variables (with the nonlocal keyword)
    - `BinarySearchTree` time & space: \_\_/6
      - `insert`: \_\_/2
      - `search`: \_\_/2
      - `remove`: \_\_/2
    - `AVLTree` time & space: \_\_/18
      - `left_rotate`: \_\_/2
      - `right_rotate`: \_\_/2
      - `balance_factor`: \_\_/1
      - `rebalance`: \_\_/2
      - `insert`: \_\_/2
      - `remove`: \_\_/2
      - `min`: \_\_/1
      - `max`: \_\_/1
      - `search`: \_\_/1
      - `inorder`/`__iter__`: \_\_/1
      - `preorder`: \_\_/1
      - `postorder`: \_\_/1
      - `levelorder`: \_\_/1
    - `NearestNeighborClassifier`: \_\_/6
      - `fit`: \_\_/3
      - `predict`: \_\_/3

_Project by Gabriel Sotelo. Adapted from the work of Bank Premsri, Joseph Pallipadan, Andrew McDonald, Jacob Caurdy and Lukas Richters._

#### Memes

![](img/tree.jpg)

![](img/thanos.jpg)

![](img/bestworst.png)
