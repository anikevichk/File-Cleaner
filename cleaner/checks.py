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


def check_empty(files, apply_changes, base_directory):
    actions = []

    for file in files:
        path = file["path"]

        if not os.path.exists(path):
            continue

        if file["size"] == 0:
            actions.append(path)

            if apply_changes:
                os.remove(path)

    if not actions:
        return

    print_section("EMPTY FILES")

    for index, path in enumerate(actions, start=1):
        print_single_action(index, "delete", path, base_directory)


def check_temp(files, temp_extensions, apply_changes, base_directory):
    actions = []

    for file in files:
        path = file["path"]

        if not os.path.exists(path):
            continue

        if is_temp_file(path, temp_extensions):
            actions.append(path)

            if apply_changes:
                os.remove(path)

    if not actions:
        return

    print_section("TEMPORARY FILES")

    for index, path in enumerate(actions, start=1):
        print_single_action(index, "delete", path, base_directory)


def check_duplicates(files, apply_changes, base_directory):
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

            if apply_changes:
                os.remove(path)

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


def check_versions(files, apply_changes, base_directory):
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

            if apply_changes:
                shutil.copy2(newest["path"], path)

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


def check_bad_names(files, bad_chars, replacement, apply_changes, base_directory):
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

            if apply_changes:
                os.rename(path, new_path)

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


def check_permissions(files, desired_permissions, apply_changes, base_directory):
    desired_mode = permissions_to_mode(desired_permissions)
    actions = []

    for file in files:
        path = file["path"]

        if not os.path.exists(path):
            continue

        if file["permissions"] != desired_permissions:
            actions.append((path, file["permissions"], desired_permissions))

            if apply_changes:
                os.chmod(path, desired_mode)

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


def check_missing_in_x(files, x_directory, temp_extensions, apply_changes, base_directory):
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

        actions.append((path, destination))

        if apply_changes:
            os.makedirs(os.path.dirname(destination), exist_ok=True)
            shutil.move(path, destination)
            hashes_in_x.add(current_hash)

    if not actions:
        return

    print_section("FILES MISSING IN X")

    for index, (source, destination) in enumerate(actions, start=1):
        print_pair_action(
            index,
            "move",
            source,
            destination,
            "from:",
            "to",
            base_directory
        )


def check_outside_x_duplicates(files, x_directory, apply_changes, base_directory):
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

            if apply_changes:
                os.remove(path)

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