#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
from free_flow.free_flow import free_flow
from project.command_interface.interface import Interface


def main():
    interface = Interface()
    command = ""

    print("---------------------------------BIENVENIDO AL JUEGO FREE FLOW---------------------------------")
    print("Digite el comando que desea:")

    while command != "salir":
        command = input("\n$ ")
        interface.set_command(command)
        interface.process_command()

if __name__ == "__main__":
    main()
    sys.exit(1)