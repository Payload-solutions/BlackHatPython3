#!/usr/bin/python3

"""Common trojan tasking on windows"""

# from ctypes import byref, create_string_buffer, c_ulong, windll
from ctypes import *
from io import StringIO

import os
import pythoncom
import pyHook
import win32clipboard
import sys
import time


def main():
    print(dir(ctypes))


if __name__ == " __main__":
    main()
