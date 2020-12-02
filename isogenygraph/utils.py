from sage.all_cmdline import primes
from isogenygraph.metadata import Metadata

from os.path import isfile


def primes_batch(start, end, size):
    data = list(primes(start, end))
    chunks = [data[x:x + size] for x in range(0, len(data), size)]
    return chunks


def get_metadata(p, open=open, isfile= isfile):
    path = f"graphs/{p}/{p}_metadata.json"

    return Metadata(path, p, open, isfile)


def get_field(p, open=open, isfile=isfile):
    metadata = get_metadata(p, open, isfile)

    return metadata.get_field()
