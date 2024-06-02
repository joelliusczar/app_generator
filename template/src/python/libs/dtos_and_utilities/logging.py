import logging as builtin_logging



formatter = builtin_logging.Formatter(
	"[%(asctime)s][%(levelname)s][%(funcName)s]: %(message)s"
)

handler = builtin_logging.FileHandler(
	"<%= projectNameSnake %>.log",
	encoding="utf-8"
)

handler.setFormatter(formatter)

logger = builtin_logging.getLogger("<%= lcPrefix %>")
debugLogger = builtin_logging.getLogger("<%= lcPrefix %>.debug")

logger.setLevel(builtin_logging.INFO)

logger.addHandler(handler)




