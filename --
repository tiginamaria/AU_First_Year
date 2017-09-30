from math import log, ceil

def fill_0(n, k):
    m= [[0 for row in range(n)] for col in range(k)]
    return m

def split(m):  
    a = m
    b = m
    c = m
    d = m
    a = a[:len(a)//2]
    b = b[:len(b)//2]
    c = c[len(c)//2:]
    d = d[len(d)//2:]
    while(len(a[0]) > len(m[0])//2):
        for i in range(len(a[0])//2):
            a[i] = a[i][:len(a[i])//2]
            b[i] = b[i][len(b[i])//2:]
            c[i] = c[i][:len(c[i])//2]
            d[i] = d[i][len(d[i])//2:]
    return a,b,c,d

def part_ad(a, b):
    if type(a) == int:
        d = a + b
    else:
        d = []
        for i in range(len(a)):
            c = []
            for j in range(len(a[0])):
                c.append(a[i][j] + b[i][j])
            d.append(c)
    return d

def s_mat(a, b):
    if type(a) == int:
        d = a - b
    else:
        d = []
        for i in range(len(a)):
            c = []
            for j in range(len(a[0])):
                c.append(a[i][j] - b[i][j])
            d.append(c)
    return d


def strassen(a, b, v):
    if v == 1:
        d = [[0]]
        d[0][0] = a[0][0] * b[0][0]
        return d
    else:
        a11, a12, a21, a22 = split(a)
        b11, b12, b21, b22 = split(b)

        v = v // 2
        p1 = strassen(part_ad(a11,a22), part_ad(b11,b22), v)
        p2 = strassen(part_ad(a21,a22), b11, v)
        p3 = strassen(a11, s_mat(b12,b22), v)
        p4 = strassen(a22, s_mat(b21,b11), v)
        p5 = strassen(part_ad(a11,a12), b22, v)
        p6 = strassen(s_mat(a21,a11), part_ad(b11,b12), v)
        p7 = strassen(s_mat(a12,a22), part_ad(b21,b22), v)

        c11 = part_ad(s_mat(part_ad(p1, p4), p5), p7)
        c12 = part_ad(p3, p5)
        c21 = part_ad(p2, p4)
        c22 = part_ad(s_mat(part_ad(p1, p3), p2), p6)
        s = len(c11)
        c = fill_0(s*2,s*2)
        for i in range(s):
            for j in range(s):
                c[i][j] = c11[i][j]
                c[i][j + s] = c12[i][j]
                c[i + s][j] = c21[i][j]
                c[i + s][j + s] = c22[i][j]

        return c
        
def readm(n, m):  
    a = [[0 for i in range(m)] for j in range(m)]
    for i in range(n):
        row = input().split()
        for j in range(len(row)):
            a[i][j] += int(row[j])
    return a

def printm(m, n):
    for i in range(n):
        print(' '.join([str(m[i][j]) for j in range(n)]))

n = int(input())
n_sq = 2 ** int(ceil(log(n, 2)))
a = readm(n, n_sq)
b = readm(n, n_sq)

 
printm (strassen(a, b, n_sq), n)
