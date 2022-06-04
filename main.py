import sys
import os.path
import logging


def input_validation(arg1, arg2, arg3, arg4):
    if not os.path.isdir(arg1):
        pass
    elif not os.path.isdir(arg2):
        pass
    elif not arg3.isdigit():
        pass
    elif not os.path.exists(arg4):
        pass


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
    logger.info("Our third Log Message")
    logger.error("Our error Log Message")