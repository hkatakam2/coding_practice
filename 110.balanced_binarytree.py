from functools import cache


def is_balanced(self, root):
    @cache
    def height(node):
        if not node:
            return 0
        return 1 + max(height(node.left), height(node.right))

    if not root:
        return True

    if abs(height(root.left) - height(root.right)) > 1:
        return False
    else:
        return self.is_balanced(root.left) and self.is_balanced(root.right)
