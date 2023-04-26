#!/usr/bin/python3

import json
import os
import random
import subprocess
import time
from enum import Enum
from pathlib import Path

from util import get_configuration_file


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class AppConfiguration(metaclass=SingletonMeta):
    def __init__(self, configs: dict):
        self.configs = {}
        required_fields = ["KNOWLEDGE_BASE_PATH"]
        default_values = {
            "SLEEP_TIME": 600
        }
        for field in required_fields:
            if configs.get(field) is None:
                raise ValueError(f"Need {field} for app configuration")
            self.configs.setdefault(field, configs.get(field))
        for field in default_values:
            if configs.get(field) is None:
                self.configs.setdefault(field, default_values.get(field))
            else:
                self.configs.setdefault(field, configs.get(field))

    def get_knowledge_base_path(self) -> Path:
        return Path(self.configs.get("KNOWLEDGE_BASE_PATH"))

    def get_sleep_time(self) -> int:
        return int(self.configs.get("SLEEP_TIME"))


class NotificationUrgencyLevel(Enum):
    NORMAL = "NORMAL"
    LOW = "LOW"
    CRITICAL = "CRITICAL"


class NotificationConfiguration:
    def __init__(self, configs: dict):
        self.app_name = "APP_NAME"
        self.urgency_level = "URGENCY_LEVEL"
        self.icon = "ICON"
        self.expire_time = "EXPIRE_TIME"
        self.configs = {}
        required_fields = []
        default_values = {
            self.app_name: "Knowledge Base",
            self.icon: None,
            self.expire_time: 5000
        }
        for field in required_fields:
            if configs.get(field) is None:
                raise ValueError(f"Need {field} for app configuration")
            self.configs.setdefault(field, configs.get(field))
        if configs.get(self.urgency_level) is not None:
            self.configs.setdefault(
                self.urgency_level,
                NotificationUrgencyLevel[configs.get(self.urgency_level)]
            )
        else:
            self.configs.setdefault(self.urgency_level, NotificationUrgencyLevel.NORMAL)
        for field in default_values:
            if configs.get(field) is None:
                self.configs.setdefault(field, default_values.get(field))
            else:
                self.configs.setdefault(field, configs.get(field))

    def get_app_name(self) -> str:
        return self.configs.get(self.app_name)

    def get_icon_path(self) -> str:
        return self.configs.get(self.icon)

    def get_expire_time(self) -> int:
        return int(self.configs.get(self.expire_time))

    def get_urgency_level(self) -> NotificationUrgencyLevel:
        return self.configs.get(self.urgency_level)


class NotificationService(metaclass=SingletonMeta):
    def __init__(self):
        self.service_provider = "notify-send"

    def send(self, config: NotificationConfiguration, summary: str, message: str):
        # print('sending... send')
        args = [self.service_provider,
                f"--urgency={config.get_urgency_level().value}",
                f"--expire-time={config.get_expire_time()}"]
        if config.get_icon_path() is not None:
            args.append(f"--icon={config.get_icon_path()}")
        args = args + [summary, message]
        subprocess.call(args)


class KnowledgeBase(metaclass=SingletonMeta):

    def __init__(self, path: Path):
        self.path = path
        self.data = {}
        self.modification_time = 0
        if not self.path.exists() or not self.path.is_file():
            raise ValueError("Path for data is wrong.")

    def __load_data(self):
        with self.path.open() as path_to_wisdom:
            self.data = json.loads(path_to_wisdom.read())

    def get_summary_and_message(self) -> (str, str):
        modification_time = os.path.getmtime(self.path)
        if self.modification_time < modification_time:
            self.__load_data()
            self.modification_time = modification_time
        summary = random.choice(list(self.data.keys()))
        key = random.choice(list(self.data[summary].keys()))
        return summary, f"{key}\n{self.data[summary][key]}"


def load_configuration() -> (AppConfiguration, NotificationService):
    with open(get_configuration_file(), "r", encoding="utf-8") as config_file:
        configs = json.loads(config_file.read())
    return AppConfiguration(configs.get("APP")), \
        NotificationConfiguration(configs.get("NOTIFICATION"))


if __name__ == "__main__":
    app_config, notification_config = load_configuration()
    notification_service = NotificationService()
    knowledge_base = KnowledgeBase(app_config.get_knowledge_base_path())
    while True:
        notification_summary, notification_message = knowledge_base.get_summary_and_message()
        notification_service.send(notification_config, notification_summary, notification_message)
        time.sleep(app_config.get_sleep_time())
