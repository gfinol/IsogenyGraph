from sage.all_cmdline import primes
from tqdm import tqdm
from multiprocessing import Pool

from isogenygraph.check import check_nodes

print("Checking nodes...")

with Pool() as pool:
    primes = list(primes(13, 30000))
    work = pool.imap(check_nodes, primes)

    for p, w in tqdm(zip(primes, work)):
        if not w:
            print(p)
