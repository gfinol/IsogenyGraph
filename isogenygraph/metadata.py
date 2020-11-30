import json
from os.path import isfile

from sage.all_cmdline import GF

from .isogenies import supersingular_count


class Metadata(object):
    def __init__(self, path, p=None, open=open, isfile=isfile):
        self.__path = path
        self.__field = None
        self.__open = open
        self.__isfile = isfile

        if self.__isfile(path):
            with self.__open(path) as f:
                self.__metadata = json.load(f)
        else:
            self.__metadata = dict()
            self.__metadata["prime"] = int(p)
            self.__metadata["nodes"] = int(supersingular_count(p))
            self.get_field()
            self.save()

    def get_field(self):
        if self.__field is None:
            p = self.__metadata["prime"]

            if 'minpoly' in self.__metadata:
                minpoly = self.__metadata["minpoly"]

                F = GF(p)
                R = F['x']
                F2 = F.extension(R(minpoly), names=('z',))

            else:
                F = GF(p)
                F2 = F.extension(2, names=('z',))
                (z,) = F2._first_ngens(1)
                self.__metadata["minpoly"] = str(z.minimal_polynomial())

            self.__field = F2

        return self.__field

    def __ensure_ell(self, ell):
        if "ell" not in self.__metadata:
            self.__metadata["ell"] = dict()

        if str(ell) not in self.__metadata["ell"]:
            self.__metadata["ell"][str(ell)] = dict()

    def set_undirected(self, undirected):
        self.__metadata["undirected"] = bool(undirected)

    def set_spine(self, spine):
        self.__metadata["spine"] = int(spine)

    def set_diameter(self, ell, diameter):
        self.__ensure_ell(ell)
        self.__metadata["ell"][str(ell)]["diameter"] = int(diameter)

    def set_eigenvalues(self, ell, eigenvalues):
        self.__ensure_ell(ell)
        self.__metadata["ell"][str(ell)]["eigenvalues"] = eigenvalues

    def set_conjugate_isogenous_pairs(self, ell, conjugate_isogenous_pairs):
        self.__ensure_ell(ell)
        self.__metadata["ell"][str(ell)]["conjugate_isogenous_pairs"] = int(conjugate_isogenous_pairs)

    def save(self):
        with self.__open(self.__path, 'w') as f:
            json.dump(self.__metadata, f)

    def get_json(self):
        return json.dumps(self.__metadata)
