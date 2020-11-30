from sage.all_cmdline import primes
from isogenygraph.metadata import Metadata


def primes_batch(start, end, size):
    data = list(primes(start, end))
    chunks = [data[x:x + size] for x in range(0, len(data), size)]
    return chunks


def get_metadata(p):
    path = f"graphs/{p}/{p}_metadata.json"

    return Metadata(path, p)


def get_field(p):
    metadata = get_metadata(p)

    return metadata.get_field()
