# design in memory file system

# clarification
1. operations needed:
   1. ls(path), mkdir(path), addContentToFile(path, content), readContentFromFile(path)
2. what does ls return? 
   1. directory -> sorted names of the children
   2. file -> a list with just the file's name
3. does mkdir create missing directories? Yes
4. does addContentToFile, create the missing file? create if missing, append if available
5. are paths always absolute? starting with / ? 
6. can file and directory share the same name in the same folder? No
7. Scale and Concurrency? Single threaded, fits in memory

# ideas
1. flat hashmap
2. tree of nodes (a trie keyed by path segment)
   1. each node is either a directory (holds a map of children) or a file(holds content)
   2. every operation walks the path one segment at a time, while is O(L) for L segments
   3. ls is O(klog k) for k children, because of sort
   4. directories are first class, name collision rule comes for free because a folder has one child map

# outline
common idea is "walk to the node at this path"

FileSystem:
    root = empty directory

    ls(path):
        node = find(path)
        if node is a file -> [node.name]
        else              -> sorted(names of node's children)

    mkdir(path):
        find(path, create_missing=True)
    
    addContentTofile(path, content):
        parent_path, name = split(path)
        parent = find(parent_path, create_missing=True)
        file = parent's child name, creating an empty file if absent
        file.content += content

    readContentFromFile(path):
        return find(path).content

    find(path, create_missing=False):
        node = root
        for each segment in path:
            if segment not in node.children and create_missing:
                make a directory for it
            else:
                node = node.children[segment]
        return node


# implementation

```python
class Node:
    def __init__(self, name, is_file=False):
        self.name = name
        self.is_file = is_file
        self.children = {} # name -> Node; used by directories
        self.content = "" # used by file

class FileSystem:
    def __init__(self):
        self.root = Node("")

    def ls(self, path):
        node = self._find(path)
        if node.is_file:
            return [node.name]
        else:
            return sorted(node.children)
    
    def mkdir(self, path):
        return self._find(path, create_missing=True)

    def addContentToFile(self, filePath, content):
        parent_path, _, name =  filePath.rpartition("/")
        if not name:
            raise ValueError(f"invalid file path: {filePath}") # edge case
        parent = self._find(parent_path)
        if file not in parent.children:
            parent.children[file] = Node(file, is_file=True)
        file = parent.children[file]
        if not file.is_file:
            raise IsDirectoryError(filePath) # edge case
        file.content += content

    def readContentFromFile(self, filePath):
        node = self._find(filePath).content
        if not node.is_file:
            raise IsDirectoryError(filePath) # edge case
        return node.content

    def _find(self, path, create_missing=False):
        node = self.root
        for segment in path.split("/"):
            if not segment: #[/a/b] -> ["", a, b]
                continue
            if node.is_file:
                raise NotDirectoryError(path) # edge
            if segment not in node.children:
                if not create_missing:
                    raise FileNotFoundEror(path) # edge
                node.children[segment] = Node(segment)
            
            node = node.children[segment]
        return node


```

# edge cases
```python
class Node:
    def __init__(self, name, is_file=False):
        self.name = name
        self.is_file = is_file
        self.children = {}      # name -> Node   (used by directories)
        self.content = ""       # used by files


class FileSystem:
    def __init__(self):
        # root = empty directory
        self.root = Node("")

    def ls(self, path):
        # node = find(path)
        node = self._find(path)
        # if node is a file -> [node.name]
        if node.is_file:
            return [node.name]
        # else -> sorted(names of node's children)
        return sorted(node.children)

    def mkdir(self, path):
        # find(path, create_missing=True)
        node = self._find(path, create_missing=True)
        if node.is_file:                                   # EDGE #4: dir over a file
            raise FileExistsError(f"{path} is a file")

    def addContentToFile(self, filePath, content):
        # parent_path, name = split(path)
        parent_path, _, name = filePath.rpartition("/")
        if not name:                                       # EDGE #5: "/" or trailing "/"
            raise ValueError(f"invalid file path: {filePath!r}")
        # parent = find(parent_path, create_missing=True)
        parent = self._find(parent_path, create_missing=True)
        # file = parent's child `name`, creating an empty file if absent
        if name not in parent.children:
            parent.children[name] = Node(name, is_file=True)
        file = parent.children[name]
        if not file.is_file:                               # EDGE #6: name is a directory
            raise IsADirectoryError(filePath)
        # file.content += content
        file.content += content

    def readContentFromFile(self, filePath):
        # return find(path).content
        node = self._find(filePath)
        if not node.is_file:                               # EDGE #8: reading a directory
            raise IsADirectoryError(filePath)
        return node.content

    def _find(self, path, create_missing=False):
        # node = root
        node = self.root
        # for each segment in path:
        for segment in path.split("/"):
            if not segment:                                # EDGE #3: "/", "a//b", "a/b/"
                continue
            if node.is_file:                               # EDGE #2: path goes through a file
                raise NotADirectoryError(path)
            # if segment not in node.children and create_missing: make a directory
            if segment not in node.children:
                if not create_missing:                     # EDGE #1: nonexistent path
                    raise FileNotFoundError(path)
                node.children[segment] = Node(segment)
            # node = node.children[segment]
            node = node.children[segment]
        return node

```

# complexity
Time: mkdir, addContentToFile, and readContentFromFile are O(L) in path length. ls is O(L + k log k) for k children.
Space: O(total nodes + total content).
Follow-up 1: Repeated += on strings can be O(n) each. If appends are heavy, I’d store a list of chunks and "".join lazily on read.
Follow-up 2: To keep ls at O(k) instead of O(k log k), I could keep children in a sorted container, at the cost of slower inserts.
Follow-up 3: For rm, mv, or cp, the tree design makes them natural: detach or reattach a subtree under a new parent.
Follow-up 4: For thread safety, I’d start with a per-directory lock and acquire locks in path order to avoid deadlocks.
