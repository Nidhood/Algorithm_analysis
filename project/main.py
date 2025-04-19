#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
from free_flow.free_flow import free_flow

def main():
    board_file_example = "inputs/board_1.txt"
    free_flow(board_file_example)

if __name__ == "__main__":
    main()
    sys.exit(1)