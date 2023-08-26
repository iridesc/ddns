from os import isatty
import coloredlogs
import logging

formatter_str = "%(asctime)s - %(levelname)s: %(message)s"
fh = logging.FileHandler(filename='log/ddns.log', encoding='utf-8', mode='a')
fh.setLevel(logging.INFO)
fh.setFormatter(logging.Formatter(formatter_str))

logger = logging.getLogger('ddns')
logger.setLevel(logging.INFO)
logger.addHandler(fh)

coloredlogs.install(level='DEBUG', logger=logger, fmt=formatter_str, isatty=True)


if __name__ == "__main__":
    logger.info("124343")
