"""Privacy-conscious rotating logs."""
import logging
from logging.handlers import RotatingFileHandler
from sentinel.config import log_dir

def configure_logging() -> None:
    handler=RotatingFileHandler(log_dir()/"sentinel.log",maxBytes=1_000_000,backupCount=3,encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s"))
    root=logging.getLogger()
    if not root.handlers:
        root.setLevel(logging.INFO); root.addHandler(handler)
