def is_balanced(self, root):
    # 1. create a cache to store heights we've already calculated
    self.height_cache = {}

    if not root:
        return True

    def height(node):
        if not node:
            return 0

        # before calculating, check if already exists
        if node in self.height_cache:
            return self.height_cache[node]

        # calculate and store it
        h = 1 + max(height(node.left), height(node.right))
        self.height_cache[node] = h
        return h

    if abs(height(root.left) - height(root.right)) > 1:
        return False
    else:
        return self.is_balanced(root.left) and self.is_balanced(root.right)
