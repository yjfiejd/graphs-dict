#!/usr/bin/python
#
# connected.py
#
# Connected components for undirected graphs.

#from bfs import BFSWithQueue as BFS
from bfs import SimpleBFS as BFS

#from dfs import DFSWithStack as DFS
#from dfs import DFSWithRecursion as DFS
from dfs import SimpleDFS as DFS

class ConnectedComponentsBFS:

    def __init__(self, graph):
        """The algorithm initialization."""
        if graph.is_directed():
            raise ValueError("graph is directed")
        self.graph = graph
        self.cc = dict()
        self.n_cc = 0

    def run(self):
        """Executable pseudocode."""
        for source in self.graph.iternodes():
            if source not in self.cc:
                algorithm = BFS(self.graph)
                algorithm.run(source, 
                pre_action=lambda node: self.cc.__setitem__(node, self.n_cc))
                self.n_cc = self.n_cc + 1


class ConnectedComponentsDFS:

    def __init__(self, graph):
        """The algorithm initialization."""
        if graph.is_directed():
            raise ValueError("graph is directed")
        self.graph = graph
        self.visited = dict(((node, False) for node in self.graph.iternodes()))
        self.cc = dict()
        self.n_cc = 0

    def run(self):
        """Executable pseudocode."""
        for source in self.graph.iternodes():
            if not self.visited[source]:
                algorithm = DFS(self.graph)
                algorithm.run(source, 
                pre_action=lambda node: self.cc.__setitem__(node, self.n_cc),
                post_action=lambda node: self.visited.__setitem__(node, True))
                self.n_cc = self.n_cc + 1

# EOF