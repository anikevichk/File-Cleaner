#!/usr/bin/env python3

import argparse
import os

from cleaner.config import read_config
from cleaner.file_utils import collect_files
from cleaner.checks import (
    check_empty,
    check_temp,
    check_duplicates,
    check_versions,
    check_bad_names,
    check_permissions,
    check_missing_in_x,
    check_outside_x_duplicates,
)


def refresh_files(directories, apply_changes):
    if apply_changes:
        return collect_files(directories)

    return None


def remove_empty_directories(directories):
    changed = True

    while changed:
        changed = False

        for directory in directories:
            if not os.path.exists(directory):
                continue

            for root, dirs, files in os.walk(directory, topdown=False):
                try:
                    if not os.listdir(root):
                        os.rmdir(root)
                        changed = True
                except OSError:
                    pass


def run_all_checks(
    files,
    directories,
    x_directory,
    config,
    temp_extensions,
    apply_changes,
    base_directory
):
    check_empty(files, apply_changes, base_directory)
    files = refresh_files(directories, apply_changes) or files

    check_temp(files, temp_extensions, apply_changes, base_directory)
    files = refresh_files(directories, apply_changes) or files

    check_versions(files, apply_changes, base_directory)
    files = refresh_files(directories, apply_changes) or files

    check_missing_in_x(
        files,
        x_directory,
        temp_extensions,
        apply_changes,
        base_directory
    )
    files = refresh_files(directories, apply_changes) or files

    check_outside_x_duplicates(
        files,
        x_directory,
        apply_changes,
        base_directory
    )
    files = refresh_files(directories, apply_changes) or files

    check_duplicates(files, apply_changes, base_directory)
    files = refresh_files(directories, apply_changes) or files

    check_bad_names(
        files,
        config["bad_chars"],
        config["replacement"],
        apply_changes,
        base_directory
    )
    files = refresh_files(directories, apply_changes) or files

    check_permissions(
        files,
        config["permissions"],
        apply_changes,
        base_directory
    )
    files = refresh_files(directories, apply_changes) or files

    return files


def run_selected_check(
    files,
    args,
    x_directory,
    config,
    temp_extensions,
    base_directory
):
    if args.mode == "empty":
        check_empty(files, args.apply, base_directory)

    elif args.mode == "temp":
        check_temp(files, temp_extensions, args.apply, base_directory)

    elif args.mode == "duplicates":
        check_duplicates(files, args.apply, base_directory)

    elif args.mode == "versions":
        check_versions(files, args.apply, base_directory)

    elif args.mode == "names":
        check_bad_names(
            files,
            config["bad_chars"],
            config["replacement"],
            args.apply,
            base_directory
        )

    elif args.mode == "permissions":
        check_permissions(
            files,
            config["permissions"],
            args.apply,
            base_directory
        )

    elif args.mode == "missing":
        check_missing_in_x(
            files,
            x_directory,
            temp_extensions,
            args.apply,
            base_directory
        )


def main():
    parser = argparse.ArgumentParser(
        description="Clean and organize files."
    )

    parser.add_argument(
        "directories",
        nargs="+",
        help="Directories to check. First directory is main X directory."
    )

    parser.add_argument(
        "--config",
        default=os.path.expanduser("~/.clean_files"),
        help="Path to config file."
    )

    parser.add_argument(
        "--mode",
        default="all",
        choices=[
            "all",
            "empty",
            "temp",
            "duplicates",
            "versions",
            "names",
            "permissions",
            "missing",
        ],
        help="Check mode."
    )

    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually apply changes."
    )

    args = parser.parse_args()

    directories = [os.path.abspath(directory) for directory in args.directories]
    x_directory = directories[0]
    base_directory = os.path.commonpath(directories)

    for directory in directories:
        if not os.path.isdir(directory):
            print(f"[ERROR] Directory does not exist: {directory}")
            return

    config = read_config(args.config)

    temp_extensions = [
        ext.strip()
        for ext in config["temp_extensions"].split(",")
        if ext.strip()
    ]

    files = collect_files(directories)

    print(f"Main directory X: {os.path.relpath(x_directory, base_directory)}")
    print(f"Config: {args.config}")
    print(f"Mode: {args.mode}")
    print(f"Apply changes: {args.apply}")
    print(f"Files found: {len(files)}")

    if args.mode == "all":
        run_all_checks(
            files,
            directories,
            x_directory,
            config,
            temp_extensions,
            args.apply,
            base_directory
        )
    else:
        run_selected_check(
            files,
            args,
            x_directory,
            config,
            temp_extensions,
            base_directory
        )

    if args.apply:
        remove_empty_directories(directories[1:])


if __name__ == "__main__":
    main()