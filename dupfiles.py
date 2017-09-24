import os
import sys
import hashlib
 
def hashf(path, blocksize = 8192):
    with open(path, 'rb') as x:
        hasher = hashlib.md5()
        tmp = x.read(blocksize)
        while tmp:
            hasher.update(tmp)
            tmp = x.read(blocksize)
    return hasher.hexdigest()


def dfind(parent):
    fdups = {}
    for folders, _, files in os.walk(parent):
        for fname in files:
            if fname[0] != '.' and fname[0] != '~' and not(os.path.islink(fname)):
                path = os.path.join(folders, fname)
                fhash = hashf(path)
                if fhash in fdups:
                    fdups[fhash].append(path)
                else:
                    fdups[fhash] = [path]
    return fdups

 
def printfiles(dicts):
    alls = list(filter(lambda x: len(x) > 1, dicts.values()))
    for files in alls:
        print(':'.join(files))
 
 
if __name__ == '__main__':
    folders = sys.argv[1] 
    printfiles(dfind(folders))
   















        
