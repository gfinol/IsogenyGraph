import numpy as np
from sage.all_cmdline import EllipticCurve
from scipy.sparse import load_npz
from random import choices

from .isogenies import supersingular_count
from .metadata import Metadata


def check_mat(file, p, ell):
    message = ''
    m = load_npz(file)

    # Check matrices are square and the right size
    size = supersingular_count(p)
    ok_size = (size == m.shape[0] == m.shape[1])

    if not ok_size:
        message += str((
            p, ell,
            size, m.shape,
        ))

    # Check all nodes have out-degree ell+1
    rowsums = m.sum(axis=1)
    ok_rowsums = np.all(rowsums == (ell + 1))

    if not ok_rowsums:
        message += f"ROWSUMS: ({p}, {ell}, {np.sum(~(rowsums == (ell + 1)))})"

    return ok_size and ok_rowsums, message


def check_nodes(p):
    file = f"graphs/{p}/{p}_nodes.txt"
    metadata = Metadata(f"graphs/{p}/{p}_metadata.json")

    F = metadata.get_field()
    with open(file, 'r') as f:
        nodes = f.readlines()

    nodes = [F(n) for n in nodes]
    ok = all((EllipticCurve(F, j=j).is_supersingular() for j in choices(nodes, k=10)))

    nodes = set(nodes)
    if len(nodes) != supersingular_count(p):
        ok = False

    return ok
