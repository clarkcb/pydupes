#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
#
# pydupes.py
#
# A file duplicates finder based on / inspired by fdupes
#
# pydupes example cmd:
# ```
# $ pydupes -rSt -x py -D vendor ~/src/clarkcb/pydupes ~/src/xfind/python/pyfind
# ```
#
# example output:
# ```
# . . .
# 7779 bytes each:
# 2021-05-06 10:43 /Users/cary/src/clarkcb/pydupes/venv/lib/python3.8/site-packages/pyfind/finder.py
# 2021-05-06 10:43 /Users/cary/src/xfind/python/pyfind/pyfind/finder.py
# . . .
# ```
#
###############################################################################
from datetime import datetime
import sys

from .common import log
from .dupesexception import DupesException
from .dupesfinder import DupesFinder
from .dupesoptions import DupesOptions
from . import __version__

async def main():
    if sys.version_info < (3,9):
        sys.exit('Sorry, Python < 3.9 is not supported')

    options = DupesOptions()
    args = sys.argv[1:]

    settings = None
    try:
        settings = options.settings_from_args(args)
    except DupesException as e:
        log('\nERROR: {0!s}\n'.format(e))
        options.usage()
        sys.exit(1)

    if settings.debug:
        log('settings: {0!s}'.format(settings))

    if settings.printusage:
        log('')
        options.usage()
        sys.exit(0)

    if settings.printversion:
        log(f'pydupes {__version__}')
        sys.exit(0)

    try:
        finder = DupesFinder(settings)
        dupes_results = await finder.find()

        if settings.summarize:
            # NOTE: calculating summary info to match fdupes
            dup_files = 0
            total_size = 0
            for r in dupes_results:
                dup_files += len(r.files) - 1
                total_size += r.size * (len(r.files) - 1)
            mb_total_size = total_size/(1000 * 1000)
            log(f'{dup_files} duplicate files (in {len(dupes_results)} sets), occupying {round(mb_total_size, 1)} megabytes')

        else:
            for r in dupes_results:
                if settings.size:
                    log(f'{r.size} bytes each:')
                sort_key = lambda f: f.stat.st_mtime
                if settings.order == 'ctime':
                    sort_key = lambda f: f.stat.st_mtime
                elif settings.order == 'name':
                    sort_key = lambda f: f.filename
                files = list(sorted(r.files, key=sort_key, reverse=settings.reverse))
                for f in files:
                    file_row = ''
                    if settings.time:
                        file_row += '{} '.format(datetime.fromtimestamp(f.stat.st_mtime).strftime("%Y-%m-%d %H:%M"))
                    file_row += str(f)
                    log(file_row)
                log('')

    except AssertionError as e:
        log('\nERROR: {0!s}\n'.format(e))
        options.usage()
        sys.exit(1)
    except KeyboardInterrupt:
        log('')
        sys.exit(0)


if __name__ == '__main__':
    main()
