from builtins import open as local_open

from lithops.config import default_config
from lithops.storage import Storage
from sage.all_cmdline import primes
from tqdm import tqdm


class Data2Cloud(object):
	"""docstring for Data2Cloud"""
	def __init__(self, bucket=None, config=None):
		config = config or default_config()
		self.storage = Storage(config)
		self.bucket = bucket or config['lithops']['storage_bucket']

	def __put_object(self, key, data):
		return self.storage.put_object(self.bucket, key, data)

	def __get_object(self, key, stream=False):
		return self.storage.get_object(self.bucket, key, stream)

	def push_nodes(self, p):
		with local_open(f'graphs/{p}/{p}_nodes.txt', 'rb') as f:
			nodes = f.read()
		self.__put_object(f'./graphs/{p}/{p}_nodes.txt', nodes)

	def push_metadata(self, p):
		with local_open(f'graphs/{p}/{p}_metadata.json', 'rb') as f:
			metadata = f.read()
		self.__put_object(f'./graphs/{p}/{p}_metadata.json', metadata)

	def push_matrix(self, p, ell):
		with local_open(f'graphs/{p}/{p}_{ell}.npz', 'rb') as f:
			matrix = f.read()
		self.__put_object(f'./graphs/{p}/{p}_{ell}.npz', matrix)

	def push_all_matrix(self, p):
		for ell in primes(2, 13):
			self.push_matrix(p, ell)

	def pull_nodes(self, p):
		nodes = self.__get_object(f'./graphs/{p}/{p}_nodes.txt')
		with local_open(f'graphs/{p}/{p}_nodes.txt', 'wb') as f:
			f.write(nodes)

	def pull_metadata(self, p):
		metadata = self.__get_object(f'./graphs/{p}/{p}_metadata.json')
		with local_open(f'graphs/{p}/{p}_metadata.json', 'wb') as f:
			f.write(metadata)

	def pull_matrix(self, p, ell):
		matrix = self.__get_object(f'./graphs/{p}/{p}_{ell}.npz')
		with local_open(f'graphs/{p}/{p}_{ell}.npz', 'wb') as f:
			f.write(matrix)

	def pull_all_matrix(self, p):
		for ell in primes(2, 13):
			self.pull_matrix(p, ell)

	def pull_all(self, p):
		self.pull_nodes(p)
		self.pull_metadata(p)
		self.pull_all_matrix(p)

	def push_all(self, p):
		self.push_nodes(p)
		self.push_metadata(p)
		self.push_all_matrix(p)


def main():
	dc = Data2Cloud()
	primes_list = list(primes(13, 30000))
	for p in tqdm(primes_list):
		dc.push_all(p)


if __name__ == '__main__':
	main()
