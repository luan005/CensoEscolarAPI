import logging
from logging.handlers import RotatingFileHandler

def init_logging(app, *, level: str = "INFO", logfile: str = "app.log") -> None:
    log_level = getattr(logging, level.upper(), logging.INFO)
    app.logger.setLevel(log_level)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    for h in list(app.logger.handlers):
        app.logger.removeHandler(h)

    sh = logging.StreamHandler()
    sh.setFormatter(formatter)
    sh.setLevel(log_level)
    app.logger.addHandler(sh)

    fh = RotatingFileHandler(logfile, maxBytes=1_000_000, backupCount=3, encoding="utf-8")
    fh.setFormatter(formatter)
    fh.setLevel(log_level)
    app.logger.addHandler(fh)

    app.logger.info("Logging iniciado (level=%s).", level.upper())
