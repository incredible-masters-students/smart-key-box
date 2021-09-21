import subprocess
import csv
import logging
import shlex
from time import sleep

from read_settings import PROJ_DIR


class SmartphoneBluetoothInformation:
    def __init__(
        self, logger: logging.Logger,
        hcitool_timeout: int = 3
    ) -> None:
        self.CSV_FILENAME = PROJ_DIR / "bluetooth_addresses.csv"
        self.logger = logger
        self.hcitool_timeout = hcitool_timeout

    def get_bluetooth_info(self) -> list:
        with open(self.CSV_FILENAME, 'r') as csv_f:
            reader = csv.reader(csv_f)
            addresses = [row for row in reader]

        processes = []
        for name, address in addresses:
            process = {"name": name, "result": (None, None)}
            command_str = f"hcitool name {address}"
            # command_str = "sleep 10"
            process["popen"] = subprocess.Popen(
                shlex.split(command_str),
                encoding='UTF-8',
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            processes.append(process)

        for process in processes:
            try:
                process["result"] =\
                    process["popen"].communicate(timeout=self.hcitool_timeout)
            except subprocess.TimeoutExpired:
                process["popen"].kill()

        persons_around_rpi = []
        for process in processes:
            stdout, stderr = process["result"]
            if stderr:
                self.logger.error(f"Error bluetooth info: {stderr}")
            if stdout:
                persons_around_rpi.append(process["name"])

        return persons_around_rpi


if __name__ == "__main__":
    from time import sleep, time
    logger = logging.getLogger(__name__)
    sbi = SmartphoneBluetoothInformation(logger)
    for i in range(60):
        old_time = time()
        print(sbi.get_bluetooth_info())
        print(f"time {i}: {time()-old_time}")
        sleep(1)
