import configparser
from pathlib import Path


def main(main_script_basename: str) -> None:
    PROJ_DIR = Path(__file__).parent
    TEMPLATE_SERVICE_FILENAME = PROJ_DIR / "template.service"
    DST_SERVICE_FILENAME = PROJ_DIR / main_script_basename

    VENV_FILENAME = PROJ_DIR / ".env" / "bin" / "python3"
    MAIN_PY_FILENAME = PROJ_DIR / "main.py"

    config = configparser.ConfigParser()
    config.optionxform = str
    config.sections()
    config.read(TEMPLATE_SERVICE_FILENAME)
    config["Service"]["ExecStart"] = f"{VENV_FILENAME} {MAIN_PY_FILENAME}"

    with DST_SERVICE_FILENAME.open('w') as configfile:
        config.write(configfile)


if __name__ == "__main__":
    main(main_script_basename="key_and_rpi.service")
