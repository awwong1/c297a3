"""
map.py

"""

class Map:
    """
    The constructor class
    >>> m = Map("test.map")
    >>> p = m.get_path( (0.0,0.0), (0.0,0.0) )
    >>> str(p)
    '[(0.0,0.0)]'
    """
    def __init__(self, file):
        pass

    def get_path(self, start_coord, stop_coord):
        return []
    
    def where_am_i(self, coord):
        pass

if __name__ == "__main__":
    import doctest
    doctest.testmod()
