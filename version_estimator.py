import sys
import json

def get_estimation(version_tags, name_data, used_names):
    available_tags = set(version_tags)
    for name in used_names:
        if name is not None and name in name_data:
            available_tags &= set(name_data[name])
    last_tag = None
    first_tag = None
    for i, tag in reversed(list(enumerate(version_tags))):
        if last_tag is None and tag in available_tags:
            last_tag = tag
        if last_tag is not None and tag not in available_tags:
            first_tag = tag
    return first_tag, last_tag

def get_req_string(module_name, first_tag, last_tag):
    result = module_name
    if last_tag:
        result += "<={}".format(last_tag)
    if first_tag:
        result += ",>{}".format(first_tag)
    return result

if __name__ == "__main__":
    used_names_by_module = json.loads(sys.stdin.read())
    with open("package_info.json", "r") as f:
        package_info = json.loads(f.read())

    result = []
    for module_name, used_names in used_names_by_module.items():
        first_tag, last_tag = get_estimation(
            package_info[module_name]["version_tags"],
            package_info[module_name]["name_data"],
            used_names
        )
        result.append(get_req_string(module_name, first_tag, last_tag))
    print(" ".join(result))