import digraph
import readModule
import dijkstra
import sys

def cost_distance(e):
    """                                                                                   
    cost_distance returns the straight-line distance between the two           
    vertices at the endpoints of the edge e.                     

    e is defined as (start, stop)                                                        
    vertices start, stop are defined as (id: lat, long)

    This function assumes that V_coord is already defined

    >>> a = 277466945
    >>> b = 277466941
    >>> c = (a,b)
    >>> print(cost_distance(c))
    0.002532184898450213

    """
    start_coord = V_coord[e[0]]
    stop_coord = V_coord[e[1]]

    lat_diff = (start_coord[0] - stop_coord[0])**2
    lon_diff = (start_coord[1] - stop_coord[1])**2
    distance = (lat_diff + lon_diff)**.5

    return distance

def total_distance(path, cost):
    """
    Total distance returns the sum of distances in a path.

    Calculate the distance beteen vertices from current vertex to next vertex
    Shift vertices over, continue until next vertex = end of path
    Sum all distances together.
    This situation uses the cost function defined above.
    NOTE: This function assumes that the list of vertices provided is a valid path

    >>> expected = total_distance([277466945, 277466943, 277466942, 277466941], cost_distance)
    >>> a = cost_distance((277466945, 277466943))
    >>> b = cost_distance((277466943, 277466942))
    >>> c = cost_distance((277466942, 277466941))
    >>> expected == a+b+c
    True
    """

    if path is None:
        return 0

    totaldistance = 0
    curver = None
    prever = None
    for i in path:
        curver = i
        if prever == None:
            prever = i
            # Notice, the distance from a vertex to itself is 0.0
            # This will only occur for the first iteration
        totaldistance += cost((prever, curver))
        prever = curver

    return totaldistance

# throw away executable name before processing command line arguments
argv = sys.argv[1:]

# if filename is supplied, use that, otherwise use stdin
if argv:
    digraph_file_name = argv.pop(0)
    digraph_file = open(digraph_file_name, 'r')
else:
    digraph_file = 'edmonton-roads-2.0.1.txt'

# load the Edmonton map data into a digraph object, and store the
# ancillary information about street names and vertex locations
(E, E_name, V, V_coord) = readModule.read_graph(digraph_file)
G = digraph.Digraph(E)

if __name__ == "__main__":
    while True:
        # look for input of lat/lon
        (start_lat, start_lon, dest_lat, dest_lon) = input(
            "lat1 lon1 lat2 lon2: ").split(' ')

        # find vertex associated with lat/lon
        start = readModule.value_search(V_coord, int(start_lat), int(start_lon))
        dest = readModule.value_search(V_coord, int(dest_lat), int(dest_lon))

        # find least_cost_path
        path = dijkstra.least_cost_path(G, start, dest, cost_distance)
        
        print(total_distance(path, cost_distance))

        # print path in "lat lon" format
        if path is not None:
            for vertex in path:
                waypoint = V_coord[vertex]
                print(str(waypoint[0]) + ' ' + str(waypoint[1]))


    import doctest
    doctest.testmod()
