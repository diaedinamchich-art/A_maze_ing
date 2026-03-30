class ConfigError(Exception):
    pass

def parse_config_file(filename: str):
    config = {}

    try:
        with open(filename, "r") as file:
            for line_number, line in enumerate(file , start = 1):
                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                if "=" not in line:
                    raise ConfigError(f"Syntax error at line {line_number}")

                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip()

                if key in config:
                    raise ConfigError(f"Duplicate key '{key}' at line {line_number}")

                config[key] = value
    except FileNotFoundError:
        raise ConfigError("Configuration file not found.")

    required_keys = [
            "WIDTH",
            "HEIGHT",
            "ENTRY",
            "EXIT",
            "OUTPUT_FILE",
            "PERFECT",
    ]

    for key in required_keys:
        if key not in config:
            raise ConfigError(f"Missing key: {key}")

    try:
        width = int(config["WIDTH"])
        height = int(config["HEIGHT"])
    except ValueError:
        raise ConfigError("WIDTH and HEIGHT must be integers.")

    if width <= 0 or height <= 0:
        raise ConfigError("WIDTH and HEIGHT must be > 0.")

    try:
        entry_x, entry_y = map(int, config["ENTRY"].split(","))
        exit_x, exit_y = map(int, config["EXIT"].split(","))
    except Exception:
        raise ConfigError("ENTRY and EXIT  must be in format x,y")

    if not (0 <= entry_x < width and 0 <= entry_y < height):
        raise ConfigError("ENTRY is out of maze bounds.")

    if not (0 <= exit_x < width and 0 <= exit_y < height):
        raise ConfigError("EXIT is out of maze bounds.")
    
    if entry_x == exit_x and entry_y == exit_y:
        raise ConfigError("ENTRY and EXIT connot be the same.")

    perfect_value = config["PERFECT"].lower()

    if perfect_value == "true":
        perfect = True
    elif perfect_value == "false":
        perfect = False
    else:
        raise ConfigError("PERFECT must be True or False.")

    output_file = config["OUTPUT_FILE"]

    seed = None
    if "SEED" in config:
        try:
            seed = int(config["SEED"])
        except ValueError:
            raise ConfigError("SEED must be an integer.")

    return {
        "width": width, 
        "height": height,
        "entry": (entry_x, entry_y),
        "exit": (exit_x, exit_y),
        "output_file": output_file,
        "perfect": perfect,
        "seed": seed
    }


