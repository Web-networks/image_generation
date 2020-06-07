import requests
import json
import subprocess
import sys
import json

def get_all_version_tags(package_name):
    response = requests.get("https://pypi.org/pypi/{}/json".format(package_name))
    assert response.ok, response.text
    tags = []
    return list(response.json()["releases"].keys())


def get_all_names(package_name, version_tag):
    def install_package():
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", package_name + "==" + version_tag],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

    def get_names():
        names = subprocess.check_output(["python", "names_from_module.py", package_name])
        return json.loads(names)

    def uninstall_package():
        subprocess.check_call(
            [sys.executable, "-m", "pip", "uninstall", package_name, "--yes"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL    
        )

    #print(version_tag)
    try:
        install_package()
        names = get_names()
        uninstall_package()
        return names
    except Exception as e:
        #print(type(e))
        #print(e)
        return []

def get_package_info(package_name):
    version_tags = get_all_version_tags(package_name)
    valid_version_tags = []
    versions_info = {}
    for version_tag in version_tags:
        names = get_all_names(package_name, version_tag)
        if names:
            valid_version_tags.append(version_tag)
        for name in names:
            if name not in versions_info:
                versions_info[name] = []
            versions_info[name].append(version_tag)
    #print(valid_version_tags)

    versions_info_filtered = {}
    for name, versions in versions_info.items():
        if len(versions) != len(valid_version_tags):
            versions_info_filtered[name] = versions
    return {
        "name_data": versions_info_filtered,
        "version_tags": valid_version_tags,
    }


if __name__ == "__main__":
    package_list = sys.stdin.readlines()
    data = {}
    for package_name in package_list:
        package_name = package_name.strip()
        data[package_name] = get_package_info(package_name)
    print(json.dumps(data))