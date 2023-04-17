#!/usr/bin/python3

import subprocess, os, time, json, sys, random
from pathlib import Path
import constants

# CONFIG_FILE = "/.config/config_spanish_the_matian0x48.json"
CONFIG_FILE = "config.json"


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

    def get_knowledge_base_path(self):
        return self.configs.get("KNOWLEDGE_BASE_PATH")

    def get_sleep_time(self):
        return self.configs.get("SLEEP_TIME")

class NotificationConfiguration():
    def __init__(self, configs: dict):
        pass


class NotificationService(metaclass=SingletonMeta):
    def __int__(self):
        pass

    def send(self, summary : str, message : str):
        pass

class KnowledgeBase(metaclass=SingletonMeta):

    def __init__(self, path):
        self.path = Path(path)
        self.data = {}
        self.modification_time = 0
        if not self.path.exists() or not self.path.is_file():
            raise "Path for data is wrong."

    def __load_data(self):
        with self.path.open() as f:
            self.path = json.loads(f.read())

    def get_summary_and_message(self) -> (str, str):
        modification_time = os.path.getmtime(self.path)
        if self.modification_time < modification_time:
            self.__load_data()
            self.modification_time = modification_time
        summary = random.choice(list(self.data.keys()))
        key = random.choice(list(self.data[summary].keys()))
        return summary, f"{key}:{self.data[summary][key]}"


def get_configuration_file() -> str:
    return CONFIG_FILE


def load_configuration() -> (AppConfiguration, NotificationService):
    with open(get_configuration_file(), "r") as f:
        configs = json.loads(f.read())
    return AppConfiguration(configs.get("APP")), NotificationConfiguration(configs.get("NOTIFICATION"))


if __name__ == "__main__":
    app_config, notification_config = load_configuration()
    notification_service = NotificationService()
    knowledge_base = KnowledgeBase(app_config.get_knowledge_base_path())
    while True:
        summary, message = knowledge_base.get_summary_and_message()
        notification_service.send(summary, message)
        time.sleep(app_config.get_sleep_time())
