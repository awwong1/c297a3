import digraph
import readModule
import sys

debug = 1

def cost_distance(e):
    """                                                                                   
    cost_distance returns the straight-line distance between the two           
    vertices at the endpoints of the edge e.                     

    e is defined as (start, stop)                                                        
    vertices start, stop are defined as (id: lat, long)

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

# load the Edmonton map data into a digraph object, and store the
# ancillary information about street names and vertex locations
(E, E_name, V, V_coord) = readModule.read_graph('edmonton-roads-digraph.txt')

G = digraph.Digraph(E)

while (debug == 0):
    # look for input of lat/lon
    (start_lat, start_lon, dest_lat, dest_lon) = input("lat1 lon1 lat2 lon2: ").split(' ')

    # find vertex associated with lat/lon
    start = readModule.value_search(V_coord, float(start_lat), float(start_lon))
    dest = readModule.value_search(V_coord, float(dest_lat), float(dest_lon))

## TODO: make sure start and dest are valid vertices

    # find least_cost_path
    path = digraph.least_cost_path(G, start, dest, cost_distance)
    print(path)
## TODO: print the path information correctly

if __name__ == "__main__":
    import doctest
    doctest.testmod()
