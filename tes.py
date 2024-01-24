class Tree:
    def __init__(self, val: int) -> None:
        self.left: 'Tree | None' = None
        self.right: 'Tree | None' = None
        self.val = val


def dfs(root: Tree | None) -> None:
    if root is None:
        return

    print(root.val)
    dfs(root.left)
    dfs(root.right)


def bfs(root: Tree | None) -> None:
    queue = [root]
    visited = []

    while queue:
        el = queue.pop(0)

        if el not in visited:
            visited.append(el)

            if el.left:
                queue.append(el.left)
            
            if el.right:
                queue.append(el.right)
    print(list(map(lambda x: x.val, visited)))


if __name__ == '__main__':
    root = Tree(1)

    root.left = Tree(2)
    root.right = Tree(3)

    root.left.left = Tree(4)

    root.right.left = Tree(5)
    root.right.right = Tree(6)

    bfs(root)
