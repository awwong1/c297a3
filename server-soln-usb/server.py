import digraph
import readModule
import dijkstra
import sys
import serial
import argparse

global debug
debug = False

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

# dumbserver code begins here

def send(serial_port, message):
    """
    Sends a message back to the client device.
    """
    full_message = ''.join((message, "\n"))

    (debug and print("server:" + full_message + ":") )

    reencoded = bytes(full_message, encoding='ascii')
    serial_port.write(reencoded)


def receive(serial_port, timeout=None):
    """
    Listen for a message. Attempt to timeout after a certain number of
    milliseconds.
    """
    raw_message = serial_port.readline()
    debug and print("client:", raw_message, ":")
    message = raw_message.decode('ascii')
    return message.rstrip("\n\r")



def parse_args():
    """
    Parses arguments for this program.
    Returns an object with the following members:
        args.
             serialport -- str
             verbose    -- bool
             graphname  -- str
    """

    parser = argparse.ArgumentParser(
        description='Assignment 1: Map directions.',
        epilog = 'If SERIALPORT is not specified, stdin/stdout are used.')
    parser.add_argument('-s', '--serial',
                        help='path to serial port',
                        dest='serialport',
                        default=None)
    parser.add_argument('-v', dest='verbose',
                        help='verbose',
                        action='store_true')
    parser.add_argument('-g', '--graph',
                        help='path to graph (DEFAULT = " edmonton-roads-2.0.1.txt")',
                        dest='graphname',
                        default=' edmonton-roads-2.0.1.txt')
    return parser.parse_args()

#dumbserver code ends here

if __name__ == "__main__":
    args = parse_args()
    
    # load the Edmonton map data into a digraph object, and store the
    # ancillary information about street names and vertex locations
    (E, E_name, V, V_coord) = readModule.read_graph(args.graphname)
    G = digraph.Digraph(E)

    # Initialize some stuff...
    if args.serialport:
        print("Opening serial port: %s" % args.serialport)
        serial_out = serial_in =  serial.Serial(args.serialport, 9600)
    else:
        print("No serial port.  Supply one with the -s port option")
        exit()

    if args.verbose:
        debug = True
    else:
        debug = False


    while True:
        # look for input of lat/lon
        
        msg = receive(serial_in)
        debug and print("GOT:" + msg + ":", file=sys.stderr)
        fields = msg.split(' ');
        if len(fields) != 4:
            continue;
        (start_lat, start_lon, dest_lat, dest_lon) = fields;
        # send(serial_out, "2")
        # send(serial_out, fields[0]+" "+fields[1])
        # send(serial_out, fields[2]+" "+fields[3])

        start = readModule.value_search(V_coord, int(start_lat), int(start_lon))
        dest = readModule.value_search(V_coord, int(dest_lat), int(dest_lon))
        
        # find least_cost_path
        path = dijkstra.least_cost_path(G, start, dest, cost_distance)
        send(serial_out, str(len(path)))
        # print(total_distance(path, cost_distance))
        
        # print path in "lat lon" format
        if path is not None:
            for vertex in path:
                waypoint = V_coord[vertex]
                send(serial_out, str(waypoint[0]) + ' ' + str(waypoint[1]))
                
    # import doctest
    # doctest.testmod()
