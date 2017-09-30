import numpy as np
from math import log, ceil


def mread(n):
    m = []
    for i in range(n):
        row = input().split()
        m.append(row)
    return m


def mprint(m):
    n = m.shape[0]
    for i in range(n):
        print(' '.join([str(m[i][j]) for j in range(n)]))


def msplit(m):
    m1, m2 = np.vsplit(m, 2)
    m11, m12 = np.hsplit(m1, 2)
    m21, m22 = np.hsplit(m2, 2)
    return m11, m12, m21, m22


def strassen(a, b):
    n = a.shape[0]
    if n == 1:
        return a * b
    else:
        a11, a12, a21, a22 = msplit(a)
        b11, b12, b21, b22 = msplit(b)
        p1 = strassen(a11 + a22, b11 + b22)
        p2 = strassen(a21 + a22, b11)
        p3 = strassen(a11, b12 - b22)
        p4 = strassen(a22, b21 - b11)
        p5 = strassen(a11 + a12, b22)
        p6 = strassen(a21 - a11, b11 + b12)
        p7 = strassen(a12 - a22, b21 + b22)
        c11 = p1 + p4 - p5 + p7
        c12 = p3 + p5
        c21 = p2 + p4
        c22 = p1 - p2 + p3 + p6
        c01 = np.vstack((c11, c21))
        c02 = np.vstack((c12, c22))
        c = np.hstack((c01, c02))
        return c


if __name__ == '__main__':
    n = int(input())
    size = 2 ** int(ceil(log(n, 2)))
    x = np.zeros((size, size), dtype=np.int)
    y = np.zeros_like(x)
    x[:n, :n] = np.array(mread(n))
    y[:n, :n] = np.array(mread(n))
    c = strassen(x, y)[:n, :n]
    mprint(c)
