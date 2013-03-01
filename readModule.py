import sys

def read_graph(digraph_file_name):
    digraph_file = open(digraph_file_name, 'r')

    V = set()
    E = set()
    V_coord = { }
    E_name = { }

    # process each line in the file
    for line in digraph_file:

        # strip all trailing whitespace
        line = line.rstrip()

        fields = line.split(",")
        type = fields[0]

        if type == 'V':
            # got a vertex record
            (id,lat,long) = fields[1:]

            # vertex id's should be ints
            id=int(id)

            # lat and long are ints
            lat=float(lat)
            long=float(long)

            V.add(id)
            V_coord[id] = (int(lat*100000), int(long*1000040))
        
        elif type == 'E':
            # got an edge record
            (start,stop,name) = fields[1:]

            # vertices are ints
            start=int(start)
            stop=int(stop)
            e = (start,stop)

            # get rid of leading and trailing quote " chars around name
            name = name.strip('"')

            # consistency check, we don't want auto adding of vertices when
            # adding an edge.
            if start not in V or stop not in V:
                raise Exception("Edge {} has an endpoint that is not a vertex".format(e) )

            E.add(e)
            E_name[e] = name
        else:
            # weird input
            raise Exception("Error: weird line |{}|".format(line))

    return (E, E_name, V, V_coord)

def value_search(V_coord, lat, lon):
    """
    reverse dictionary lookup - finds the key given value
    if no key exists, returns nearest key as defined by cost function
    >>> V_coord = {1: (2,2), 2:(3,4), 3:(6,2), 4:(53, -113)}
    >>> value_search(V_coord, 3, 4) == 2
    True
    >>> value_search(V_coord, 3, 2) == 1
    True

    >>> print(value_search(V_coord, 1000, 1000))
    3

    >>> print(value_search(V_coord, -1000, -1000))
    4

    >>> S_coord = {1: (14, 12), 2: (12, 14)}
    >>> value_search(S_coord, 11, 11) == 1
    True
    
    >>> T_coord = {1: (12, 14), 2: (14, 12)}
    >>> value_search(T_coord, 11, 11) == 1
    True

    """
    key = 0
    minimum = float("inf")

    # finds lat/lon if in V_coord
    for k,v in V_coord.items():
        if v == (lat, lon):
            key = k

    # finds closest vertex if lat/lon not in V_coord
    if key == 0:
        for k,v in V_coord.items():
            distance = ((lat - v[0])**2 + (lon - v[1])**2)**.5
            if distance < minimum:
                minimum = distance
                key = k

    return key


if __name__ == "__main__":
    import doctest
    doctest.testmod()
