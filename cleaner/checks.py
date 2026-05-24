import os
import shutil
from collections import defaultdict

from cleaner.file_utils import (
    permissions_to_mode,
    is_inside_directory,
    is_temp_file,
    has_bad_chars,
    sanitize_name,
    unique_path,
    get_file_hash,
)

from cleaner.output import (
    print_section,
    print_single_action,
    print_pair_action,
    print_permission_action,
)

from cleaner.actions import (
    describe_single,
    describe_pair,
    describe_permissions,
)


def execute_action(apply_changes, chooser, action_key, description, action):
    if apply_changes:
        action()
        return

    if chooser and chooser.should_apply(action_key, description):
        action()


def check_empty(files, apply_changes, base_directory, chooser=None):
    actions = []

    for file in files:
        path = file["path"]

        if not os.path.exists(path):
            continue

        if file["size"] == 0:
            actions.append(path)

    if not actions:
        return

    print_section("EMPTY FILES")

    for index, path in enumerate(actions, start=1):
        print_single_action(index, "delete", path, base_directory)

        execute_action(
            apply_changes,
            chooser,
            "delete_empty",
            describe_single("delete", path, base_directory),
            lambda path=path: os.remove(path) if os.path.exists(path) else None
        )


def check_temp(files, temp_extensions, apply_changes, base_directory, chooser=None):
    actions = []

    for file in files:
        path = file["path"]

        if not os.path.exists(path):
            continue

        if is_temp_file(path, temp_extensions):
            actions.append(path)

    if not actions:
        return

    print_section("TEMPORARY FILES")

    for index, path in enumerate(actions, start=1):
        print_single_action(index, "delete", path, base_directory)

        execute_action(
            apply_changes,
            chooser,
            "delete_temp",
            describe_single("delete", path, base_directory),
            lambda path=path: os.remove(path) if os.path.exists(path) else None
        )


def check_duplicates(files, apply_changes, base_directory, chooser=None):
    by_hash = defaultdict(list)
    actions = []

    for file in files:
        path = file["path"]

        if not os.path.exists(path):
            continue

        by_hash[file["hash"]].append(file)

    for same_files in by_hash.values():
        if len(same_files) < 2:
            continue

        oldest = min(same_files, key=lambda item: item["mtime"])

        for file in same_files:
            path = file["path"]

            if path == oldest["path"]:
                continue

            if not os.path.exists(path):
                continue

            actions.append((path, oldest["path"]))

    if not actions:
        return

    print_section("DUPLICATE FILES")

    for index, (duplicate, original) in enumerate(actions, start=1):
        print_pair_action(
            index,
            "delete duplicate",
            duplicate,
            original,
            "file:",
            "keep oldest",
            base_directory
        )

        execute_action(
            apply_changes,
            chooser,
            "delete_duplicate",
            describe_pair(
                "delete duplicate",
                duplicate,
                original,
                "file:",
                "keep oldest",
                base_directory
            ),
            lambda duplicate=duplicate: os.remove(duplicate)
            if os.path.exists(duplicate)
            else None
        )


def check_versions(files, apply_changes, base_directory, chooser=None):
    by_name = defaultdict(list)
    actions = []

    for file in files:
        path = file["path"]

        if not os.path.exists(path):
            continue

        by_name[file["name"]].append(file)

    for same_name_files in by_name.values():
        if len(same_name_files) < 2:
            continue

        hashes = set(file["hash"] for file in same_name_files)

        if len(hashes) == 1:
            continue

        newest = max(same_name_files, key=lambda item: item["mtime"])

        for file in same_name_files:
            path = file["path"]

            if path == newest["path"]:
                continue

            if not os.path.exists(path):
                continue

            actions.append((path, newest["path"]))

    if not actions:
        return

    print_section("NEWER VERSIONS OF FILES")

    for index, (old_file, new_file) in enumerate(actions, start=1):
        print_pair_action(
            index,
            "replace older",
            old_file,
            new_file,
            "file:",
            "with newer",
            base_directory
        )

        execute_action(
            apply_changes,
            chooser,
            "replace_older",
            describe_pair(
                "replace older",
                old_file,
                new_file,
                "file:",
                "with newer",
                base_directory
            ),
            lambda old_file=old_file, new_file=new_file: shutil.copy2(new_file, old_file)
            if os.path.exists(old_file) and os.path.exists(new_file)
            else None
        )


def check_bad_names(files, bad_chars, replacement, apply_changes, base_directory, chooser=None):
    actions = []

    for file in files:
        path = file["path"]

        if not os.path.exists(path):
            continue

        if has_bad_chars(path, bad_chars):
            folder = os.path.dirname(path)
            old_name = os.path.basename(path)
            new_name = sanitize_name(old_name, bad_chars, replacement)
            new_path = unique_path(os.path.join(folder, new_name))

            actions.append((path, new_path))

    if not actions:
        return

    print_section("FILES WITH PROBLEMATIC NAMES")

    for index, (old_path, new_path) in enumerate(actions, start=1):
        print_pair_action(
            index,
            "rename",
            old_path,
            new_path,
            "from:",
            "to",
            base_directory
        )

        execute_action(
            apply_changes,
            chooser,
            "rename_bad_name",
            describe_pair(
                "rename",
                old_path,
                new_path,
                "from:",
                "to",
                base_directory
            ),
            lambda old_path=old_path, new_path=new_path: os.rename(old_path, new_path)
            if os.path.exists(old_path)
            else None
        )


def check_permissions(files, desired_permissions, apply_changes, base_directory, chooser=None):
    desired_mode = permissions_to_mode(desired_permissions)
    actions = []

    for file in files:
        path = file["path"]

        if not os.path.exists(path):
            continue

        if file["permissions"] != desired_permissions:
            actions.append((path, file["permissions"], desired_permissions))

    if not actions:
        return

    print_section("FILES WITH INCORRECT PERMISSIONS")

    for index, (path, old_permissions, new_permissions) in enumerate(actions, start=1):
        print_permission_action(
            index,
            path,
            old_permissions,
            new_permissions,
            base_directory
        )

        execute_action(
            apply_changes,
            chooser,
            "change_permissions",
            describe_permissions(path, old_permissions, new_permissions, base_directory),
            lambda path=path: os.chmod(path, desired_mode)
            if os.path.exists(path)
            else None
        )


def check_missing_in_x(files, x_directory, temp_extensions, apply_changes, base_directory, chooser=None):
    hashes_in_x = set()
    actions = []

    for file in files:
        path = file["path"]

        if not os.path.exists(path):
            continue

        if is_inside_directory(path, x_directory):
            hashes_in_x.add(get_file_hash(path))

    for file in files:
        path = file["path"]

        if not os.path.exists(path):
            continue

        if is_inside_directory(path, x_directory):
            continue

        if file["size"] == 0:
            continue

        if is_temp_file(path, temp_extensions):
            continue

        current_hash = get_file_hash(path)

        if current_hash in hashes_in_x:
            continue

        relative = os.path.relpath(path, base_directory)
        parts = relative.split(os.sep)

        # remove Y1 / Y2 and keep the rest of the path
        relative_inside_source = os.path.join(*parts[1:])
        destination = os.path.join(x_directory, relative_inside_source)

        if os.path.exists(destination):
            destination = unique_path(destination)

        actions.append((path, destination, current_hash))
        hashes_in_x.add(current_hash)

    if not actions:
        return

    print_section("FILES MISSING IN X")

    for index, (source, destination, current_hash) in enumerate(actions, start=1):
        print_pair_action(
            index,
            "move",
            source,
            destination,
            "from:",
            "to",
            base_directory
        )

        def move_file(source=source, destination=destination, current_hash=current_hash):
            if os.path.exists(source):
                os.makedirs(os.path.dirname(destination), exist_ok=True)
                shutil.move(source, destination)
                hashes_in_x.add(current_hash)

        execute_action(
            apply_changes,
            chooser,
            "move_missing_to_x",
            describe_pair("move", source, destination, "from:", "to", base_directory),
            move_file
        )


def check_outside_x_duplicates(files, x_directory, apply_changes, base_directory, chooser=None):
    hashes_in_x = set()
    actions = []

    for file in files:
        path = file["path"]

        if not os.path.exists(path):
            continue

        if is_inside_directory(path, x_directory):
            hashes_in_x.add(get_file_hash(path))

    for file in files:
        path = file["path"]

        if not os.path.exists(path):
            continue

        if is_inside_directory(path, x_directory):
            continue

        current_hash = get_file_hash(path)

        if current_hash in hashes_in_x:
            actions.append(path)

    if not actions:
        return

    print_section("DUPLICATES OUTSIDE X")

    for index, path in enumerate(actions, start=1):
        print_single_action(
            index,
            "delete",
            path,
            base_directory
        )

        execute_action(
            apply_changes,
            chooser,
            "delete_outside_x_duplicate",
            describe_single("delete", path, base_directory),
            lambda path=path: os.remove(path) if os.path.exists(path) else None
        )