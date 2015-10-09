#!/usr/bin/python
#
# Connected components for undirected graphs.
# Strongly connected components for directed graphs.

#from bfs import BFSWithQueue as SimpleBFS
from bfs import SimpleBFS

#from dfs import DFSWithStack as SimpleDFS
#from dfs import DFSWithRecursion as SimpleDFS
from dfs import SimpleDFS


class StronglyConnectedComponents:
    """Strongly connected components for directed graphs."""

    def __init__(self, graph):
        """The algorithm initialization."""
        if not graph.is_directed():
            raise ValueError("the graph is not directed")
        self.graph = graph
        self.scc = dict((node, None) for node in self.graph.iternodes())
        self.n_scc = 0

    def run(self):
        """Executable pseudocode."""
        algorithm = SimpleDFS(self.graph)
        order = []
        # use post_action!
        algorithm.run(post_action=lambda node: order.append(node))
        order.reverse()
        algorithm = SimpleDFS(self.graph.transpose())
        for source in order:
            if self.scc[source] is None:
                algorithm.run(source, pre_action=lambda
                    node: self.scc.__setitem__(node, self.n_scc))
                self.n_scc = self.n_scc + 1


class ConnectedComponentsBFS:
    """Connected components for undirected graphs."""

    def __init__(self, graph):
        """The algorithm initialization."""
        if graph.is_directed():
            raise ValueError("the graph is directed")
        self.graph = graph
        self.cc = dict((node, None) for node in self.graph.iternodes())
        self.n_cc = 0

    def run(self):
        """Executable pseudocode."""
        algorithm = SimpleBFS(self.graph)
        for source in self.graph.iternodes():
            if self.cc[source] is None:
                algorithm.run(source, pre_action=lambda node:
                    self.cc.__setitem__(node, self.n_cc))
                self.n_cc = self.n_cc + 1


class ConnectedComponentsDFS:
    """Connected components for undirected graphs."""

    def __init__(self, graph):
        """The algorithm initialization."""
        if graph.is_directed():
            raise ValueError("the graph is directed")
        self.graph = graph
        self.cc = dict((node, None) for node in self.graph.iternodes())
        self.n_cc = 0

    def run(self):
        """Executable pseudocode."""
        algorithm = SimpleDFS(self.graph)
        for source in self.graph.iternodes():
            if self.cc[source] is None:
                algorithm.run(source, pre_action=lambda node:
                    self.cc.__setitem__(node, self.n_cc))
                self.n_cc = self.n_cc + 1


def is_connected(graph):
    """Test if the undirected graph is connected."""
    if graph.is_directed():
        raise ValueError("the graph is directed")
    algorithm = SimpleDFS(graph)
    order = list()
    source = graph.iternodes().next()
    algorithm.run(source, lambda node: order.append(node))
    return len(order) == graph.v()

# EOF
