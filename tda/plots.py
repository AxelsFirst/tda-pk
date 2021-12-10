import random

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from matplotlib.patches import Circle, Polygon
from scipy.spatial import ConvexHull


def draw_graph(complex, **kwargs):

    if complex.points and len(complex.points[0].coords) != 2:
        raise Exception('Only 2d plots are supported.')

    # Plot settings
    fig, ax = plt.subplots()
    fig.set_figheight(kwargs['fig_width'])
    fig.set_figwidth(kwargs['fig_height'])
    fig.set_dpi(kwargs['fig_dpi'])
    ax.axis('equal')

    # Draw graph
    pos = {p: p.coords for p in complex.points}
    nx.draw(
        G=complex.graph,
        ax=ax,
        pos=pos,
        with_labels=kwargs['with_labels'],
        font_size=kwargs['font_size'],
        node_color=kwargs['node_background_color'],
        node_size=kwargs['node_size'],
        edge_color=kwargs['node_border_color'],
        edgecolors=kwargs['edge_color']
    )

    return ax


def plot_graph(
        complex,
        fig_width=5,
        fig_height=5,
        fig_dpi=150,
        with_labels=True,
        font_size=8,
        node_size=300,
        node_background_color='#fff',
        node_border_color='#000',
        edge_color='#000',
        draw_ball=False,
        ball_alpha=1/10,
        ball_color=None,
        save=False,
        file_name='plot'):

    """

    Plot the graph underlying the Vietoris-Rips complex object.

    Parameters
    ----------
    complex: tda.VietorisRipsComplex
        A Vietoris-Rips complex object.
    fig_width: float, optional
        Width of figure in inches.
    fig_height: float, optional
        Height of figure in inches.
    fig_dpi: float, optional
        DPI of the plot.
    with_labels: bool, optional
        Should labels be drawn for each node?
    font_size: int, optional
        Font size.
    node_size: int, optional
        Size of node.
    node_background_color: string, optional
        Color of node background.
    node_border_color: string, optional
        Color of node border.
    edge_color: string, optional
        Color of edges.
    draw_ball: bool, optional
        Should balls be drawn around nodes?
    ball_alpha: float, optional
        Opacity of ball surrounding a vertex.
    ball_color: string, optional
        Color of ball surrounding a vertex.
        If None balls will be coloured randomly.
    save: bool, optional
        Should the plot be saved to png.
    file_name: string, optional
        Name of file to save plot.
    """

    ax = draw_graph(
        complex=complex,
        fig_width=fig_width,
        fig_height=fig_height,
        fig_dpi=fig_dpi,
        with_labels=with_labels,
        font_size=font_size,
        node_size=node_size,
        node_background_color=node_background_color,
        node_border_color=node_border_color,
        edge_color=edge_color
    )

    if draw_ball:
        for point in complex.points:
            if ball_color is None:
                color = [random.random() for _ in range(3)]
            else:
                color = ball_color
            circle = Circle(
                point.coords,
                radius=complex.epsilon,
                alpha=ball_alpha,
                edgecolor=None,
                facecolor=color,
                zorder=-1
            )
            ax.add_artist(circle)

    plt.tight_layout()

    if save:
        plt.savefig(f'{file_name}.png')

    plt.show()


def plot_faces(
        complex,
        face_dimension,
        fig_width=5,
        fig_height=5,
        fig_dpi=150,
        with_labels=True,
        font_size=8,
        node_size=300,
        node_background_color='#fff',
        node_border_color='#000',
        edge_color='#000',
        face_color=None,
        face_alpha=1/10,
        save=False,
        file_name='plot'):
    """

    Plot a graph with colored faces.

    Parameters
    ----------
    complex: tda.VietorisRipsComplex
        A Vietoris-Rips complex object.
    fig_width: float, optional
        Width of figure in inches.
    fig_height: float, optional
        Height of figure in inches.
    fig_dpi: float, optional
        DPI of the plot.
    with_labels: bool, optional
        Should labels be drawn for each node?
    font_size: int, optional
        Font size.
    node_size: int, optional
        Size of node.
    node_background_color: string, optional
        Color of node background.
    node_border_color: string, optional
        Color of node border.
    edge_color: string, optional
        Color of edges.
    draw_ball: bool, optional
        Should balls be drawn around nodes?
    face_alpha: float, optional
        Opacity of face.
    face_color: string, optional
        Color of face.
        If None balls will be coloured randomly.
    save: bool, optional
        Should the plot be saved to png.
    file_name: string, optional
        Name of file to save plot.

    """

    ax = draw_graph(
        complex=complex,
        fig_width=fig_width,
        fig_height=fig_height,
        fig_dpi=fig_dpi,
        with_labels=with_labels,
        font_size=font_size,
        node_size=node_size,
        node_background_color=node_background_color,
        node_border_color=node_border_color,
        edge_color=edge_color
    )

    if complex.simplices is None:
        complex.find_simplices()

    for face in complex.find_faces_with_dim(face_dimension):
        coords = list()
        for f in face:
            coords.append(f.coords)
        coords = np.vstack(coords)

        hull = ConvexHull(coords)
        if face_color is None:
            color = [random.random() for _ in range(3)]
        else:
            color = face_color

        polygon = Polygon(
            hull.points[hull.vertices],
            alpha=face_alpha,
            zorder=-1,
            color=color
        )
        ax.add_artist(polygon)

    plt.tight_layout()

    if save:
        plt.savefig(f'{file_name}.png')

    plt.show()


def plot_simplices(
        complex,
        fig_width=5,
        fig_height=5,
        fig_dpi=150,
        with_labels=True,
        font_size=8,
        node_size=300,
        node_background_color='#fff',
        node_border_color='#000',
        edge_color='#000',
        simplex_color=None,
        simplex_alpha=1/10,
        save=False,
        file_name='plot'):
    """

    Plot a graph with colored simplices.

    Parameters
    ----------
    complex: tda.VietorisRipsComplex
        A Vietoris-Rips complex object.
    fig_width: float, optional
        Width of figure in inches.
    fig_height: float, optional
        Height of figure in inches.
    fig_dpi: float, optional
        DPI of the plot.
    with_labels: bool, optional
        Should labels be drawn for each node?
    font_size: int, optional
        Font size.
    node_size: int, optional
        Size of node.
    node_background_color: string, optional
        Color of node background.
    node_border_color: string, optional
        Color of node border.
    edge_color: string, optional
        Color of edges.
    draw_ball: bool, optional
        Should balls be drawn around nodes?
    simplex_alpha: float, optional
        Opacity of simplex.
    simplex_color: string, optional
        Color of simplex.
        If None balls will be coloured randomly.
    save: bool, optional
        Should the plot be saved to png.
    file_name: string, optional
        Name of file to save plot.
    """

    ax = draw_graph(
        complex=complex,
        fig_width=fig_width,
        fig_height=fig_height,
        fig_dpi=fig_dpi,
        with_labels=with_labels,
        font_size=font_size,
        node_size=node_size,
        node_background_color=node_background_color,
        node_border_color=node_border_color,
        edge_color=edge_color
    )

    for face in complex.find_simplices():
        points = list()
        for p in face:
            points.append(p)
        coords = list(map(lambda x: x.coords, points))
        coords = np.vstack(coords)
        if coords.shape[0] < 3:
            continue

        hull = ConvexHull(coords)
        if simplex_color is None:
            color = [random.random() for _ in range(3)]
        else:
            color = simplex_color
        polygon = Polygon(
            hull.points[hull.vertices],
            alpha=simplex_alpha,
            color=color,
            zorder=-1
        )
        ax.add_artist(polygon)

    plt.tight_layout()

    if save:
        plt.savefig(f'{file_name}.png')

    plt.show()
