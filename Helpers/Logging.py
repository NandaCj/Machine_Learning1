import logging

Log_Format = "%(asctime)s %(levelname)s %(funcName)s --> %(message)s"
logging.basicConfig(level='INFO', format=Log_Format)
logger = logging.getLogger()
Info = logger.info
Error = logger.error
Critical = logger.critical
Debug = logger.debug