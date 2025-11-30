from .sheets import GSheet
from dotenv import load_dotenv
import logging, os


__all__ = ["GSheet"]

load_dotenv()

if level := os.environ.get("DATA2INSIGHTS_LOGLEVEL"):
    if hasattr(logging, level.upper()):
        log_level = getattr(logging, level.upper(), logging.INFO)
    else:
        raise ValueError(
            f"{level} is not a valid logger level: CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET"
        )

    logging.basicConfig(level=log_level)
    logger = logging.getLogger("data2insights")
    logger.info(f"Set logger level to {level}")


def init_ss(id_: str):
    """
    Get a google spreadsheet by id
    """
    from .services import Service
    from .sheets import GSheet

    service = Service()
    return GSheet(service, id_)
