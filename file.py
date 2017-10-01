import sys
import hashlib
import os
from collections import defaultdict


def hash_file(path):
    block_size = 2 ** 10
    with open(path, 'rb') as f:
        hasher = hashlib.md5()
        tmp = f.read(block_size)
        while tmp:
            hasher.update(tmp)
            tmp = f.read(block_size)
        return hasher.hexdigest()


def find_duplicates(main):
    hash_to_files = defaultdict(list)
    for root, _, files in os.walk(main):
        for f_name in files:
            path = os.path.join(root, f_name)
            if not f_name.startswith(('.', '~')) and not os.path.islink(path):
                hashf = hash_file(path)
                hash_to_files[hashf].append(os.path.relpath(path, start=main))
    return hash_to_files


def print_files(hash_to_files):
    for files in hash_to_files.values():
        if len(files) > 1:
            print(':'.join(files))


def main():
    folders = sys.argv[1]
    print_files(find_duplicates(folders))


if __name__ == '__main__':
    main()
