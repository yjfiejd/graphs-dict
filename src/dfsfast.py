#!/usr/bin/python

from edges import Edge
from collections import deque


class DFSWithStack:
    """Depth-First Search with a stack."""

    def __init__(self, graph):
        """The algorithm initialization."""
        self.graph = graph
        self.color = dict(((node, "WHITE") for node in self.graph.iternodes()))
        self.prev = dict(((node, None) for node in self.graph.iternodes()))
        self.time = 0    # time stamp
        self.dd = dict()
        self.ff = dict()

    def run(self, source=None, pre_action=None, post_action=None):
        """Executable pseudocode."""
        if source is not None:
            self.visit(source, pre_action, post_action)
        else:
            for node in self.graph.iternodes():
                if self.color[node] == "WHITE":
                    self.visit(node, pre_action, post_action)

    def visit(self, node, pre_action=None, post_action=None):
        """Explore the connected component,"""
        self.time = self.time + 1
        self.dd[node] = self.time
        self.color[node] = "GREY"
        Q = deque()
        Q.append(node)   # node is GREY
        if pre_action:   # when Q.append
            pre_action(node)
        while len(Q) > 0:
            source = Q.pop()    # przetwarzam szary node
            for target in self.graph.iteradjacent(source):
                if self.color[target] == "WHITE":
                    self.prev[target] = source
                    self.time = self.time + 1
                    self.dd[target] = self.time
                    self.color[target] = "GREY"
                    Q.append(target)   # target is GREY
                    if pre_action:   # when Q.append
                        pre_action(target)
            self.time = self.time + 1
            self.ff[source] = self.time
            self.color[source] = "BLACK"
            if post_action:   # source became BLACK
                post_action(source)

    def to_tree(self):
        """The spanning tree is built."""
        tree = self.graph.__class__(self.graph.v(), directed=False)
        for node in self.graph.iternodes():
            if self.prev[node] is not None:
                # tree edge (parent, node)
                tree.add_edge(Edge(self.prev[node], node))
        return tree

    def to_dag(self):
        """Returns the spanning tree as a dag."""
        dag = self.graph.__class__(self.graph.v(), directed=True)
        for node in self.graph.iternodes():
            if self.prev[node] is not None:
                # Edge(parent, node)
                dag.add_edge(Edge(self.prev[node], node))
        return dag


class DFSWithRecursion:
    """Depth-First Search with a recursion."""

    def __init__(self, graph):
        """The algorithm initialization."""
        self.graph = graph
        self.color = dict(((node, "WHITE") for node in self.graph.iternodes()))
        self.prev = dict(((node, None) for node in self.graph.iternodes()))
        self.time = 0    # time stamp
        self.dd = dict()
        self.ff = dict()
        # ciekawe ustawianie rekurencji
        import sys
        recursionlimit = sys.getrecursionlimit()
        sys.setrecursionlimit(max(self.graph.v()*2, recursionlimit))

    def run(self, source=None, pre_action=None, post_action=None):
        """Executable pseudocode."""
        if source is not None:
            self.visit(source, pre_action, post_action)
        else:
            for node in self.graph.iternodes():
                if self.color[node] == "WHITE":
                    self.visit(node, pre_action, post_action)

    def visit(self, node, pre_action=None, post_action=None):
        """Explore recursively the connected component."""
        self.time = self.time + 1
        self.dd[node] = self.time
        self.color[node] = "GREY"
        if pre_action:   # visit started
            pre_action(node)
        for target in self.graph.iteradjacent(node):
            if self.color[target] == "WHITE":
                self.prev[target] = node
                self.visit(target, pre_action, post_action)
        self.time = self.time + 1
        self.ff[node] = self.time
        self.color[node] = "BLACK"
        if post_action:   # node became BLACK
            post_action(node)

    def to_tree(self):
        """The spanning tree is built."""
        tree = self.graph.__class__(self.graph.v(), directed=False)
        for node in self.graph.iternodes():
            if self.prev[node] is not None:
                # tree edge (parent, node)
                tree.add_edge(Edge(self.prev[node], node))
        return tree

    def to_dag(self):
        """Returns the spanning tree as a dag."""
        dag = self.graph.__class__(self.graph.v(), directed=True)
        for node in self.graph.iternodes():
            if self.prev[node] is not None:
                # Edge(parent, node), out-tree
                dag.add_edge(Edge(self.prev[node], node))
        return dag


class SimpleDFS:
    """Depth-First Search with a recursion."""

    def __init__(self, graph):
        """The algorithm initialization."""
        self.graph = graph
        self.prev = dict()
        # ciekawe ustawianie rekurencji
        import sys
        recursionlimit = sys.getrecursionlimit()
        sys.setrecursionlimit(max(self.graph.v() * 2, recursionlimit))

    def run(self, source=None, pre_action=None, post_action=None):
        """Executable pseudocode."""
        if source is not None:
            self.prev[source] = None   # before visit
            self.visit(source, pre_action, post_action)
        else:
            for node in self.graph.iternodes():
                if node not in self.prev:
                    self.prev[node] = None   # before visit
                    self.visit(node, pre_action, post_action)

    def visit(self, node, pre_action=None, post_action=None):
        """Explore recursively the connected component."""
        if pre_action:
            pre_action(node)
        for target in self.graph.iteradjacent(node):
            if target not in self.prev:
                self.prev[target] = node   # before visit
                self.visit(target, pre_action, post_action)
        if post_action:
            post_action(node)

    def to_tree(self):
        """The spanning tree is built."""
        tree = self.graph.__class__(self.graph.v(), directed=False)
        for node in self.graph.iternodes():
            if self.prev[node] is not None:
                # tree edge (parent, node)
                tree.add_edge(Edge(self.prev[node], node))
        return tree

    def to_dag(self):
        """Returns the spanning tree as a dag."""
        dag = self.graph.__class__(self.graph.v(), directed=True)
        for node in self.graph.iternodes():
            if self.prev[node] is not None:
                # Edge(parent, node), out-tree
                dag.add_edge(Edge(self.prev[node], node))
        return dag

# EOF