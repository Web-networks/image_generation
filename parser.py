import json
import ast
from dataclasses import dataclass
import sys
from module_lists import default_modules

@dataclass
class ImportPath:
    search_path: str
    real_path: str

    def find_name(self, name):
        name_arr = name.split(".")
        search_path_arr = self.search_path.split(".")
        search_path_len = len(search_path_arr)
        if len(name_arr) >= search_path_len:
            name_search_path = name_arr[:search_path_len]
            name_rest_path = name_arr[search_path_len:]
            if name_search_path == search_path_arr:
                found_name = self.real_path
                if name_rest_path:
                    found_name += "." + ".".join(name_rest_path)
                return found_name


class ImportTracker(ast.NodeVisitor):
    def __init__(self):
        self.import_paths = []
    

    def visit_Import(self, node):
        for alias in node.names:
            real_path = alias.name
            if alias.asname:
                search_path = alias.asname
            else:
                search_path = real_path
            self.import_paths.append(ImportPath(search_path, real_path))


    def visit_ImportFrom(self, node):
        for alias in node.names:
            real_path = node.module + "." + alias.name
            if alias.asname:
                search_path = alias.asname
            else:
                search_path = alias.name
            self.import_paths.append(ImportPath(search_path, real_path))


class NameTracker(ast.NodeVisitor):
    def __init__(self, import_paths):
        self.import_paths = import_paths
        self.used_names = set()


    def process_name(self, name):
        for import_path in self.import_paths:
            used_name = import_path.find_name(name)
            if used_name is not None:
                self.used_names.add(used_name)


    def visit_Name(self, node):
        self.process_name(node.id)


    def visit_Attribute(self, node):
        full_name = [node.attr]
        parent = node.value
        while isinstance(parent, ast.Attribute):
            full_name.append(parent.attr)
            parent = parent.value
        if isinstance(parent, ast.Name):
            full_name.append(parent.id)
            # refactor with join
            full_name.reverse()
            name = ""
            for part in full_name:
                if name:
                    name = name + "." + part
                else:
                    name += part
            self.process_name(name)

    def names_by_module(self):
        result = {}
        for name in self.used_names:
            module_name = name.split(".", 1)[0]
            if module_name in default_modules:
                continue
            if module_name not in result:
                result[module_name] = []
            result[module_name].append(name)
        return result


def nb_to_code(nb_file):
    jupyter_json = json.loads(nb_file.read())
    assert jupyter_json["nbformat"] >= 4, "Jupyter version >= 4 is supported"
    result = []
    for cell in jupyter_json["cells"]:
        if cell["cell_type"] == "code":
            result.append("\n".join(cell["source"]))
    return result


def dependencies_from_code(code_text):
    root = ast.parse(code_text, "test.py")
    import_tracker = ImportTracker()
    import_tracker.visit(root)

    name_tracker = NameTracker(import_tracker.import_paths)
    name_tracker.visit(root)
    return name_tracker.names_by_module()


def dependencies_from_nb(nb_file):
    cells = nb_to_code(nb_file)
    cell_imports = map(dependencies_from_code, cells)
    total_imports = set.union(*cell_imports)
    return list(total_imports)


if __name__ == "__main__":
    print(json.dumps(dependencies_from_code(sys.stdin.read())))
    
