import sys
import os.path
import logging
import hashlib
import argparse


class Repository():

    def copy_file(self):
        pass

    def remove_file(self):
        pass


def create_parser ():
    parser = argparse.ArgumentParser()
    parser.add_argument ('-s', '--source')
    parser.add_argument('-c', '--clone')
    parser.add_argument('-i', '--interval')
    parser.add_argument('-l', '--log')

    return parser


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
            full_path = os.path.join(path, file)
            file_hash = file_to_hash_sha256(full_path)
            rel_path = os.path.relpath(full_path, start=directory)
            file_dictionary[rel_path] = file_hash
    return file_dictionary


if __name__ == "__main__":
    parser = create_parser()
    namespace = parser.parse_args(sys.argv[1:])

    input_validation(namespace.source,namespace.clone, namespace.interval, namespace.log)

    original_directory = namespace.source
    clone_directory = namespace.clone
    sync_interval = int(namespace.interval)
    log_file = namespace.log

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

    for item1 in clone_files.items():
        file_found = False
        for item2 in origin_files.items():
            if item1 == item2:
                file_found = True
        if not file_found:
            remove_file(item1)

    for item1 in origin_files.items():
        file_found = False
        for item2 in clone_files.items():
            if item1 == item2:
                file_found = True
        if not file_found:
            copy_file(item1)
            


