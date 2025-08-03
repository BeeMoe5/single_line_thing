import os
import sys, discord
from math import isnan
from sys import intern, dllhandle
from os.path import pardir
from os.path import isdir, isfile
from discord.ext import commands as cmds
from datetime import datetime as dt, date as d

name, name2 = "test", "test2"
name3, name4, *rest_of = "test3", "test4", "test5", "test6"

if name == "test":
    print("cool")
else:
    print("not cool")


print(name)
print(name2)
print(name3, name4)
print(*rest_of)
