import json
import sys
import importlib
import inspect
import json


def get_names(package_name):
    def get_names_rec(module, prefix, depth):
        if depth > 5:
            return []
        names = []
        for member_name, member in inspect.getmembers(module):
            if member_name[0] == "_":
                continue 
            full_name = prefix + "." + member_name
            names.append(full_name)
            if inspect.ismodule(member) or inspect.isclass(member):
                names += get_names_rec(member, full_name, depth + 1)
        return names

    module = importlib.import_module(package_name)
    return get_names_rec(module, package_name, 0)

if __name__ == "__main__":
    print(json.dumps(get_names(sys.argv[1])))