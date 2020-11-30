from sage.all_cmdline import primes
import os
from tqdm import tqdm

from isogenygraph.check import check_mat


print("Checking matrices...")

ps = list(primes(13, 30000))
progress = tqdm(ps)
for p in progress:
	for ell in primes(2, 12):
		file_path = f"graphs/{p}/{p}_{ell}.npz"
		
		if os.path.isfile(file_path):
			ok, error = check_mat(file_path, p, ell)
			if not ok:
				progress.write(error)
		else:
			progress.write(f'File not found: {file_path}')