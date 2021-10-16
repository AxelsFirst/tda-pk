def euclidean_metric(p1, p2):
    """

    Find the euclidean distance between to `Point` objects.

    Parameters:
    -----------
    p1 : tda.Point
    p2 : tda.Point

    Returns:
    --------
    float
        Distance between the points.

    """

    d = 0
    for x, y in zip(p1.coords, p2.coords):
        d += (y - x) ** 2
    return d ** (1 / 2)
