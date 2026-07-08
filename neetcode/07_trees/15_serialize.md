### question
Implement an algorithm to serialize and deserialize a binary tree.

Serialization is the process of converting an in-memory structure into a sequence of bits so that it can be stored or sent across a network to be reconstructed later in another computer environment.

You just need to ensure that a binary tree can be serialized to a string and this string can be deserialized to the original tree structure. There is no additional restriction on how your serialization/deserialization algorithm should work.

**1. Restate**
Convert in-memory binary tree to string (serialize). Convert string back to exact same binary tree (deserialize). No constraints on string format format.

**2. Clarify & I/O**

* **Input (Serialize):** `TreeNode` root.
* **Output (Serialize):** `String`.
* **Input (Deserialize):** `String`.
* **Output (Deserialize):** `TreeNode` root.
* **Questions:** Node values negative? Yes. Max depth? Up to 10^4. Can we use delimiters? Yes.

**3. Hand-Trace**
Input tree:
1
/ 

2   3
/ 

4   5

* Visit preorder (Node, Left, Right). Use 'X' for null.
* At 1: string="1,"
* Go left to 2: string="1,2,"
* 2's left is null: string="1,2,X,"
* 2's right is null: string="1,2,X,X,"
* Go right from 1 to 3: string="1,2,X,X,3,"
* 3's left is 4, 4's children null: string="1,2,X,X,3,4,X,X,"
* 3's right is 5, 5's children null: string="1,2,X,X,3,4,X,X,5,X,X"
Output string: `"1,2,X,X,3,4,X,X,5,X,X"`
To deserialize, read sequentially. '1' is root. '2' is left child. Next two 'X' mean 2 has no children. Backtrack to 1, next is '3' (right child), etc.

**4. Brainstorm & Complexity**

* *Idea 1: DFS Preorder (Hand-trace logic).* Recursively build string. Recursively consume string.
* Time: O(N) visit every node.
* Space: O(N) recursion stack and string size.


* *Idea 2: BFS Level-order.* Queue-based.
* Time: O(N).
* Space: O(N) for queue and string. Lots of trailing nulls to handle or strip.


* *Idea 3: DFS Inorder/Postorder.* Harder to reconstruct top-down without extra info (usually need Inorder + Preorder together).

**5. Suggest Solutions**
Prefer Idea 1 (DFS Preorder). Matches hand-trace exactly. Simple top-down recursion. Easy to explain, minimal state tracking compared to BFS queue management.

**6. Outline (Core Logic)**

```python
class Codec:
    def serialize(self, root): # -> str
        """
        Reframe: Flatten tree top-down, explicitly marking missing nodes.
        State: List of strings maintained, chosen because string concatenation is slow.
        Invariant: Traversal order strictly matches (Root, Left, Right).

        build_list(node) = appends node value or 'X' to list recursively.

        Core logic:
        - traverse tree preorder
        - if node exists, append value, recurse left, recurse right
        - join list with commas
        Edge cases:
        - empty tree (root is None)
        """
        pass

    def deserialize(self, data): # -> TreeNode
        """
        Reframe: Rebuild tree top-down by consuming serialized tokens sequentially.
        State: Queue (or iterator) of tokens, chosen because we consume values strictly left-to-right.
        Invariant: Next token in queue always belongs to current subtree insertion point.

        consume_token() = gets next value from queue, builds node, connects left/right subtrees.

        Core logic:
        - split string by commas into queue
        - pop token
        - create node with token value
        - attach node.left by recursively consuming tokens
        - attach node.right by recursively consuming tokens
        - return node
        Edge cases:
        - token is 'X' (return None)
        - empty input string
        """
        pass

```

**7. Iterative Implementation**

*Iteration 1: Skeleton with placeholders*

```python
class Codec:
    def serialize(self, root):
        result_list = []
        
        def build_list(node):
            # TODO: append val or 'X', recurse
            pass
            
        build_list(root)
        # TODO: return joined string
        return ""

    def deserialize(self, data):
        # TODO: split data into token_queue
        token_queue = []
        
        def consume_token():
            # TODO: pop token, return None if 'X', else build node and recurse
            pass
            
        return consume_token()

```

*Iteration 2: Core logic (Happy path)*

```python
class Codec:
    def serialize(self, root):
        result_list = []
        
        def build_list(node):
            # ADDED: base case and preorder traversal
            if not node:
                result_list.append("X")
                return
            result_list.append(str(node.val))
            build_list(node.left)
            build_list(node.right)
            
        build_list(root)
        # ADDED: join list
        return ",".join(result_list)

    def deserialize(self, data):
        # ADDED: split into list
        token_queue = data.split(",")
        
        def consume_token():
            # ADDED: pop front, check null, build subtrees
            val = token_queue.pop(0)
            if val == "X":
                return None
                
            node = TreeNode(int(val))
            node.left = consume_token()
            node.right = consume_token()
            return node
            
        return consume_token()

```

*Iteration 3: Walk Edge Cases*

* *Edge case:* Empty tree `serialize(None)`.
* `build_list(None)` appends "X". `result_list` is `["X"]`.
* Returns `"X"`. Works perfectly.


* *Edge case:* Empty tree `deserialize("X")`.
* `token_queue = ["X"]`.
* `consume_token` pops `"X"`, returns `None`. Works perfectly.


* *Edge case:* Empty string input to deserialize?
* `serialize` always outputs at least `"X"`, never empty string. Not a problem.



**8. Complexity & Optimization**

* *Current Complexity:*
* `serialize`: Time O(N), Space O(N) for string/recursion.
* `deserialize`: `pop(0)` on a Python list is O(N). Doing this N times makes deserialization **O(N^2)**. Space O(N).


* *Optimization:* Use `iter()` to consume the list in O(1) time per token, bringing `deserialize` time to **O(N)**.

*Final Optimized Code:*

```python
class Codec:
    def serialize(self, root):
        res = []
        def build_list(node):
            if not node:
                res.append("X")
                return
            res.append(str(node.val))
            build_list(node.left)
            build_list(node.right)
            
        build_list(root)
        return ",".join(res)

    def deserialize(self, data):
        # OPTIMIZATION: iter() gives O(1) sequential reads
        tokens = iter(data.split(","))
        
        def consume_token():
            val = next(tokens)
            if val == "X":
                return None
            node = TreeNode(int(val))
            node.left = consume_token()
            node.right = consume_token()
            return node
            
        return consume_token()

```