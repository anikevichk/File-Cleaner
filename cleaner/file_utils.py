import hashlib
import os


def permissions_to_mode(permissions):
    result = 0
    values = [
        (0, "r", 0o400), (1, "w", 0o200), (2, "x", 0o100),
        (3, "r", 0o040), (4, "w", 0o020), (5, "x", 0o010),
        (6, "r", 0o004), (7, "w", 0o002), (8, "x", 0o001),
    ]

    for index, char, value in values:
        if index < len(permissions) and permissions[index] == char:
            result += value

    return result


def get_permissions(path):
    mode = os.stat(path).st_mode & 0o777

    result = ""
    flags = [
        (0o400, "r"), (0o200, "w"), (0o100, "x"),
        (0o040, "r"), (0o020, "w"), (0o010, "x"),
        (0o004, "r"), (0o002, "w"), (0o001, "x"),
    ]

    for flag, char in flags:
        result += char if mode & flag else "-"

    return result


def get_file_hash(path):
    sha = hashlib.sha256()

    with open(path, "rb") as file:
        while True:
            chunk = file.read(1024 * 1024)

            if not chunk:
                break

            sha.update(chunk)

    return sha.hexdigest()


def is_inside_directory(path, directory):
    path = os.path.abspath(path)
    directory = os.path.abspath(directory)

    return os.path.commonpath([path, directory]) == directory


def is_temp_file(path, temp_extensions):
    name = os.path.basename(path)

    for ext in temp_extensions:
        if name.endswith(ext):
            return True

    return False


def has_bad_chars(path, bad_chars):
    name = os.path.basename(path)

    for char in name:
        if char in bad_chars:
            return True

    return False


def sanitize_name(name, bad_chars, replacement):
    result = ""

    for char in name:
        if char in bad_chars:
            result += replacement
        else:
            result += char

    return result


def unique_path(path):
    if not os.path.exists(path):
        return path

    folder = os.path.dirname(path)
    filename = os.path.basename(path)
    name, extension = os.path.splitext(filename)

    counter = 1

    while True:
        new_path = os.path.join(folder, f"{name}_{counter}{extension}")

        if not os.path.exists(new_path):
            return new_path

        counter += 1


def collect_files(directories):
    files = []

    for directory in directories:
        for root, _, filenames in os.walk(directory):
            for filename in filenames:
                path = os.path.join(root, filename)

                try:
                    info = {
                        "path": path,
                        "name": filename,
                        "size": os.path.getsize(path),
                        "mtime": os.path.getmtime(path),
                        "permissions": get_permissions(path),
                        "hash": get_file_hash(path),
                    }

                    files.append(info)

                except OSError as error:
                    print(f"[ERROR] Cannot read {path}: {error}")

    return files
