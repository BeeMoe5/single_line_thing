import ast
import copy
import os
import sys
import typing

import astunparse


def all_isinstance(_type, iterable: list):
    return all(isinstance(item, _type) for item in iterable)


def create_module_from_node(node) -> ast.Module:
    return ast.parse(astunparse.unparse(node))


def unparse_imports(imports) -> str:
    unparsed_imports = ""
    for imp in imports:
        unparsed_imports += astunparse.unparse(imp)
    return unparsed_imports


def unparse_ifs(n: ast.If, count: int) -> typing.List[ast.Module]:
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
            print(astunparse.unparse(node))
            module = create_module_from_node(node)
            modules.append(module)

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
    import_nodes = filter(
        lambda n: isinstance(n, (ast.Import, ast.ImportFrom)), parsed.body
    )
    unparsed_imports = unparse_imports(import_nodes)
    # print(unparsed_imports)
    # make initial file
    with open("output/_1.py", "w") as _1:
        _1.write(unparsed_imports)

    for count, node in enumerate(parsed.body, start=1):
        # skip imports
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            continue

        # print(f"{node=}")
        # print(astunparse.unparse(node))
        file_contents = ""

        if isinstance(node, ast.Assign):
            file_contents += astunparse.unparse(node)
        elif isinstance(node, ast.If):
            file_contents += unparse_ifs(node, count)


if __name__ == "__main__":
    main()
