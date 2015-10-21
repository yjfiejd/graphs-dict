#!/usr/bin/python

from Queue import Queue
#from graphtheory.algorithms.bipartite import BipartiteGraphBFS as Bipartite
from graphtheory.algorithms.bipartite import BipartiteGraphDFS as Bipartite


class HopcroftKarp:
    """Maximum-cardinality matching using the Hopcroft-Karp algorithm.
    
    Notes
    -----
    Based on pseudocode from:
    
    http://en.wikipedia.org/wiki/Hopcroft-Karp_algorithm
    """

    def __init__(self, graph):
        """The algorithm initialization."""
        self.graph = graph
        self.pair = dict((node, None) for node in self.graph.iternodes())
        self.distance = dict()
        self.cardinality = 0
        algorithm = Bipartite(self.graph)
        algorithm.run()
        self.v1 = list()   # or set()
        self.v2 = list()   # or set()
        for node in self.graph.iternodes():
            if algorithm.color[node] == 1:
                self.v1.append(node)   # or add()
            else:
                self.v2.append(node)   # or add()
        self.Q = Queue()   # for nodes from self.v1

    def run(self):
        """Executable pseudocode."""
        while self._bfs_stage():
            for node in self.v1:
                if self.pair[node] is None and self._dfs_stage(node):
                    self.cardinality = self.cardinality + 1
                    #print self.pair

    def _bfs_stage(self):
        """The BFS stage."""
        for node in self.v1:
            if self.pair[node] is None:
                self.distance[node] = 0
                self.Q.put(node)
            else:
                self.distance[node] = float("inf")
        self.distance[None] = float("inf")
        while not self.Q.empty():
            node = self.Q.get()
            if self.distance[node] < self.distance[None]:
                for edge in self.graph.iteroutedges(node):
                    if self.distance[self.pair[edge.target]] == float("inf"):
                        self.distance[self.pair[edge.target]] = self.distance[node] + 1
                        self.Q.put(self.pair[edge.target])
        return self.distance[None] != float("inf")

    def _dfs_stage(self, node):
        """The DFS stage."""
        if node is not None:
            for edge in self.graph.iteroutedges(node):
                if self.distance[self.pair[edge.target]] == self.distance[node] + 1:
                    if self._dfs_stage(self.pair[edge.target]):
                        self.pair[edge.target] = node
                        self.pair[node] = edge.target
                        return True
            self.distance[node] = float("inf")
            return False
        return True

# EOF