import logging as builtin_logging



formatter = builtin_logging.Formatter("%(asctime)s %(message)s")

handler = builtin_logging.FileHandler("<%= projectName %>.log", encoding="utf-8")
debugOnlyhandler = builtin_logging.FileHandler(
	"<%= projectName %>-debug.log",
	encoding="utf-8"
)

handler.setFormatter(formatter)
debugOnlyhandler.setFormatter(formatter)

logger = builtin_logging.getLogger("<%= lcPrefix %>")
debugLogger = builtin_logging.getLogger("<%= lcPrefix %>.debug")

logger.setLevel(builtin_logging.INFO)
debugLogger.setLevel(builtin_logging.DEBUG)

logger.addHandler(handler)
debugLogger.addHandler(debugOnlyhandler)



