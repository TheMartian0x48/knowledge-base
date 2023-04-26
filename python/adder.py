import json, os
from pathlib import Path

HOME_DIR = os.environ['HOME']
CONFIG_FILE_PATH = f"{HOME_DIR}/.config/knowledge_base_config.json"
BACKUP_CONFIG_FILE = f"{HOME_DIR}/.knowledgebase/python/config.json"


def get_configuration_file() -> str:
    if Path(CONFIG_FILE_PATH).exists():
        return CONFIG_FILE_PATH
    # using backup config
    return BACKUP_CONFIG_FILE


def get_database_file_path() -> str:
    with open(get_configuration_file(), "r") as f:
        configs = json.loads(f.read())
    return configs["APP"]["KNOWLEDGE_BASE_PATH"]


data = {}
with open(get_database_file_path(), 'r') as f:
    data = json.loads(f.read())

print()
print("topics")

index_to_topics = {}
index = 1
for key in data.keys():
    index_to_topics[index] = key
    print(f"  {index} : {key}")
    index += 1
topic_size = index
print(f"  {index} : add new topic ")

print()
index = int(input("topic index : "))
assert 1 <= index <= topic_size, f"topic index must be greater than {0} and less than {topic_size}"

if index == topic_size:
    topic = input("new topic name : ")
    assert topic not in data.keys(), f"topic {topic} already exist"
    index_to_topics[index] = topic
    data[topic] = {}
topic = index_to_topics[index]

print()

while True:
    print(f"topic     : {topic}")
    knowledge = input("knowledge : ")
    base = input("base      : ")
    if knowledge in data[topic].keys():
        is_override = input(f"already exist in knowledgebase. want to override ? (Y/y for yes) : ")
        if is_override == 'y' or is_override == 'Y':
            data[topic][knowledge] = base
            print(f"overrided {knowledge} in {topic}")
    else:
        data[topic][knowledge] = base
        print(f"added {knowledge} in {topic}")
    print()
    is_repeating = input("want to repeat? (Y/y for yes) : ")
    if is_repeating == 'y' or is_repeating == 'Y':
        continue
    else:
        break

print()

with open(get_database_file_path(), 'w') as f:
    f.write(json.dumps(data, indent=4))