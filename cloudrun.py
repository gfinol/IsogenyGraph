import os
from bisect import bisect_left
from collections import defaultdict
from functools import partial

from lithops.multiprocessing import Pool
from lithops.storage.cloud_proxy import open
from sage.all_cmdline import primes
from scipy.sparse import coo_matrix, save_npz

from isogenygraph.isogenies import neighbors, supersingular_count
from isogenygraph.utils import get_field, primes_batch


def search(alist, item):
    'Locate the leftmost value exactly equal to item'
    i = bisect_left(alist, item)
    if i != len(alist) and alist[i] == item:
        return i
    raise ValueError


def reduce_isogeny_graph(work, nodes, F):
    rows = []
    cols = []
    data = []
    index = partial(search, nodes)
    
    for node_index, (node, neighbors) in enumerate(work):
        for neighbor, multiplicity in neighbors:
            neighbor = F(neighbor)
            rows += [node_index]
            cols += [index(neighbor)]
            data += [multiplicity]

    N = len(nodes)
    adjacency_matrix = coo_matrix((data, (rows, cols)), shape=(N, N)).asfptype().tocsr()
    return adjacency_matrix


def parse_nodes(p, F):
    nodes = []
    with open(f"graphs/{p}/{p}_nodes.txt", 'r') as f:
        for line in f:
            nodes.append(F(line))
    return nodes


def neighbors_str(ell, node):
    return [(str(n), m) for n,m in neighbors(ell, node)]


def mapping(p, ell, F, batch):
    start, end = batch
    data = open(f'./graphs/{p}/{p}_nodes.txt').read().splitlines()[start: end]
    nodes = [F(line) for line in data]
    work = [(str(node), neighbors_str(ell, node)) for node in nodes]

    return work, p, ell
    

def reduce2dict(res):
    work_dict = defaultdict(list)

    for work, p, ell in res:
        work_dict[(p, ell)] += work        

    return work_dict


def create_save_matrix(work_dict):
    for key, work in work_dict.items():
        p, ell = key
        F = get_field(p)
        nodes = parse_nodes(p, F)
        assert len(work) == supersingular_count(p)
        matrix = reduce_isogeny_graph(work, nodes, F)
        save_npz(f"graphs/{p}/{p}_{ell}.npz", matrix, compressed=True)


def main():
    initargs= {
        'runtime_memory': 1024,
        'runtime': 'gfinol/sagemath-lithops:2.0'
    }
    with Pool(initargs=initargs) as pool:
        for p_primes in primes_batch(13, 30000, 100):
            print(f'Starting range {p_primes[0]} - {p_primes[-1]}')
            iterdata = []
            for p in p_primes:
                F = get_field(p)

                # if we have too many nodes, we compute them by groups aka batches
                count_p = supersingular_count(p)
                n_lines_batch = 500
                rang = list(range(0, count_p, n_lines_batch)) + [count_p]
                batches = list(zip(rang[:-1], rang[1:]))

                for ell in primes(2, 12):
                    if not os.path.isfile(f"graphs/{p}/{p}_{ell}.npz"):
                        for batch in batches:
                            iterdata.append((p, ell, F, batch))

            if iterdata:
                print('Runing on cloud')
                res = pool.starmap(mapping, iterdata)

                print('Reducing')
                work_dict = reduce2dict(res)

                print('Saving data.')
                create_save_matrix(work_dict)


if __name__ == "__main__":
    main()
