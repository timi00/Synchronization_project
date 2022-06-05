import argparse
import logging
import os.path
import sys

from DirectorySynchronizer import DirectorySynchronizer


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--source', help='Path to source directory')
    parser.add_argument('-c', '--clone', help='Path to clone directory')
    parser.add_argument('-i', '--interval', help='an integer, interval for synchronizing')
    parser.add_argument('-l', '--log', help='Path to log file')

    return parser


def input_validation(arg1, arg2, arg3, arg4):
    if not os.path.isdir(arg1):
        raise NotADirectoryError("{} directory does not exist!".format(arg1))
    elif not os.path.isdir(arg2):
        raise NotADirectoryError("{} directory does not exist!".format(arg2))
    elif not arg3.isdigit():
        raise TypeError("{} is not a digit!".format(arg3))
    elif not os.path.isfile(arg4):
        raise FileNotFoundError("{} file does not exist!".format(arg4))


def create_logger(log_file):
    log_format = "%(levelname)s %(asctime)s - %(message)s"

    logging.basicConfig(format=log_format,
                        level=logging.INFO,
                        handlers=[logging.FileHandler(log_file),
                                  logging.StreamHandler()])
    logger = logging.getLogger()
    return logger


def main():
    parser = create_parser()
    namespace = parser.parse_args(sys.argv[1:])
    # printing entered arguments
    print(f"\nThe name of the program: {sys.argv[0]}")
    print(f"\nSource directory: {namespace.source}")
    print(f"\nClone directory: {namespace.clone}")
    print(f"\nInterval: {namespace.interval} min")
    print(f"\nFile for logging: {namespace.log}")

    input_validation(namespace.source, namespace.clone, namespace.interval, namespace.log)

    original_directory = namespace.source
    clone_directory = namespace.clone
    sync_interval = int(namespace.interval) * 60
    log_file = namespace.log

    logger = create_logger(log_file)

    sync = DirectorySynchronizer(logger, original_directory, clone_directory)
    sync.run(sync_interval)


if __name__ == "__main__":
    main()
