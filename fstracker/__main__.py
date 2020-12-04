#!/usr/bin/env python
# -*- coding: utf-8 -*-


from sys           import argv
from .command_line import run, log



if __name__ == "__main__":

    log_mode = False

    if len(argv) > 3:
        if argv[3].strip().lower() == "log":
            log_mode = True

    time_wait = int(argv[2])

    if log_mode:
        log(argv[1], time_wait)
    else:
        run(argv[1], time_wait)
