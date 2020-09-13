#!/usr/bin/env python
# -*- coding: utf-8 -*-


from os          import walk
from os.path     import join
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
