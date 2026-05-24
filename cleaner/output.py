import os


LINE_LENGTH = 60


def relative_path(path, base_directory):
    return os.path.relpath(path, base_directory)


def print_section(title):
    print()
    print("=" * LINE_LENGTH)
    print(title)
    print("=" * LINE_LENGTH)


def print_single_action(index, action, path, base_directory):
    print(f"{index}. {action}: {relative_path(path, base_directory)}")
    print()


def print_pair_action(index, action, source, target, source_label, target_label, base_directory):
    print(f"{index}. {action}: {source_label} {relative_path(source, base_directory)}")
    print(f"   {target_label}: {relative_path(target, base_directory)}")
    print()


def print_permission_action(index, path, old_permissions, new_permissions, base_directory):
    print(f"{index}. change permissions: {relative_path(path, base_directory)}")
    print(f"   from: {old_permissions}")
    print(f"   to:   {new_permissions}")
    print()