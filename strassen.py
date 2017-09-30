import numpy as np


def matrix_read(n):
    return [list(map(int, input().split())) for _ in range(n)]


def matrix_print(m):
    for row in m:
        print(*row)


def matrix_split(m):
    m1, m2 = np.vsplit(m, 2)
    m11, m12 = np.hsplit(m1, 2)
    m21, m22 = np.hsplit(m2, 2)
    return m11, m12, m21, m22


def strassen(a, b):
    n = a.shape[0]
    if n == 1:
        return a * b
    else:
        a11, a12, a21, a22 = matrix_split(a)
        b11, b12, b21, b22 = matrix_split(b)
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
        return np.vstack((
            np.hstack((c11, c12)),
            np.hstack((c21, c22))
        ))


def main():
    n = int(input())
    size = 1
    while (size < n):
        size *= 2
    x = np.zeros((size, size), dtype=np.int)
    y = np.zeros_like(x)
    x[:n, :n] = matrix_read(n)
    y[:n, :n] = matrix_read(n)
    c = strassen(x, y)[:n, :n]
    matrix_print(c)


if __name__ == '__main__':
    main()
