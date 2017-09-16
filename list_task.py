# Remove equal adjacent elements
#
# Example input: [1, 2, 2, 3]
# Example output: [1, 2, 3]

# a = [int(s) for s in input().split()]
def remove_adjacent(a):
    b = []
    for i in a:
        if i!=b[-1] or len(b)==0 :
            b.append(i)
    return b
# b=remove_adjacent(a)
# print(' '.join([str(i) for i in b]))

# Merge two sorted lists in one sorted list in linear time
#
# Example input: [2, 4, 6], [1, 3, 5]
# Example output: [1, 2, 3, 4, 5, 6]
# x = [int(s) for s in input().split()]
# y = [int(s) for s in input().split()]
def linear_merge(a,b):
    i=0
    j=0
    c=[]
    while (i < len(a)) or (j < len(b)):
        if j>=len(b):
            c.append(a[i])
            i+=1
        elif i>= len(a):
            c.append(b[j])
            j+=1
        elif a[i]<b[j]:
            c.append(a[i])
            i+=1
        else:
            c.append(b[j])
            j+=1
    return c
# c=linear_merge(x,y)
# print(' '.join([str(i) for i in c]))
