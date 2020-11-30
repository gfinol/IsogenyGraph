from sage.all_cmdline import EllipticCurve, is_prime, kronecker, QuadraticField
import sage.modular.ssmod.ssmod


def modpoly(ell, x, y):
    return sage.modular.ssmod.ssmod.Phi_polys(ell, x, y)


def supersingular_count(p):
    e = 0
    if p % 3 == 2:
        e += 1
    if p % 4 == 3:
        e += 1
    return int(p / 12) + e


def neighbors(ell, E):
    R = E.base_ring()['x']
    (x,) = R._first_ngens(1)
    return modpoly(ell, E, x).roots()


def elliptic_curve(F2):
    F = F2.subfield(1)
    R = F['s']
    (s,) = R._first_ngens(1)
    p = F2.characteristic()

    # Bröker's algorithm
    if p % 3 == 2:
        first_node = EllipticCurve(F2, [0, 1])
    elif p % 4 == 3:
        first_node = EllipticCurve(F2, [1, 0])
    else:
        q = 3
        while not (is_prime(q) and kronecker(-q, p) == -1):
            q += 4

        if q == 3:
            first_node = EllipticCurve(F2, [0, 1])
        else:
            K = QuadraticField(-q, names=('a',))
            (a,) = K._first_ngens(1)
            P_K = K.hilbert_class_polynomial()
            j = R(P_K).roots(multiplicities=False)[0]
            first_node = EllipticCurve(F2, j=j)

    return first_node
