import os


DEFAULT_CONFIG = {
    "permissions": "rw-r--r--",
    "bad_chars": ':";*?$#`|\\',
    "replacement": "_",
    "temp_extensions": ".tmp,~",
}


def read_config(config_path):
    config = DEFAULT_CONFIG.copy()

    if not os.path.exists(config_path):
        return config

    with open(config_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if not line or line.startswith("#") or "=" not in line:
                continue

            key, value = line.split("=", 1)
            config[key.strip()] = value.strip()

    return config