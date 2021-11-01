import gc
import os
import random
import sys
import time
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sys.path.append(os.path.join(os.getcwd(), '.'))

from tda.vr_complex import VietorisRipsComplex  # noqa: E402


def measure(f):
    def wrapper(*args, **kwargs):
        start = time.time()
        f(*args, **kwargs)
        stop = time.time()
        return stop - start
    return wrapper


def make_points(n, d=2):
    names, coords = list(), list()
    for i in range(n):
        names.append(str(i))
        coords.append([random.random() for _ in range(d)])
    return names, coords


@measure
def create_graph(vrc):
    vrc.create_graph()


@measure
def find_simplices(vrc):
    vrc.find_simplices()


@measure
def find_faces(vrc):
    vrc.find_faces()


@measure
def find_faces_with_dim(vrc, dim):
    vrc.find_faces_with_dim(dim)


@measure
def boundary_operator_matrix(vcr, dim):
    vcr.boundary_operator_matrix(dim)


@measure
def check_nesting(vrc, higher, lower):
    vrc.check_nesting(higher, lower)


def benchmark_create_graph(points):
    times = list()
    for n in points:
        names, coords = make_points(n)
        vrc = VietorisRipsComplex.from_list(
            names=names,
            coords=coords,
            epsilon=float('inf')
        )
        times.append(create_graph(vrc))
    return points, times


def benchmark_find_simplices(points):
    times = list()
    for n in points:
        names, coords = make_points(n)
        vrc = VietorisRipsComplex.from_list(
            names=names,
            coords=coords,
            epsilon=float('inf')
        )
        vrc.create_graph()
        times.append(find_simplices(vrc))
    return points, times


def benchmark_find_faces(points):
    times = list()
    for n in points:
        names, coords = make_points(n)
        vrc = VietorisRipsComplex.from_list(
            names=names,
            coords=coords,
            epsilon=float('inf')
        )
        vrc.create_graph()
        vrc.find_simplices()
        times.append(find_faces(vrc))
    return points, times


def benchmark_find_faces_with_dim(points):
    times = list()
    for n in points:
        names, coords = make_points(n)
        vrc = VietorisRipsComplex.from_list(
            names=names,
            coords=coords,
            epsilon=float('inf')
        )
        vrc.create_graph()
        vrc.find_simplices()
        times.append(find_faces_with_dim(vrc, 2))
    return points, times


def benchmark_check_nesting(points):
    times = list()
    for n in points:
        names, coords = make_points(n)
        vrc = VietorisRipsComplex.from_list(
            names=names,
            coords=coords,
            epsilon=float('inf')
        )
        vrc.create_graph()
        vrc.find_simplices()
        higher = vrc.find_faces_with_dim(1)
        lower = vrc.find_faces_with_dim(0)
        times.append(check_nesting(vrc, higher, lower))
    return points, times


def benchmark_boundary(points):
    times = list()
    for n in points:
        names, coords = make_points(n)
        vrc = VietorisRipsComplex.from_list(
            names=names,
            coords=coords,
            epsilon=float('inf')
        )
        vrc.create_graph()
        vrc.find_simplices()
        times.append(find_faces_with_dim(vrc, 2))
    return points, times


def plot(points, times_mean, time_stds, func, path):
    title = func.__name__
    title = title.replace('benchmark_', '').replace('_', ' ').capitalize()

    plt.figure(figsize=(5, 4))
    plt.style.use('ggplot')
    plt.plot(points, times_mean)
    plt.fill_between(
        x=points,
        y1=times_mean + time_stds,
        y2=times_mean - time_stds,
        alpha=1/3
    )
    plt.xticks(points)
    plt.xlabel('# Points')
    plt.ylabel('Time (s)')
    plt.title(title)
    plt.tight_layout()
    plt.savefig(f'{path}/{func.__name__}.png')


def print_results(points, time_mean, time_std, func, path):

    path = f'{path}/{func.__name__}.txt'

    df = pd.DataFrame(
        data=np.transpose(np.vstack([points, time_mean, time_std])),
        columns=['n points', 'time mean', 'time std']
    )

    header = f'Execution time for {func.__name__}'
    sep = '-' * len(header)

    print(sep)
    print(header)
    print(sep)
    print(df)

    df.to_csv(path)


def main():

    gc.disable()
    random.seed(123)

    fmt = "%d-%m-%Y %H:%M:%S"
    benchmark_ts = datetime.now().strftime(fmt)
    path = f'{os.getcwd()}/performance/results/{benchmark_ts}'
    Path(path).mkdir(parents=True, exist_ok=True)

    functions = [
        benchmark_create_graph,
        benchmark_find_simplices,
        # benchmark_find_faces,
        benchmark_find_faces_with_dim,
        benchmark_check_nesting,
        benchmark_boundary
    ]

    reps = 30
    points = list(range(1, 105, 5))
    for func in functions:
        times = list()
        for r in range(reps):
            points, run_time = func(points)
            times.append(run_time)
        times = np.vstack(times)
        times_means = np.mean(times, axis=0)
        times_stds = np.std(times, axis=0)

        plot(points, times_means, times_stds, func, path)
        print_results(points, times_means, times_stds, func, path)


if __name__ == '__main__':
    main()
