import os
from pathlib import Path

from lithops.multiprocessing import Pool
from lithops.storage.cloud_proxy import open

from isogenygraph.isogenies import neighbors, elliptic_curve, supersingular_count
from isogenygraph.utils import get_field, primes_batch


def bfs(F, p):
    first_node = elliptic_curve(F).j_invariant()
    size = supersingular_count(p)

    queue = {first_node}
    visited = set()

    ell = 2 

    while queue and not len(queue) + len(visited) == size:
        node = queue.pop()
        visited.add(node)

        for neighbor, _ in neighbors(ell, node):
            if neighbor not in queue and neighbor not in visited:
                queue.add(neighbor)

    nodes = list(visited.union(queue))
    assert len(nodes) == size
    nodes.sort()

    s = '\n'.join(map(str, nodes))
    with open(f'graphs/{p}/{p}_nodes.txt', 'w') as f:
        f.write(s)


def main():
    initargs = {
        'runtime_memory': 512,
        'runtime': 'gfinol/sagemath-lithops:2.0'
    }
    with Pool(initargs=initargs) as pool:

        for batch in primes_batch(13, 30000, 500):
            print(f'Starting range {batch[0]} - {batch[-1]}')

            iterdata = []
            for p in batch:
                Path(f'graphs/{p}').mkdir(parents=True, exist_ok=True)
                if not os.path.isfile(f'graphs/{p}/{p}_nodes.txt') or True:
                    F = get_field(p)
                    iterdata.append((F, p))

            if iterdata:
                print('Running multiple bfs...')
                pool.map(bfs, iterdata)


if __name__ == "__main__":
    main()