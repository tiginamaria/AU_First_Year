import sys
import hashlib
import os
from collections import defaultdict


def file_hash(path, mod=8192):
    with open(path, 'rb') as x:
        hasher = hashlib.md5()
        tmp = x.read(mod)
        while tmp:
            hasher.update(tmp)
            tmp = x.read(mod)
        return hasher.hexdigest()


def dup_find(parent):
    file_dups = defaultdict(list)
    for root, _, files in os.walk(parent):
        for f_name in files:
            if not (f_name.startswith(('.', '~')) and os.path.islink(f_name)):
                    path = os.path.join(os.path.realpath(root), f_name)
                    hashf = file_hash(path)
                    if hashf in file_dups:
                        file_dups[hashf].append(path)
                    else:
                        file_dups[hashf] = [path]
    return file_dups


def file_print(file_dups):
    for files in file_dups.values():
        if len(files) > 1:
            print(':'.join(files))


def main():
    folders = sys.argv[1]
    file_print(dup_find(folders))


if __name__ == '__main__':
    main()
