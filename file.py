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


def find_duplicates(parent):
    file_to_hash = defaultdict(list)
    for root, _, files in os.walk(parent):
        for f_name in files:
            path = os.path.join(root, f_name)
            if not f_name.startswith(('.', '~')) and not os.path.islink(path):
                hashf = file_to_hash(path)
                file_to_hash[hashf].append(os.path.relpath(path, start=parent))
    return file_to_hash


def print_files(file_to_hash):
    for files in file_to_hash.values():
        if len(files) > 1:
            print(':'.join(files))


def main():
    folders = sys.argv[1]
    print_files(find_duplicates(folders))


if __name__ == '__main__':
    main()
