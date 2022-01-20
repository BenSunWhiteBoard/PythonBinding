import pty
import cffi
import invoke
import pathlib
import sys
import os
import shutil
import re
import glob

on_win = sys.platform.startswith("win")

@invoke.task
def clean(c):
    """Remove any built objects"""
    for file_pattern in (
        "*.o",
        "*.so",
        "*.obj",
        "*.dll",
        "*.exp",
        "*.lib",
        "*.pyd",
    ):
        for file in glob.glob(file_pattern):
            os.remove(file)
    for dir_pattern in "Release":
        for dir in glob.glob(dir_pattern):
            shutil.rmtree(dir)

def print_banner(msg):
    print("==================================================")
    print("= {} ".format(msg))

@invoke.task()
def build_example(c, path=None):
    """Build the shared library for the sample C code"""
    # c: invoke.Context
    if on_win:
        if not path:
            print("Path is missing")
        else:
            print("Win not support yet")
    else:
        print_banner("Building C Library")
        cmd = "gcc -c -Wall -Werror -fpic c_example.c"
        invoke.run(cmd)
        invoke.run("gcc -shared -o libexample.so c_example.o")

        print("* Complete")

@invoke.task()
def test_pointer(c):
    print_banner("Testing pointer in ctypes")
    invoke.run("python3 pointer_test.py", pty = True)

@invoke.task()
def test_struct(c):
    print_banner("Testing struct in ctypes")
    invoke.run("python3 struct_test.py", pty = True)

@invoke.task()
def build_start(c, path=None):
    if on_win:
        if not path:
            print("Path is missing")
        else:
            print("Win not support yet")
    else:
        print_banner("Building C Library")
        cmd = "gcc -c -Wall -Werror -fpic c_example.c"
        invoke.run(cmd)
        invoke.run("gcc -shared -o libexample.so c_example.o")

        print("* Complete")