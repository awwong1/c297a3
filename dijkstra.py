import digraph

def least_cost_path(G, start, dest, cost):
    """
    path = least_cost_path(G, start, dest, cost)

    least_cost_path returns a least cost path in the digraph G from vertex
    start to vertex dest, where costs are defined by the cost function.
    cost should be a function that takes a single edge argument and returns
    a real-valued cost.

    if there is no path, then returns None

    the path from start to start is [start]

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

    # todo[v] is the current best estimate of cost to get from start to v 
    todo = { start: 0}

    # v in visited when the vertex v's least cost from start has been determined
    visited = set()

    # parent[v] is the vertex that just precedes v in the path from start to v
    parent = {}

    # Check if the start and dest are in the given graph
    if not(start in G.vertices() and dest in G.vertices()):
        return None

    # If the vertices exist, check if a path exists between the two vertices:
    if digraph.shortest_path(G, start, dest) == None:
        return None

    while todo and (dest not in visited):

        # priority queue operation
        # remove smallest estimated cost vertex from todo list

        # items from the todo dictionary
        (cur,c) = min(todo.items(), key=lambda x: x[1])
        todo.pop(cur)

        # it is now visited, and will never have a smaller cost
        visited.add(cur)

        for n in G.adj_to(cur):
            if n in visited: continue
            if n not in todo or ( c + cost((cur,n)) < todo[n] ):
                todo[n] = c + cost((cur,n))
                parent[n] = cur

    # if there is a path, extract it.  The graph may be disconnected
    # so in that case return None
    # extract path
    path = [dest]
    while path[-1] != start:
        path.append(parent[path[-1]])
    path.reverse()
    
    if G.is_path(path) == True:
        return path

    else:
        return None

if __name__ == "__main__":
    import doctest
    doctest.testmod()
