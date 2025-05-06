from pathlib import Path
import yaml


class ProjectStructure:
    def __init__(self, config_path, base_dir="project"):
        self.config_path = Path(config_path)
        self.base_dir = Path(base_dir)
        self.files = []

    def load_config(self):
        with self.config_path.open("r") as f:
            config = yaml.safe_load(f)
        self.files = config.get("files", [])

    def create(self):
        self.base_dir.mkdir(exist_ok=True)
        print(f"Created base directory: {self.base_dir}")

        for file_rel_path in self.files:
            file_path = self.base_dir / file_rel_path
            file_path.parent.mkdir(parents=True, exist_ok=True)
            if not file_path.exists():
                file_path.touch()
                print(f"Created file: {file_path}")
            else:
                print(f"File already exists: {file_path}")

    def tree(
        self,
        path=None,
        prefix="",
        max_depth=None,
        show_files=True,
        show_dirs=True,
        current_depth=0,
    ):
        """
        Generate lines of a tree view of the directory.

        Args:
            path (Path): Directory path to start from. Defaults to base_dir.
            prefix (str): Prefix string for indentation.
            max_depth (int): Max recursion depth. None means unlimited.
            show_files (bool): Whether to show files.
            show_dirs (bool): Whether to show directories.
            current_depth (int): Current recursion depth (internal use).

        Yields:
            str: Lines representing the tree view.
        """
        if path is None:
            path = self.base_dir

        if max_depth is not None and current_depth > max_depth:
            return

        try:
            entries = sorted(
                path.iterdir(), key=lambda e: (e.is_file(), e.name.lower())
            )
        except PermissionError:
            return  # Skip directories without permission

        entries = [
            e
            for e in entries
            if (e.is_dir() and show_dirs) or (e.is_file() and show_files)
        ]
        pointers = ["├── "] * (len(entries) - 1) + ["└── "]

        for pointer, entry in zip(pointers, entries):
            yield prefix + pointer + entry.name
            if entry.is_dir():
                extension = "│   " if pointer == "├── " else "    "
                yield from self.tree(
                    entry,
                    prefix + extension,
                    max_depth,
                    show_files,
                    show_dirs,
                    current_depth + 1,
                )

    def get_tree_str(self, **kwargs):
        """Return the entire tree view as a string."""
        lines = [self.base_dir.name]
        lines.extend(self.tree(**kwargs))
        return "\n".join(lines)


if __name__ == "__main__":
    # Example usage
    creator = ProjectStructure("project_structure.yaml", base_dir="nearest-neighbor")
    creator.load_config()
    creator.create()

    print("\nProject directory tree:\n")
    print(creator.get_tree_str(max_depth=3, show_files=True, show_dirs=True))
