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

            # lat and long are floats
            lat=float(lat)
            long=float(long)

            V.add(id)
            V_coord[id] = (lat,long)
        
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
    """
    for k,v in V_coord.items():
        if v == (lat, lon):
            return k
