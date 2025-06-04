#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os

def clear_screen():
    if os.name == "nt":
        os.system("cls")
    else:
        print("\033[2J\033[H", end="")