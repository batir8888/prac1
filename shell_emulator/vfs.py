import json
from typing import Dict, Any, Tuple, Optional, List

class VFS:
    """Simple in-memory virtual file system."""
    def __init__(self, tree: Optional[Dict[str, Any]] = None):
        self.root: Dict[str, Any] = tree if tree is not None else {}

    @staticmethod
    def from_json_file(path: str) -> 'VFS':
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return VFS(data)

    def _resolve(self, path: str) -> Tuple[Dict[str, Any], str]:
        """Return parent directory dict and final name for given path."""
        if path.startswith('/'):
            cur = self.root
            parts = [p for p in path.split('/') if p][:-1]
            name = path.split('/')[-1]
        else:
            raise ValueError('Path must be absolute in VFS operations')
        for p in parts:
            if p not in cur or not isinstance(cur[p], dict):
                raise FileNotFoundError(f'Directory {p} not found')
            cur = cur[p]
        return cur, name

    def get_node(self, path: str) -> Any:
        if path == '/':
            return self.root
        if path.startswith('/'):
            cur = self.root
            parts = [p for p in path.split('/') if p]
        else:
            raise ValueError('Path must be absolute in VFS operations')
        for p in parts:
            if p not in cur:
                raise FileNotFoundError(path)
            cur = cur[p]
        return cur

    def list_dir(self, path: str) -> List[str]:
        node = self.get_node(path)
        if not isinstance(node, dict):
            raise NotADirectoryError(path)
        return sorted(node.keys())

    def make_dir(self, path: str) -> None:
        parent, name = self._resolve(path)
        if name in parent:
            raise FileExistsError(path)
        parent[name] = {}

    def make_file(self, path: str, content: str = '') -> None:
        parent, name = self._resolve(path)
        if name in parent and isinstance(parent[name], dict):
            raise IsADirectoryError(path)
        parent[name] = content

