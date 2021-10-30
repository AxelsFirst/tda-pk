import random

import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.patches import Circle


def plot_graph(
        complex,
        fig_width=5,
        fig_height=5,
        fig_dpi=150,
        with_labels=True,
        font_size=8,
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

    pos = {p: p.coords for p in complex.points}

    # Plot settings
    fig, ax = plt.subplots()
    fig.set_figheight(fig_width)
    fig.set_figwidth(fig_height)
    fig.set_dpi(fig_dpi)
    ax.axis('equal')

    # Draw graph
    nx.draw(
        G=complex.graph,
        pos=pos,
        ax=ax,
        with_labels=with_labels,
        font_size=font_size,
        node_color=node_background_color,
        edge_color=node_border_color,
        edgecolors=edge_color
    )

    # Draw balls
    if draw_ball:
        for coords in pos.values():
            if ball_color is None:
                color = [random.random() for _ in range(3)]
            circle = Circle(
                coords,
                radius=complex.epsilon,
                alpha=ball_alpha,
                edgecolor=None,
                facecolor=color,
                zorder=-1
            )
            ax.add_artist(circle)

    plt.tight_layout()

    # Save
    if save:
        plt.savefig(f'{file_name}.png')

    plt.show()


def plot_faces(complex):
    """

    Plot a graph with colored faces.

    Parameters
    ----------
    complex: tda.VietorisRipsComplex
        A Vietoris-Rips complex object.

    """

    raise NotImplementedError()


def plot_simplices(complex):
    """

    Plot a graph with colored simplices.

    Parameters
    ----------
    complex: tda.VietorisRipsComplex
        A Vietoris-Rips complex object.

    """

    raise NotImplementedError()
