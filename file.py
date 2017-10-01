import sys
import hashlib
import os
from collections import defaultdict


def hash_file(path):
    block_size = 2**10
    with open(path, 'rb') as f:
        hasher = hashlib.md5()
        tmp = f.read(block_size)
        while tmp:
            hasher.update(tmp)
            tmp = f.read(block_size)
        return hasher.hexdigest()


def find_duplicates(parent):
    key_to_value = defaultdict(list)
    for root, _, files in os.walk(parent):
        for f_name in files:
            path = os.path.join(root, f_name)
            if not f_name.startswith(('.', '~')) and not os.path.islink(path):
                hashf = hash_file(path)
                key_to_value[hashf].append(os.path.relpath(path, start=parent))
    return key_to_value


def print_files(key_to_value):
    for files in key_to_value.values():
        if len(files) > 1:
            print(':'.join(files))


def main():
    folders = sys.argv[1]
    print_files(find_duplicates(folders))


if __name__ == '__main__':
    main()
