#!/usr/bin/env python3

import argparse
import os

from cleaner.config import read_config
from cleaner.actions import ActionChooser
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


def should_refresh(apply_changes, chooser):
    return apply_changes or chooser is not None


def refresh_files(directories, apply_changes, chooser):
    if should_refresh(apply_changes, chooser):
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


def get_checks(config, temp_extensions, x_directory):
    return {
        "empty": lambda files, apply, base, chooser: check_empty(
            files,
            apply,
            base,
            chooser
        ),
        "temp": lambda files, apply, base, chooser: check_temp(
            files,
            temp_extensions,
            apply,
            base,
            chooser
        ),
        "duplicates": lambda files, apply, base, chooser: check_duplicates(
            files,
            apply,
            base,
            chooser
        ),
        "versions": lambda files, apply, base, chooser: check_versions(
            files,
            apply,
            base,
            chooser
        ),
        "names": lambda files, apply, base, chooser: check_bad_names(
            files,
            config["bad_chars"],
            config["replacement"],
            apply,
            base,
            chooser
        ),
        "permissions": lambda files, apply, base, chooser: check_permissions(
            files,
            config["permissions"],
            apply,
            base,
            chooser
        ),
        "missing": lambda files, apply, base, chooser: check_missing_in_x(
            files,
            x_directory,
            temp_extensions,
            apply,
            base,
            chooser
        ),
        "outside_duplicates": lambda files, apply, base, chooser: check_outside_x_duplicates(
            files,
            x_directory,
            apply,
            base,
            chooser
        ),
    }


def run_all_checks(
    files,
    directories,
    x_directory,
    config,
    temp_extensions,
    apply_changes,
    base_directory,
    chooser=None
):
    checks = get_checks(config, temp_extensions, x_directory)

    order = [
        "empty",
        "temp",
        "versions",
        "missing",
        "outside_duplicates",
        "duplicates",
        "names",
        "permissions",
    ]

    for check_name in order:
        checks[check_name](files, apply_changes, base_directory, chooser)
        files = refresh_files(directories, apply_changes, chooser) or files

    return files


def run_selected_check(
    files,
    args,
    x_directory,
    config,
    temp_extensions,
    base_directory,
    chooser=None
):
    checks = get_checks(config, temp_extensions, x_directory)
    checks[args.mode](files, args.apply, base_directory, chooser)


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
        help="Actually apply all suggested changes."
    )

    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Ask before applying each suggested action."
    )

    args = parser.parse_args()

    if args.apply and args.interactive:
        parser.error("Use either --apply or --interactive, not both.")

    directories = [
        os.path.abspath(directory)
        for directory in args.directories
    ]

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
    print(f"Interactive mode: {args.interactive}")
    print(f"Files found: {len(files)}")

    chooser = ActionChooser(interactive=args.interactive) if args.interactive else None

    if args.mode == "all":
        run_all_checks(
            files,
            directories,
            x_directory,
            config,
            temp_extensions,
            args.apply,
            base_directory,
            chooser
        )
    else:
        run_selected_check(
            files,
            args,
            x_directory,
            config,
            temp_extensions,
            base_directory,
            chooser
        )

    if args.apply or args.interactive:
        remove_empty_directories(directories[1:])


if __name__ == "__main__":
    main()