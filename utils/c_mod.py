import math


def c_mod(a, n):
    return a - (n * math.trunc(a/n))
