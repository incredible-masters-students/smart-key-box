import subprocess
import csv


def read_address():
    file_name = 'ble-address.csv'
    f = open(file_name, 'r')
    blelist = list(csv.reader(f))
    return blelist


def get_bluetooth_info(bleaddress):
    procs = []
    for add in bleaddress:
        print(add[0])
        command_str = f"hcitool name {add[0]}"
        proc = subprocess.Popen(
            command_str.split(),
            encoding='UTF-8',
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        procs.append(proc)

    result = []
    for proc in procs:
        result.append(proc.communicate())

    return result


def main():
    blelist = read_address()
    print(blelist)

    res = get_bluetooth_info(blelist)
    print(res)
    return 0


if __name__ == "__main__":
    from time import sleep
    for i in range(60):
        main()
        sleep(1)
