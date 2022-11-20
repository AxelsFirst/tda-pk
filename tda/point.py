class Point(object):
    """

    A point in n-dimensional euclidean space.

    Parameters:
    -----------
    name : str
        The name of the `Point`.
    coords: list
        A list of floats.

    """

    def __init__(self, name, coords):
        self.name = name
        self.coords = coords

    def __str__(self):
        return self.name
