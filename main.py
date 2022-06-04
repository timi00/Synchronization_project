import sys
import os.path
import logging
import hashlib
from pathlib import Path


def input_validation(arg1, arg2, arg3, arg4):
    if not os.path.isdir(arg1):
        pass
    elif not os.path.isdir(arg2):
        pass
    elif not arg3.isdigit():
        pass
    elif not os.path.exists(arg4):
        pass


def file_to_hash_sha256(filename):
    sha256_hash = hashlib.sha256()
    with open(filename, "rb") as f:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def files_to_dictionary(directory):
    file_dictionary = {}
    for path, currentDirectory, files in os.walk(directory):
        for file in files:
            file_hash = file_to_hash_sha256(os.path.join(path, file))
            file_dictionary[os.path.join(path, file)] = file_hash
    return file_dictionary


if __name__ == "__main__":
    input_validation(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    original_directory = sys.argv[1]
    clone_directory = sys.argv[2]
    sync_interval = int(sys.argv[3])
    log_file = sys.argv[4]

    Log_Format = "%(levelname)s %(asctime)s - %(message)s"

    logging.basicConfig(format=Log_Format,
                        level=logging.INFO,
                        handlers=[logging.FileHandler(log_file),
                                  logging.StreamHandler()])
    logger = logging.getLogger()
    # logger.info("Our third Log Message")
    # logger.error("Our error Log Message")

    origin_files = files_to_dictionary(original_directory)
    clone_files = files_to_dictionary(clone_directory)
    for key, value in origin_files.items():
        print(f"filename: {key}, hash: {value}")


