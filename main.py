import sys
import os.path
import logging
import hashlib
import argparse
from DirectorySynchronizer import DirectorySynchronizer


def create_parser ():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--source')
    parser.add_argument('-c', '--clone')
    parser.add_argument('-i', '--interval')
    parser.add_argument('-l', '--log')

    return parser


def input_validation(arg1, arg2, arg3, arg4):
    if not os.path.isdir(arg1):
        raise NotADirectoryError("{} folder does not exist!".format(arg1))
    elif not os.path.isdir(arg2):
        raise NotADirectoryError("{} folder does not exist!".format(arg2))
    elif not arg3.isdigit():
        raise TypeError("{} is not a digit!".format(arg3))
    elif not os.path.isfile(arg4):
        raise FileNotFoundError("{} file does not exist!".format(arg4))


def create_logger(log_file):
    Log_Format = "%(levelname)s %(asctime)s - %(message)s"

    logging.basicConfig(format=Log_Format,
                        level=logging.INFO,
                        handlers=[logging.FileHandler(log_file),
                                  logging.StreamHandler()])
    logger = logging.getLogger()
    return logger


if __name__ == "__main__":
    parser = create_parser()
    namespace = parser.parse_args(sys.argv[1:])
    #todo: print entered arguments

    input_validation(namespace.source,namespace.clone, namespace.interval, namespace.log)

    original_directory = namespace.source
    clone_directory = namespace.clone
    sync_interval = int(namespace.interval)
    log_file = namespace.log

    logger = create_logger(log_file)
    # logger.info("Our third Log Message")
    # logger.error("Our error Log Message")

    sync = DirectorySynchronizer(logger, original_directory, clone_directory)
    sync.run(sync_interval)




            


