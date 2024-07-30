import os
import subprocess


def run_cmd(command):
    os.system(command)


def run_cmd_popen(command):
    return os.popen(command)


def run_cmd_subprocess(command, **kwargs):
    return subprocess.Popen(args=command, **kwargs)
