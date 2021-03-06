import hashlib
import os.path
import shutil
import time


class DirectorySynchronizer:
    def __init__(self, logger, source_dir, clone_dir):
        self.logger = logger
        self.source_dir = source_dir
        self.clone_dir = clone_dir

    def create_dir(self, directory):
        full_path = os.path.join(self.clone_dir, directory)
        os.mkdir(full_path)
        self.logger.info(f"Directory {full_path} was created")

    # another possible solution: instead of creating new directory, we can copy existing from source:
    # def copy_dir(self, directory):
    #     source_path = os.path.join(self.source_dir, directory)
    #     clone_path = os.path.join(self.clone_dir, directory)
    #     if not os.path.exists(clone_path):
    #         shutil.copytree(source_path, clone_path)

    def remove_dir(self, directory):
        full_path = os.path.join(self.clone_dir, directory)
        shutil.rmtree(full_path)
        self.logger.info(f"Directory {full_path} was deleted")

    def copy_file(self, file):
        source_path = os.path.join(self.source_dir, file)
        clone_path = os.path.join(self.clone_dir, file)
        shutil.copy2(source_path, clone_path)
        self.logger.info(f"File {file} was copied from {source_path}")

    def remove_file(self, file):
        full_path = os.path.join(self.clone_dir, file)
        os.remove(full_path)
        self.logger.info(f"File {full_path} was deleted")

    @staticmethod
    def file_to_hash_sha256(filename):
        sha256_hash = hashlib.sha256()
        with open(filename, "rb") as f:
            # Read and update hash string value in blocks of 4K
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    @staticmethod
    def directories_to_tuple(directory):
        directories = tuple()
        for dirpath, dirnames, files in os.walk(directory):
            for dirname in dirnames:
                full_path = os.path.join(dirpath, dirname)
                rel_path = (os.path.relpath(full_path, start=directory),)
                directories += rel_path
        return directories

    def files_to_dictionary(self, directory):
        file_dictionary = {}
        for path, currentDirectory, files in os.walk(directory):
            for file in files:
                full_path = os.path.join(path, file)
                file_hash = self.file_to_hash_sha256(full_path)
                rel_path = os.path.relpath(full_path, start=directory)
                file_dictionary[rel_path] = file_hash
        return file_dictionary

    def synchronize_directories(self, origin_dirs, clone_dirs):
        # checks if directory from clone directory exists in source directory. If not, it removes the directory from
        # clone directory
        for clone_dir in clone_dirs:
            dir_found = False
            for origin_dir in origin_dirs:
                if clone_dir == origin_dir:
                    dir_found = True
            if not dir_found:
                try:
                    self.remove_dir(clone_dir)
                except Exception as e:
                    self.logger.error(f"Unable to remove directory {clone_dir}. {e}")
        # checks if directory from source directory exists in clone directory. If not, it creates the directory in
        # clone directory
        for origin_dir in origin_dirs:
            dir_found = False
            for clone_dir in clone_dirs:
                if clone_dir == origin_dir:
                    dir_found = True
            if not dir_found:
                try:
                    self.create_dir(origin_dir)
                except Exception as e:
                    self.logger.error(f"Unable to create directory {origin_dir}. {e}")

    def synchronize_files(self, origin_files, clone_files):
        # checks if file from clone directory exists in source directory. If not, it removes the file from
        # clone directory
        for filename, filehash in clone_files.items():
            orig_filehash = origin_files.get(filename)
            if filehash != orig_filehash:
                try:
                    self.remove_file(filename)
                except Exception as e:
                    self.logger.error(f"Unable to remove file {filename}. {e}")
        # checks if file from source directory exists in clone directory. If not, it creates the file in
        # clone directory
        for filename, filehash in origin_files.items():
            clone_filehash = clone_files.get(filename)
            if filehash != clone_filehash:
                try:
                    self.copy_file(filename)
                except Exception as e:
                    self.logger.error(f"Unable to copy file {filename}. {e}")

    def run(self, interval):
        while True:
            if not os.path.isdir(self.source_dir):
                self.logger.error(f"{self.source_dir} directory does not exist!")
                break
            origin_dirs = self.directories_to_tuple(self.source_dir)

            if not os.path.isdir(self.clone_dir):
                shutil.copytree(self.source_dir, self.clone_dir)
            clone_dirs = self.directories_to_tuple(self.clone_dir)

            self.synchronize_directories(origin_dirs, clone_dirs)

            origin_files = self.files_to_dictionary(self.source_dir)
            clone_files = self.files_to_dictionary(self.clone_dir)
            self.synchronize_files(origin_files, clone_files)

            self.logger.info(f"\nDirectory {self.clone_dir} is synchronized with {self.source_dir}")
            self.logger.info(f"\nNext synchronization will be in {interval} seconds")
            # waiting for next iteration
            time.sleep(interval)
