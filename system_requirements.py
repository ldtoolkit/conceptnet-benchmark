#!/usr/bin/env python3
from datetime import datetime
from subprocess import Popen
from time import sleep
import humanize
import psutil
import shutil
import sys

time_before = datetime.now()
ram_before = psutil.virtual_memory().used
disk_before = shutil.disk_usage("/")[1]
max_ram = ram_before
max_disk = disk_before

process = Popen(sys.argv[1:])
while process.poll() is None:
    sleep(0.01)
    max_ram = max(max_ram, psutil.virtual_memory().used)
    max_disk = max(max_disk, shutil.disk_usage("/")[1])

time_after = datetime.now()
    
print("Time:", time_after - time_before)
print("RAM:", humanize.naturalsize(max_ram - ram_before, binary=True))
print("Disk:", humanize.naturalsize(max_disk - disk_before, binary=True))
