#!/usr/bin/python

from Queue import Queue


class BorieDominatingSet:
    """Find a minimum cardinality dominating set for trees.
    
    Attributes
    ----------
    graph : input forest
    dominating_set : set with nodes
    parent : dict (DFS tree)
    cardinality : number (the size of min dset)
    
    Notes
    -----
    Based on
    
    Richard B. Borie, R. Gary Parker, Craig A. Tovey, 
    Solving Problems on Recursively Constructed Graphs,
    ACM Computing Surveys 41, 4 (2008).
    """

    def __init__(self, graph):
        """The algorithm initialization."""
        if graph.is_directed():
            raise ValueError("the graph is directed")
        self.graph = graph
        self.parent = dict()
        self.dominating_set = set()
        self.cardinality = 0
        import sys
        recursionlimit = sys.getrecursionlimit()
        sys.setrecursionlimit(max(self.graph.v() * 2, recursionlimit))

    def run(self, source=None):
        """Executable pseudocode."""
        if source is not None:
            # A single connected component, a single tree.
            self.parent[source] = None   # before _visit
            a2_set, b2_set, c2_set = self._visit(source)
            self.dominating_set.update(min([a2_set, b2_set], key=len))
            self.cardinality = len(self.dominating_set)
        else:
            # A forest is possible.
            for node in self.graph.iternodes():
                if node not in self.parent:
                    self.parent[node] = None   # before _visit
                    a2_set, b2_set, c2_set = self._visit(node)
                    self.dominating_set.update(min([a2_set, b2_set], key=len))
            self.cardinality = len(self.dominating_set)

    def _compose(self, arg1, arg2):
        """Compose results."""
        # a_set : min dset that includes root
        # b_set : min dset that excludes root
        # c_set : root undominated
        a1_set, b1_set, c1_set = arg1
        a2_set, b2_set, c2_set = arg2
        a_set = a1_set | min(arg2, key=len)
        b_set = min([b1_set | a2_set, b1_set | b2_set,
            c1_set | a2_set], key=len)
        c_set = c1_set | b2_set
        return (a_set, b_set, c_set)

    def _visit(self, root):
        """Explore recursively the connected component."""
        # Start from a single node.
        arg1 = (set([root]), set([root]), set())
        for target in self.graph.iteradjacent(root):
            if target not in self.parent:
                self.parent[target] = root   # before _visit
                arg2 = self._visit(target)
                arg1 = self._compose(arg1, arg2)
        return arg1


class TreeDominatingSet:
    """Find a maximum dominating set for trees.
    
    Attributes
    ----------
    graph : input forest
    dominating_set : set with nodes
    cardinality : number (the size of min dset)
    _used : set, private
    """

    def __init__(self, graph):
        """The algorithm initialization."""
        if graph.is_directed():
            raise ValueError("the graph is directed")
        self.graph = graph
        self.dominating_set = set()
        self.cardinality = 0
        self._used = set()   # for dset and neighbors

    def run(self):
        """Executable pseudocode."""
        # A dictionary with node degrees, O(V) time.
        degree_dict = dict((node, self.graph.degree(node))
            for node in self.graph.iternodes())
        Q = Queue()   # for leafs
        # Put leafs to the queue, O(V) time.
        for node in self.graph.iternodes():
            if degree_dict[node] == 0:
                self.dominating_set.add(node)   # isolated node from the beginning
                self._used.add(node)
                self.cardinality += 1
            elif degree_dict[node] == 1:   # leaf
                Q.put(node)
        while not Q.empty():
            source = Q.get()
            # A leaf may become isolated.
            if degree_dict[source] == 0:
                if source in self._used:   # parent in dset
                    pass
                else:   # parent not in dset
                    self.dominating_set.add(source)
                    self._used.add(source)
                    self.cardinality += 1
            elif degree_dict[source] == 1:
                if source in self._used:
                    # Remove such leaf.
                    for node in self.graph.iteradjacent(source):
                        if degree_dict[node] > 0:   # this is parent
                            degree_dict[node] -= 1
                            degree_dict[source] -= 1
                            if degree_dict[node] == 1:   # new leaf
                                Q.put(node)
                            break
                else:   # source not in used, parent go to dset
                    for target in self.graph.iteradjacent(source):
                        if degree_dict[target] > 0:   # this is parent
                            self.dominating_set.add(target)
                            self._used.add(target)
                            self.cardinality += 1
                            # Remove edges going from target.
                            for node in self.graph.iteradjacent(target):
                                if degree_dict[node] > 0:
                                    degree_dict[node] -= 1
                                    degree_dict[target] -= 1
                                    self._used.add(node)   # child goes to used
                                    if degree_dict[node] == 1:   # new leaf
                                        Q.put(node)
                            break