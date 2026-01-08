def is_balanced(self, root: Optional[TreeNode]) -> bool:
    def dfs(node):
        if not node:
            return (True, 0)

        # ask left child for the report
        left_balanced, left_height = dfs(node.left)
        # ask right child for the report
        right_balanced, right_height = dfs(node.right)
        # process the results
        # if either child is unbalanced, I am unbalanced too
        if not left_balanced or not right_balanced:
            return (False, 0)  # height does not matter
        # if children are ok, check my own balance
        if abs(left_height - right_height) > 1:
            return (False, 0)
        # if everything is ok, return True and my height
        return (True, 1 + max(left_height, right_height))

    balanced, height = dfs(root)
    return balanced
