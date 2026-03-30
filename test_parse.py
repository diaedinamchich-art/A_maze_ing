import sys
from config import parse_config_file, ConfigError

def main():
    try:
        config = parse_config_file(sys.argv[1])
        print("Configuration loaded successfully:")
        print(config)
    except ConfigError as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
