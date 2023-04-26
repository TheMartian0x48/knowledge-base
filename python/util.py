import os
from pathlib import Path

HOME_DIR = os.environ['HOME']
CONFIG_FILE_PATH = f"{HOME_DIR}/.config/knowledge_base_config.json"
BACKUP_CONFIG_FILE = f"{HOME_DIR}/.knowledgebase/python/config.json"


def get_configuration_file() -> str:
    if Path(CONFIG_FILE_PATH).exists():
        return CONFIG_FILE_PATH
    # using backup config
    return BACKUP_CONFIG_FILE
