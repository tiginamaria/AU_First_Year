import sys
import hashlib
import os
from collections import defaultdict


def file_hash(path):
    mod = 2**10
    with open(path, 'rb') as x:
        hasher = hashlib.md5()
        tmp = x.read(mod)
        while tmp:
            hasher.update(tmp)
            tmp = x.read(mod)
        return hasher.hexdigest()


def dup_find(parent):
    file_dup = defaultdict(list)
    for root, _, files in os.walk(parent):
        for f_name in files:
            path = os.path.join(root, f_name)
            if not (f_name.startswith(('.', '~')) and os.path.islink(path)):
                    hashf = file_hash(path)
                    file_dup[hashf].append(os.path.relpath(path, start=parent))
    return file_dup


def file_print(file_dup):
    for files in file_dup.values():
        if len(files) > 1:
            print(':'.join(files))


def main():
    folders = sys.argv[1]
    file_print(dup_find(folders))


if __name__ == '__main__':
    main()
