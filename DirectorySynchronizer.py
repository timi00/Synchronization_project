import sys
import os.path
import logging
import hashlib
import argparse


class DirectorySynchronizer:
    def __init__(self, logger, source_dir, clone_dir):
        self.logger = logger
        self.source_dir = source_dir
        self.clone_dir = clone_dir

    def copy_file(self):
        pass

    def remove_file(self):
        pass

    def file_to_hash_sha256(self, filename):
        sha256_hash = hashlib.sha256()
        with open(filename, "rb") as f:
            # Read and update hash string value in blocks of 4K
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def files_to_dictionary(self, directory):
        file_dictionary = {}
        for path, currentDirectory, files in os.walk(directory):
            for file in files:
                full_path = os.path.join(path, file)
                file_hash = self.file_to_hash_sha256(full_path)
                rel_path = os.path.relpath(full_path, start=directory)
                file_dictionary[rel_path] = file_hash
        return file_dictionary

    def synchronize_files(self, origin_files, clone_files):
        for filename, filehash in clone_files.items():
            orig_filehash = origin_files.get(filename)
            if filehash != orig_filehash:
                try:
                    self.remove_file()
                except Exception as e:
                    self.logger.error(f"Unable to remove file {filename}. {e}")

        for filename, filehash in origin_files.items():
            clone_filehash = clone_files.get(filename)
            if filehash != clone_filehash:
                try:
                    self.copy_file()
                except Exception as e:
                    self.logger.error(f"Unable to copy file {filename}. {e}")

    def run(self, interval):
        origin_files = self.files_to_dictionary(self.source_dir)
        clone_files = self.files_to_dictionary(self.clone_dir)
