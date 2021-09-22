import configparser
from pathlib import Path


def main() -> None:
    MAIN_SCRIPT_BASENAME = "smart_key_box.service"

    SETUP_DIR = Path(__file__).resolve().parent
    PROJ_DIR = SETUP_DIR.parent
    TEMPLATE_SERVICE_FILENAME = SETUP_DIR / "template.service"
    DST_SERVICE_FILENAME = SETUP_DIR / MAIN_SCRIPT_BASENAME

    # PYTHON_PATH = PROJ_DIR / ".env" / "bin" / "python3"
    PYTHON_PATH = "/usr/bin/python3"
    MAIN_PY_FILENAME = PROJ_DIR / "src" / "main.py"
    FLAG = "--do-post-slack-message"

    config = configparser.ConfigParser()
    config.optionxform = str
    config.sections()
    config.read(TEMPLATE_SERVICE_FILENAME)
    config["Service"]["ExecStart"] = f"{PYTHON_PATH} {MAIN_PY_FILENAME} {FLAG}"

    with DST_SERVICE_FILENAME.open('w') as configfile:
        config.write(configfile)


if __name__ == "__main__":
    main()
