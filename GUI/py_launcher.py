#!/usr/bin/env python3
# -*- codding: utf-8 -*-

import os
import sys

from datetime import datetime

max_log_files = 20
log_rep = "../log/"
log_file_name = log_rep + "log.txt"


def rotate_log():
    last_log_file = log_file_name + "." + str(max_log_files)

    if os.path.exists(last_log_file):
        os.remove(last_log_file)

    for i in range(max_log_files - 1, 0, -1):
        if os.path.exists(log_file_name + "." + str(i)):
            os.rename(log_file_name + "." + str(i), log_file_name + "." + str(i + 1))

    if os.path.exists(log_file_name):
        os.rename(log_file_name, log_file_name + ".1")

def log_platform_information():
    import platform
    with open(log_file_name, "a") as f:
        f.write("\n### Platform informations ###\n")
        f.write("machine: " + str(platform.machine()) + "\n")
        f.write("arch: " + str(platform.architecture()) + "\n")
        f.write("proc: " + str(platform.processor()) + "\n")
        f.write("system: " + str(platform.system()) + "\n")
        f.write("system version: " + str(platform.version()) + "\n")
        f.write("system release: " + str(platform.release()) + "\n")
        f.write("system win32: " + str(platform.win32_ver()) + "\n")
        f.write("uname: " + str(platform.uname()) + "\n")
        f.write("python version: " + str(platform.python_version()) + "\n")
        f.write("python implementation: " + str(platform.python_implementation()) + "\n")
        f.write("python revision: " + str(platform.python_revision()) + "\n")
        f.write("python compiler: " + str(platform.python_compiler()) + "\n")
        f.write("### end platform informations ###\n")

if __name__ == '__main__':
    from main import start_qt_application
    if not os.path.exists(log_rep):
        os.mkdir(log_rep)
    else:
        rotate_log()

    with open(log_file_name, 'w') as logfile:
        logfile.write("Starting log at: " + datetime.now().isoformat() + "\n")

    log_platform_information()

    with open(log_file_name, "a") as f:
        f.write("\n### Starting GUI ###\n\n")

    start_qt_application()
