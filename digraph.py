"""
Graph module for undirected graphs.
"""

import random

try:
    import display
except:
    print("Warning: failed to load display module.  Graph drawing will not work.")
    
class Digraph:
    """
    Directed graph.  The vertices must be immutable.

    To create an empty graph:
    >>> G = Digraph()
    >>> (G.num_vertices(), G.num_edges())
    (0, 0)

    To create a circular graph with 3 vertices:
    >>> G = Digraph([(1, 2), (2, 3), (3, 1)])
    >>> (G.num_vertices(), G.num_edges())
    (3, 3)
    """

    def __init__(self, edges = None):
        self._tosets = {}
        self._fromsets = {}

        if edges:
            for e in edges: self.add_edge(e)

    def __repr__(self):
        return "Digraph({}, {})".format(self.vertices(), self.edges())

    def add_vertex(self, v):
        """
        Adds a vertex to the graph.  It starts with no edges.
        
        >>> G = Digraph()
        >>> G.add_vertex(1)
        >>> G.vertices() == {1}
        True
        """
        if v not in self._tosets:
            self._tosets[v] = set()
            self._fromsets[v] = set()

    def add_edge(self, e):
        """
        Adds an edge to graph.  If vertices in the edge do not exist, it adds them.
        
        >>> G = Digraph()
        >>> G.add_vertex(1)
        >>> G.add_vertex(2)
        >>> G.add_edge((1, 2))
        >>> G.add_edge((2, 1))
        >>> G.add_edge((3, 4))
        >>> G.add_edge((1, 2))
        >>> G.num_edges()
        3
        >>> G.num_vertices()
        4
        """
        # Adds the vertices (in case they don't already exist)
        for v in e:
            self.add_vertex(v)

        # Add the edge
        self._tosets[e[0]].add(e[1])
        self._fromsets[e[1]].add(e[0])

    def edges(self):
        """
        Returns the set of edges in the graph as ordered tuples.

        Running time is O(m + n) where n is the number of vertices
          and m is the number of edges
        """
        return { (v, w) for v in self._tosets for w in self._tosets[v] }

    def vertices(self):
        """
        Returns the set of vertices in the graph.
        """
        return set(self._tosets.keys())

    def draw(self, filename, attr = {}):
        """
        Draws the graph into a dot file.
        """
        display.write_dot_desc((self.vertices(), self.eges()), filename, attr)

    def num_edges(self):
        """
        Returns the number of edges in the graph.
        """
        m = 0
        for v in self._tosets:
            m += len(self._tosets[v])
        return m

    def num_vertices(self):
        """
        Returns the number of vertices in the graph.
        """
        return len(self._tosets)

    def adj_to(self, v):
        """
        Returns the set of vertices that contain an edge from v.

        >>> G = Digraph()
        >>> for v in [1, 2, 3]: G.add_vertex(v)
        >>> G.add_edge((1, 3))
        >>> G.add_edge((1, 2))
        >>> G.adj_to(3) == set()
        True
        >>> G.adj_to(1) == { 2, 3 }
        True
        """
        return self._tosets[v]

    def adj_from(self, v):
        """
        Returns the set of vertices that contain an edge to v.

        >>> G = Digraph()
        >>> G.add_edge((1, 3))
        >>> G.add_edge((2, 3))
        >>> G.adj_from(1) == set()
        True
        >>> G.adj_from(3) == { 1, 2 }
        True
        """
        return self._fromsets[v]

    def is_path(self, path):
        """
        Returns True if the list of vertices in the argument path are a
        valid path in the graph.  Returns False otherwise.

        >>> G = Digraph([(1, 2), (2, 3), (2, 4), (1, 5), (2, 5), (4, 5), (5, 2)])
        >>> G.is_path([1, 5, 2, 4, 5])
        True
        >>> G.is_path([1, 5, 4, 2])
        False

        >>> G.is_path([1, 1, 1, 1])
        True
        >>> G.is_path([5, 2, 5, 2, 5, 4, 5])
        False
        >>> G.is_path([5, 2, 5, 2, 5])
        True
        >>> G.is_path([5, 4, 2, 5, 1])
        False
        >>> G.is_path([])
        False
        >>> G.is_path([1])
        True
        >>> G.is_path('asdf')
        False
        >>> G.is_path(None)
        False
        >>> G.is_path(1)
        False
        >>> G.is_path([1, 3])
        False
        """
         # If not a valid list, return false
        if type(path) != list:
            return False

        # If empty list, return false
        if len(path) == 0:
            return False
        
        # Attempts to see if there is an element in the path
        # Sets first element as previous for base case
        # Will always be previous cursor for every other case
        # This makes a single point a valid path from itself to itself
        prevertex = path[0]
        value = False
        for vertex in path:
            if (vertex in self.adj_to(prevertex)) or (vertex == prevertex):
                value = True
                prevertex = vertex
            else:
                value = False
                break
        return value

def random_graph(n, m):
    """
    Make a random Digraph with n vertices and m edges.

    >>> G = random_graph(10, 5)
    >>> G.num_edges()
    5
    >>> G.num_vertices()
    10
    >>> G = random_graph(1, 1)
    Traceback (most recent call last):
    ...
    ValueError: For 1 vertices, you wanted 1 edges, but can only have a maximum of 0
    """
    G = Digraph()
    for v in range(n):
        G.add_vertex(v)

    max_num_edges = n * (n-1)
    if m > max_num_edges:
        raise ValueError("For {} vertices, you wanted {} edges, but can only have a maximum of {}".format(n, m, max_num_edges))

    while G.num_edges() < m:
        G.add_edge(random.sample(range(n), 2))

    return G

def spanning_tree(G, start):  
    """ 
    Runs depth-first-search on G from vertex start to create a spanning tree.
    """
    visited = set()
    todo = [ (start, None) ]

    T = Digraph()
    
    while todo:
        (cur, e) = todo.pop()

        if cur in visited: continue

        visited.add(cur)
        if e: T.add_edge(e)

        for n in G.adj_to(cur):
            if n not in visited:
                todo.append((n, (cur, n)))
                
    return T

def shortest_path(G, source, dest):
    """
    Returns the shortest path from vertex source to vertex dest.

    >>> G = Digraph([(1, 2), (2, 3), (3, 4), (4, 5), (1, 6), (3, 6), (6, 7)])
    >>> path = shortest_path(G, 1, 7)
    >>> path
    [1, 6, 7]
    >>> G.is_path(path)
    True

    >>> G = Digraph([(1, 2), (2, 3), (3, 4), (1, 5), (6, 7), (7, 8), (4, 6)])
    >>> path = shortest_path(G, 1, 8)
    >>> path
    [1, 2, 3, 4, 6, 7, 8]
    >>> G.is_path(path)
    True

    This should return nothing, because of directionality
    >>> G = Digraph([(-4, -5), (53, 5), (5, -5)])
    >>> path = shortest_path(G, -4, 53)
    >>> path
    >>> G.is_path(path)
    False

    However, this is okay
    >>> G = Digraph([(-4, -5), (53, 5), (-5, 5), (5, 53)])
    >>> path = shortest_path(G, -4, 53)
    >>> path
    [-4, -5, 5, 53]
    >>> G.is_path(path)
    True
    
    These two paths have 2 different paths of the same distance
    >>> G = Digraph([(1, 2), (1, 3), (2, 4), (3, 4)])
    >>> path = shortest_path(G, 1, 4)
    >>> path
    [1, 2, 4]
    >>> G.is_path(path)
    True

    This one still picks [1, 2, 4] instead of [1, 3, 4] for some reason (still correct)
    >>> G = Digraph([(1, 3), (1, 2), (3, 4), (2, 4)])
    >>> path = shortest_path(G, 1, 4)
    >>> path
    [1, 2, 4]
    >>> G.is_path(path)
    True

    These should return nothing
    >>> G = Digraph([(1, 2), (1, 3), (7, 10)])
    >>> path = shortest_path(G, 1, 10)
    >>> path
    >>> G.is_path(path)
    False

    >>> G = Digraph([(1, 2), (2, 3), (3, 4), (1, 5), (6, 7), (7, 8)])
    >>> path = shortest_path(G, 1, 8)
    >>> path
    >>> G.is_path(path)
    False
    """
    parent = {}
    queue = []
    queue.append(source)
    
    while queue:
        cur = queue.pop(0)
        if cur == dest:
            path = [dest]
            while path[-1] != source:
                path.append(parent[path[-1]])
            path.reverse()
            return path

        for i in G.adj_to(cur):
            if i not in parent:
                parent[i] = cur
                queue.append(i)
    else:
        return None


def least_cost_path(G, start, dest, cost):
    """
    path = least_cost_path(G, start, dest, cost)

    least_cost_path returns a least cost path in the digraph G from vertex
    start to vertex dest, where costs are defined by the cost function.
    cost should be a function that takes a single edge argument and returns
    a real-valued cost.

    if there is no path, then returns None
    the path from start to start is [start]

    The following test cases should emulate shortest_path

    >>> G = Digraph();
    >>> def testcost(e): return 1
    
    Empty Digraph, should return no path
    >>> least_cost_path(G, 1, 2, testcost) == None
    True

    Path created from vertex 1 to 2, edge created
    >>> G.add_edge((1, 2))
    >>> a = least_cost_path(G, 1, 2, testcost)
    >>> a == [1, 2]
    True

    >>> b = least_cost_path(G, 2, 1, testcost)
    >>> b == None
    True
    
    >>> G.add_edge((2, 3))
    >>> c = least_cost_path(G, 1, 3, testcost)
    >>> c == [1, 2, 3]
    True

    >>> G.add_edge((3, 4))
    >>> G.add_edge((2, 4))
    >>> d = least_cost_path(G, 1, 4, testcost)
    >>> d == [1, 2, 4]
    True

    Using server values now
    >>> import server
    >>> e = least_cost_path(server.G, 277466945, 277466941, server.cost_distance)
    >>> print(e)
    [277466945, 277466943, 277466942, 277466941]

    >>> f = least_cost_path(server.G, 354287616, 406847557, server.cost_distance)
    >>> print(f)
    

    """
    todo = {start: 0}
    visited = set()
    parent = {}

    # Check if the start and dest are in the given graph
    if not(start in G.vertices() and dest in G.vertices()):
        return None

    # If the vertices exist, check if a path exists between the two vertices:
    if shortest_path(G, start, dest) == None:
        return None
    
    # At this point, it is verified that a path eists between the two vertices:
    while todo and (dest not in visited):
        (cur, c) = min(todo.items(), key = lambda x: x[1])
        todo.pop(cur)

        visited.add(cur)

        for n in G.adj_to(cur):
            if n in visited: continue
            if n not in todo or ( c + cost((cur,n)) < todo[n] ):
                todo[n] = c + cost((cur,n))
                parent[n] = cur

    # extract path
    path = [dest]
    while path[-1] != start:
        path.append(parent[path[-1]])
    path.reverse()
    
    if G.is_path(path) == True:
        return path

    else:
        return None


def compress(walk):
    """
    Remove cycles from a walk to create a path.
    
    >>> compress([1, 2, 3, 4])
    [1, 2, 3, 4]
    >>> compress([1, 3, 0, 1, 6, 4, 8, 6, 2])
    [1, 6, 2]
    """
    
    lasttime = {}

    for (i,v) in enumerate(walk):
        lasttime[v] = i

    rv = []
    i = 0
    while (i < len(walk)):
        rv.append(walk[i])
        i = lasttime[walk[i]]+1

    return rv
    
            

if __name__ == "__main__":
    import doctest
    doctest.testmod()
