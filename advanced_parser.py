import json
import ast

def nb_to_code(nb_file):
    jupyter_json = json.loads(nb_file.read())
    assert jupyter_json["nbformat"] >= 4, "Jupyter version >= 4 is supported"
    result = []
    for cell in jupyter_json["cells"]:
        if cell["cell_type"] == "code":
            result.append("\n".join(cell["source"]))
    return result

def dependencies_from_code(code_text):
    class ImportFinder(ast.NodeVisitor) :
        def __init__(self):
            self.imports = set()

        def add_import(self, name):
            self.imports.add(name.split('.')[0])

        def visit_Import(self, node):
            for alias in node.names:
                self.add_import(alias.name)

        def visit_ImportFrom(self, node):
            if node.module == "__future__":
                return
            else:
                self.add_import(node.module)

    root = ast.parse(code_text) 
    import_finder = ImportFinder()
    import_finder.visit(root)
    return import_finder.imports

def dependencies_from_nb(nb_file):
    cells = nb_to_code(nb_file)
    cell_imports = map(dependencies_from_code, cells)
    total_imports = set.union(*cell_imports)
    return list(total_imports)


if __name__ == "__main__":
    import sys
    with open(sys.argv[1], "r") as nb_file:
        print(dependencies_from_nb(nb_file))
    
