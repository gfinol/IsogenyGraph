from bisect import bisect_left

import networkx as nx
import numpy as np
from numpy import real as npreal
from sage.all_cmdline import Graph
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import eigs


def spine_size(nodes):
    spine = 0

    F2 = nodes[0].base_ring()
    F = F2.subfield(1)
    for node in nodes:
        if node in F:
            spine += 1
        else:
            break

    return spine


def compute_diameter(matrix):
    nxg = nx.from_scipy_sparse_matrix(matrix, parallel_edges=True)
    g = Graph(nxg, loops=True)
    diameter = g.diameter()
    return diameter


def compute_eigenvalues(matrix):
    a, _ = eigs(matrix, k=2, which="LR", return_eigenvectors=False)
    (b,) = eigs(matrix, k=1, which="SR", return_eigenvectors=False)
    return npreal(a), npreal(b)


def frobenius_matrix(nodes):
    F2 = nodes[0].base_ring()
    F = F2.subfield(1)
    p = F.characteristic()

    rows = []
    cols = []

    for j in nodes:
        if j in F:
            continue
        rows += [bisect_left(nodes, j)]
        cols += [bisect_left(nodes, j ** p)]

    N = len(nodes)
    frob = coo_matrix((np.ones(len(rows)), (rows, cols)), shape=(N, N)).asfptype().tocsr()
    return frob
