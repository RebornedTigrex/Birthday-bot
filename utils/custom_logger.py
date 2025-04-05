import logging, requests

from . import config

logging.basicConfig(level=logging.INFO, format="SCRIPT | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)





def log(department, level, msg, user_id="SYSTEM"):
    
    bot_token = config["TOKEN"]
    admins = config["ADMINS"]
    
    levels = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "critical": logging.CRITICAL
    }
    logger.log(levels[level], f"{department} | {user_id} | {msg}")
    if level in ["warning", "error", "critical"]:
        msg = f"SCRIPT | {level.upper()} | {department} | {user_id} | {msg}"
        for admin_id in admins:
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            body = {"chat_id": str(admin_id), "text": msg}
            requests.post(url, data=body)