#coding: utf-8
import subprocess
import csv
from time import sleep

def read_address():
    file_name = 'ble-address.csv'
    f = open(file_name,'r')
    blelist = list(csv.reader(f))
    return blelist

def get_bluetooth_info(bleaddress):
    procs=[]
    for add in bleaddress:
        print(add[0])
        proc=subprocess.Popen(['hcitool','name',add[0]], encoding='UTF-8', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        procs.append(proc)

    result=[]
    for proc in procs:
        result.append(proc.communicate())
    
    return result

def main():
    blelist = read_address()
    print(blelist)

    res = get_bluetooth_info(blelist)
    print(res)
    return 0

main()
