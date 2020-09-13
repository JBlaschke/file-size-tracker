#!/usr/bin/env python
# -*- coding: utf-8 -*-


from os       import walk
from os.path  import join
from sys      import argv
from time     import sleep
from pathlib  import Path
from datetime import datetime



def get_files(dirname, single_level=True):

    files = []
    for (dirpath, dirnames, filenames) in walk(dirname):

        for filename in filenames:
            files.append(join(dirpath, filename))

        if single_level:
            break

    return files



def get_sizes(files):

    stats = dict()
    for cfile in files:
        stats[cfile] = dict(size = Path(cfile).stat().st_size,
                            time = datetime.now())

    return stats



def compare_sizes(sizes_1, sizes_2):

    diffs = dict()
    for key in sizes_1:

        size_1 = sizes_1[key]["size"]
        ts_1   = sizes_1[key]["time"]
        size_2 = sizes_2[key]["size"]
        ts_2   = sizes_2[key]["time"]

        ds = size_2 - size_1
        dt = (ts_2 - ts_1).total_seconds()

        diffs[key] = dict(ds = ds, dt = dt, rate = ds/dt)

    return diffs



if __name__ == "__main__":

    ts1 = datetime.now()

    files     = get_files(argv[1])
    time_wait = int(argv[2])
    
    sizes_1 = get_sizes(files)
    sleep(time_wait)
    sizes_2 = get_sizes(files)

    diffs = compare_sizes(sizes_1, sizes_2)

    for key in diffs:
        elt = diffs[key]

        if elt["ds"] != 0:
            print(f"{key}: {elt['rate']}, {elt['ds']}")
