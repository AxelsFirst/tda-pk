def are_unique(points):
    """

    Check if a list of `Point` objects is unique.

    Parameters:
    -----------
    points: list
        A list of `Point` objects.

    Output:
    -------
    bool:
        True if points are unique else False.

    """

    seen = set()
    for p in points:
        coords = tuple(p.coords)
        if coords not in seen:
            seen.add(coords)
        else:
            return False

    seen = set()
    for p in points:
        name = p.name
        if name not in seen:
            seen.add(name)
        else:
            return False

    return True
