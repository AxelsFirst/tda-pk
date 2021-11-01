import os
import sys

sys.path.append(os.path.join(os.getcwd(), '.'))

from tda.vr_complex import VietorisRipsComplex  # noqa: E402
from tests.graphs import graphs  # noqa: E402
from tda.plots import plot_graph  # noqa: E402

for name, graph in graphs.items():
    vrc = VietorisRipsComplex.from_list(
        names=graph['names'],
        coords=graph['coords'],
        epsilon=graph['epsilon']
    )
    vrc.create_graph()
    plot_graph(complex=vrc, save=True, file_name=f'tests/images/{name}')
