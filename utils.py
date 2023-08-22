import hashlib
import string
import random


# unique hash to check if two files are equal
def hashfile(file):
    buf_size = 65536
    sha256 = hashlib.sha256()

    with open(file, 'rb') as f:
        while True:
            data = f.read(buf_size)
            if not data:
                break
            sha256.update(data)

    return sha256.hexdigest()


# used for renaming files that don't have the same content but match the name of a file from source folder
def get_random_name():
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for _ in range(10))
    return result_str
