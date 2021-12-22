import equation_visualizer.parser.tokens as tokens

class TreeNode:

    def __init__(self, value: tokens.Token):
        self.value = value
        self.left = None
        self.right = None
        self.parent = None

class NodeVisitor:

    def __init__(self, root: TreeNode):
        self.root = root

    def visit(self, node: TreeNode):
        node.execute()
    