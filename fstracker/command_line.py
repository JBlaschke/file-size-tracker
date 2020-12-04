#!/usr/bin/env python
# -*- coding: utf-8 -*-


from time     import sleep
from datetime import datetime

from .track import get_files, get_sizes, compare_sizes


MiB = 1024**2


def run(root_dir, time_wait):

    files = get_files(root_dir)

    print(f"TRACKING {len(files)} files over {time_wait} seconds")
    
    sizes_1 = get_sizes(files)
    sleep(time_wait)
    sizes_2 = get_sizes(files)

    diffs = compare_sizes(sizes_1, sizes_2)

    print("Files whose sizes have changed:")

    avg_rate = 0
    n_rate   = 0
    for key in diffs:
        elt = diffs[key]

        if elt.ds != 0:
            rate      = elt.rate
            avg_rate += rate
            n_rate   += 1

            rate_mbps = rate/MiB

            print(f"{key}: {rate_mbps} MiB/s, {elt.ds}")

    if n_rate > 0:
        avg_rate /= n_rate

    print(f"AVERAGE rate-of-change for {n_rate} files: {avg_rate/MiB} MiB/s")
    print(f"=>TOTAL rate-of-change for {n_rate} files: {avg_rate/MiB*n_rate} MiB/s")



def log(root_dir, time_wait, out="fs.log"):

    print(f"TRACKING {root_dir} every {time_wait} seconds")
    print(f"Tranfer rates stored to {out}")

    while True:
        files = get_files(root_dir)

        sizes_1 = get_sizes(files)
        sleep(time_wait)
        sizes_2 = get_sizes(files)

        diffs = compare_sizes(sizes_1, sizes_2)

        avg_rate = 0
        n_rate   = 0
        for key in diffs:
            elt = diffs[key]

            if elt.ds != 0:
                rate      = elt.rate
                avg_rate += rate
                n_rate   += 1

        if n_rate > 0:
            avg_rate /= n_rate

        with open(out, "a") as f:
            f.write(f"[{datetime.now()}] {n_rate} {avg_rate} {time_wait}")

        for key in diffs:
            elt = diffs[key]

            if elt.ds != 0:
                rate = elt.rate

                with open(out, "a") as f:
                    f.write(f" {rate}")

        with open(out, "a") as f:
            f.write(f"\n")
