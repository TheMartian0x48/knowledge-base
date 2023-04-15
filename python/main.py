#!/usr/bin/python3

import subprocess
import os
import json
import constants

# CONFIG_FILE = "/.config/config_spanish_the_matian0x48.json"
CONFIG_FILE = "config.json"
APP_CONFIGURATIONS = map()
NOTIFICATION_CONFIGURATIONS = map()


def load_configuration():
    with open(CONFIG_FILE, "r") as f:
        configs = json.loads(f.read())
    app_config = configs["APP"]
    notification_config = configs["NOTIFICATIONS"]
    return app_config, notification_config


def send_notification(summary, message):
    configs = {
        f"{constants.NOTIFICATION_ICON}": "--icon",
        f"{constants.NOTIFICATION_URGENCY_LEVEL}": "--urgency",
        f"{constants.NOTIFICATION_APP_NAME}": "--app-name",
        f"{constants.NOTIFICATION_EXPIRE_TIME}": "--expire-time"
    }
    args = ['notify-send']
    for key in configs.keys():
        if NOTIFICATION_CONFIGURATIONS[key] is not None:
            args.append(f"{configs[key]}={NOTIFICATION_CONFIGURATIONS[key]}")

    args.append(summary)
    args.append(message)
    subprocess.call(args)


def run_app():
    pass


def main():
    APP_CONFIGURATIONS, NOTIFICATION_CONFIGURATIONS = load_configuration()
    run_app()
