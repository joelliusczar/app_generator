import logging as builtin_logging
import os

api_log_level = os.environ.get(
	"<%= ucPrefix %>_API_LOG_LEVEL",
	builtin_logging.getLevelName(builtin_logging.WARNING)
)


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

logger.setLevel(api_log_level)

logger.addHandler(handler)




