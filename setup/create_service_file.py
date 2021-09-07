import configparser
from pathlib import Path


def main() -> None:
    MAIN_SCRIPT_BASENAME = "smart_key_box.service"

    SETUP_DIR = Path(__file__).parent
    PROJ_DIR = SETUP_DIR.parent
    TEMPLATE_SERVICE_FILENAME = SETUP_DIR / "template.service"
    DST_SERVICE_FILENAME = SETUP_DIR / MAIN_SCRIPT_BASENAME

    VENV_FILENAME = PROJ_DIR / ".env" / "bin" / "python3"
    MAIN_PY_FILENAME = PROJ_DIR / "src" / "main.py"

    config = configparser.ConfigParser()
    config.optionxform = str
    config.sections()
    config.read(TEMPLATE_SERVICE_FILENAME)
    config["Service"]["ExecStart"] = f"{VENV_FILENAME} {MAIN_PY_FILENAME}"

    with DST_SERVICE_FILENAME.open('w') as configfile:
        config.write(configfile)


if __name__ == "__main__":
    main()
