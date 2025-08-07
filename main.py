import ast
import copy
import os
import sys
import typing

import astunparse


class TheTransformer(ast.NodeTransformer):
    def visit_Import(self, node):
        pass


def allisinstance(_type, iterable: list):
    return all(isinstance(item, _type) for item in iterable)


def create_module_from_node(node) -> ast.Module:
    return ast.parse(astunparse.unparse(node))


def unparse_imports(imports: list[typing.Union[ast.Import, ast.ImportFrom]]) -> str:
    combined_imports = []
    for imp in imports:
        if isinstance(imp, ast.Import):
            # print(imp.__dict__)
            combined_imports.extend(imp.names)
            # names = [F"{alias.name=} {alias.asname=}" for alias in imp.names]
            # print(*names, sep="\n")
        if isinstance(imp, ast.ImportFrom):
            new_imports = []
            
    unparsed_imports = astunparse.unparse(ast.Import(names=combined_imports)).strip()
    print(unparsed_imports)
    return unparsed_imports


def unparse_ifs(n: ast.If, count: int) -> list[str]:
    """
    to split if statement expressions into different files
    :param n:
    :param count:
    :return:
    """
    modules = []
    for node in n.body:
        if isinstance(node, ast.If):
            modules += unparse_ifs(n, count)

        if isinstance(node, ast.Expr):  # if it can be in one line
            # print(astunparse.unparse(node))
            module = create_module_from_node(node)
            modules.append(astunparse.unparse(module))

    return modules


def main():
    try:
        file_name = sys.argv[1]
    except IndexError:
        print("pass in a file name!")
        return exit(1)

    with open(file_name, "r") as f:
        code = f.read()

    if not os.path.exists("output"):
        os.mkdir("output")

    parsed = ast.parse(code)
    # filter imports
    import_nodes = list(filter(
        lambda n: isinstance(n, (ast.Import, ast.ImportFrom)), parsed.body
    ))
    unparsed_imports = unparse_imports(import_nodes)
    # print(unparsed_imports)
    # make initial file
    with open("output/_1.py", "w") as _1:
        _1.write(unparsed_imports)

    for count, node in enumerate(parsed.body, start=1):
        file_contents = ""
        # skip imports
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            continue

        # print(f"{node=}")
        # print(astunparse.unparse(node))

        if isinstance(node, ast.Assign):
            file_contents += astunparse.unparse(node)
        elif isinstance(node, ast.If):
            file_contents += "".join(unparse_ifs(node, count))


if __name__ == "__main__":
    main()
