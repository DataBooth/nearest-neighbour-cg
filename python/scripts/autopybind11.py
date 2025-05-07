import re
from pathlib import Path


class AutoPybind11:
    """
    Given a C++ .cpp file, generates a pybind11 binding .cpp file
    that exposes all top-level classes and their public methods.
    """

    def __init__(self, cpp_path):
        self.cpp_path = Path(cpp_path)
        self.cpp_code = self.cpp_path.read_text()
        self.module_name = self.cpp_path.stem + "_cpp"
        self.binding_path = self.cpp_path.with_name(
            self.cpp_path.stem + "_bindings_tmp.cpp"
        )
        self.classes = []  # List of (class_name, methods)

    def parse_classes(self):
        # Find all top-level class definitions
        class_pattern = re.compile(r"class\s+(\w+)\s*\{([\s\S]*?)\};", re.MULTILINE)
        # Only match public methods, skip destructors/operators
        method_pattern = re.compile(
            r"(?:public:)?\s*([^\s]+)\s+(\w+)\(([^)]*)\)(\s*const)?\s*[{;]"
        )
        for class_match in class_pattern.finditer(self.cpp_code):
            class_name = class_match.group(1)
            class_body = class_match.group(2)
            methods = []
            for meth_match in method_pattern.finditer(class_body):
                ret, name, args, constness = meth_match.groups()
                if name.startswith("~") or name.startswith("operator"):
                    continue
                methods.append((ret, name, args, bool(constness)))
            self.classes.append((class_name, methods))

    def generate_binding_code(self):
        lines = [
            "#include <pybind11/pybind11.h>",
            "#include <pybind11/stl.h>",
            f'#include "{self.cpp_path.name}"',
            "namespace py = pybind11;",
            "",
            f"PYBIND11_MODULE({self.module_name}, m) {{",
        ]
        for class_name, methods in self.classes:
            lines.append(f'    py::class_<{class_name}>(m, "{class_name}")')
            # Always add default constructor if possible
            lines.append("        .def(py::init<>())")
            for ret, name, args, constness in methods:
                # Generate argument list for pybind11
                arg_names = []
                if args.strip():
                    arg_names = [
                        a.strip().split()[-1] for a in args.split(",") if a.strip()
                    ]
                arg_str = ", ".join([f'py::arg("{a}")' for a in arg_names])
                # Expose method
                lines.append(
                    f'        .def("{name}", &{class_name}::{name}'
                    + (f", {arg_str}" if arg_str else "")
                    + ")"
                )
            lines.append("        ;")
        lines.append("}")
        return "\n".join(lines)

    def write_binding_file(self):
        self.parse_classes()
        code = self.generate_binding_code()
        self.binding_path.write_text(code)
        print(f"[AutoPybind11] Binding written to: {self.binding_path}")
        return self.binding_path


# Usage example:
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python autopybind11.py path/to/source.cpp")
        exit(1)
    cpp_path = sys.argv[1]
    wrapper = AutoPybind11(cpp_path)
    wrapper.write_binding_file()
