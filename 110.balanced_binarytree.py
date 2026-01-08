def is_balanced(root):
    if not root:
        return True

    def height(node):
        if not node:
            return 0
        return 1 + max(height(node.left), height(node.right))

    if abs(height(root.left) - height(root.right)) > 1:
        return False
    else:
        return is_balanced(root.left) and is_balanced(root.right)
