#!/usr/bin/env python
# -*- coding: utf-8 -*-


from os          import walk
from os.path     import join
from sys         import argv
from time        import sleep
from pathlib     import Path
from datetime    import datetime
from dataclasses import dataclass



@dataclass
class FileStats:
    path: str
    size: int
    time: datetime



@dataclass
class FileStatDiff:
    path: str
    ds:   int
    dt:   float
    rate: float



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
        stats[cfile] = FileStats(path = cfile, 
                                 size = Path(cfile).stat().st_size,
                                 time = datetime.now())

    return stats



def compare_sizes(sizes_1, sizes_2):

    diffs = dict()
    for key in sizes_1:

        size_1 = sizes_1[key].size
        ts_1   = sizes_1[key].time
        size_2 = sizes_2[key].size
        ts_2   = sizes_2[key].time

        ds = size_2 - size_1
        dt = (ts_2 - ts_1).total_seconds()

        diffs[key] = FileStatDiff(path = key, ds = ds, dt = dt, rate = ds/dt)


    return diffs



if __name__ == "__main__":

    files     = get_files(argv[1])
    time_wait = int(argv[2])

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
