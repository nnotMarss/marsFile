# 24v11Q
from pytermgui import tim
import subprocess
import sys
import os

Prefix = sys.executable
Stream = tim.print

def Get(*args):
    for arg in args:
        if isinstance(arg, str):
            Stream(arg, end="")
        elif callable(arg):
            arg()
    usrVal = input()
    return usrVal

def Install(moduleName=None, silent=False):
    if moduleName is None:
        return False
    else:
        try:
            __import__(moduleName)
            return True
        except ImportError:
            result = subprocess.run([Prefix, "-m", "pip", "install", moduleName], capture_output=True)
            if result.returncode != 0:
                if not silent:
                    Stream(" [underline]<DEBUG>[/] [italic error]Module %s installed with failure![/]\n [underline]<DEBUG>[/] [italic error]%s[/]" % (moduleName, result.stderr.decode()))
                return False
            else:
                if not silent:
                    Stream("[underline]<DEBUG>[/] [italic mediumseagreen]Module %s installed with success![/]" % moduleName)
                return True

def Clear():
    if os.name == "nt":
        _ = os.system("cls")
    else:
        _ = os.system("clear")