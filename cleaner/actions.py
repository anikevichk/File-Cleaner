import os


class ActionChooser:
    def __init__(self, interactive=False):
        self.interactive = interactive
        self.always_apply = set()
        self.always_skip = set()

    def should_apply(self, action_key, description=None):
        if not self.interactive:
            return False

        if action_key in self.always_apply:
            return True

        if action_key in self.always_skip:
            return False

        while True:
            answer = input(
                "Apply this action? [y]es / [n]o / [a]lways yes / [s]kip all: "
            ).strip().lower()

            if answer in ("y", "yes", "t", "tak"):
                return True

            if answer in ("n", "no", "nie", ""):
                return False

            if answer in ("a", "all", "always", "zawsze"):
                self.always_apply.add(action_key)
                return True

            if answer in ("s", "skip", "skip all", "pomin", "pomijaj"):
                self.always_skip.add(action_key)
                return False

            print("Please choose: y, n, a or s.")


def relative_path(path, base_directory):
    return os.path.relpath(path, base_directory)


def describe_single(action, path, base_directory):
    return f"{action}: {relative_path(path, base_directory)}"


def describe_pair(action, source, target, source_label, target_label, base_directory):
    return (
        f"{action}: {source_label} {relative_path(source, base_directory)}\n"
        f"{target_label}: {relative_path(target, base_directory)}"
    )


def describe_permissions(path, old_permissions, new_permissions, base_directory):
    return (
        f"change permissions: {relative_path(path, base_directory)}\n"
        f"from: {old_permissions}\n"
        f"to:   {new_permissions}"
    )
