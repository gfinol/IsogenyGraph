from lithops.multiprocessing import Pool
from lithops.storage.cloud_proxy import open
from numpy import count_nonzero
from sage.all_cmdline import primes
from scipy.sparse import load_npz

from isogenygraph.compute_metrics import spine_size, compute_diameter, compute_eigenvalues, \
    frobenius_matrix
from isogenygraph.utils import get_metadata, primes_batch


def compute_metrics_f(p, metadata):
    F = metadata.get_field()
    with open(f'./graphs/{p}/{p}_nodes.txt') as f:
        data = f.read().splitlines()
    nodes = [F(line) for line in data]

    undirected = (p % 12 == 1)
    metadata.set_spine(spine_size(nodes))
    metadata.set_undirected(bool(undirected))

    frob = frobenius_matrix(nodes)

    for ell in primes(2, 12):
        with open(f'./graphs/{p}/{p}_{ell}.npz', 'rb') as f:
            matrix = load_npz(f)

        metadata.set_diameter(ell, compute_diameter(matrix))
        c_ell = count_nonzero((frob * matrix).diagonal()) / 2
        metadata.set_conjugate_isogenous_pairs(ell, c_ell)

        if matrix.shape[0] > 3:
            metadata.set_eigenvalues(ell, compute_eigenvalues(matrix))

    with open(f'./graphs/{p}/{p}_metadata.json', 'w') as f:
        f.write(metadata.get_json())


def main():

    step = 50  # change me
    start, end = 13, 30000  # change me

    initargs = {
        'runtime_memory': 256,
        'runtime': 'gfinol/sagemath-lithops:2.0'
    }

    with Pool(initargs=initargs) as pool:
        for batch in primes_batch(start, end, step):
            print(f'Starting range {batch[0]} - {batch[-1]}')

            iterdata = []
            for p in batch:
                metadata = get_metadata(p)
                iterdata.append((p, metadata))

            if iterdata:
                pool.starmap(compute_metrics_f, iterdata)


if __name__ == '__main__':
    main()
