#!/usr/bin/env python
# -*- coding: utf-8 -*-


from time import sleep

from .track import get_files, get_sizes, compare_sizes



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

            print(f"{key}: {rate}, {elt.ds}")

    if n_rate > 0:
        avg_rate /= n_rate

    print(f"AVERAGE rate-of-change for {n_rate} files: {avg_rate/1024/1024} MB/s")
    print(f"       => TOTAL change for {n_rate} files: {avg_rate/1024/1024*n_rate} MB/s")
