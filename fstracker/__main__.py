#!/usr/bin/env python
# -*- coding: utf-8 -*-


from sys           import argv
from .command_line import run



if __name__ == "__main__":

    time_wait = int(argv[2])
    run(argv[1], time_wait)
