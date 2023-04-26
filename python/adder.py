import json
from util import get_configuration_file


def get_database_file_path() -> str:
    with open(get_configuration_file(), "r") as config_file:
        configs = json.loads(config_file.read())
    return configs["APP"]["KNOWLEDGE_BASE_PATH"]


knowledgebase = {}
with open(get_database_file_path(), 'r') as f:
    knowledgebase = json.loads(f.read())

print()
print("topics")

index_to_topics = {}
index = 1
for key in knowledgebase.keys():
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
    assert topic not in knowledgebase.keys(), f"topic {topic} already exist"
    index_to_topics[index] = topic
    knowledgebase[topic] = {}
topic = index_to_topics[index]

print()

while True:
    print(f"topic     : {topic}")
    knowledge = input("knowledge : ")
    base = input("base      : ")
    if knowledge in knowledgebase[topic].keys():
        is_override = input(f"already exist in knowledgebase. want to override ? (Y/y for yes) : ")
        if is_override == 'y' or is_override == 'Y':
            knowledgebase[topic][knowledge] = base
            print(f"overridden {knowledge} in {topic}")
    else:
        knowledgebase[topic][knowledge] = base
        print(f"added {knowledge} in {topic}")
    print()
    is_repeating = input("want to repeat? (Y/y for yes) : ")
    if is_repeating == 'y' or is_repeating == 'Y':
        continue
    else:
        break

print()

with open(get_database_file_path(), 'w') as f:
    f.write(json.dumps(knowledgebase, indent=4))
