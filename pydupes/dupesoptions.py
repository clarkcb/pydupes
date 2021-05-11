# -*- coding: utf-8 -*-
###############################################################################
#
# dupesoptions.py
#
# class DupesOptions: defines the available command-line options and
#                     corresponding utility methods
#
###############################################################################
import argparse
from typing import List

from .dupesexception import DupesException
from .dupessettings import DupesSettings


class DupesOptions(object):
    """class to provide usage info and parse command-line arguments into settings"""

    def __init__(self):
        self._parser = self.__get_parser()

    def __get_parser(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(usage='%(prog)s [options] DIRECTORY...', add_help=False, exit_on_error=False)
        parser.add_argument('-r', '--recurse', action='store_true', help='for every directory given follow subdirectories encountered within')
        parser.add_argument('-R', '--recurse:', dest='recurse_dirs', type=str, action='append', help='for every directory given after this option follow subdirectories encountered within')
        parser.add_argument('-G', '--minsize', metavar='SIZE', type=int, help='consider only files greater than or equal to SIZE bytes', default=-1)
        parser.add_argument('-L', '--maxsize', metavar='SIZE', type=int, help='consider only files less than or equal to SIZE bytes', default=-1)
        parser.add_argument('-n', '--noempty', action='store_true', help='exclude zero-length files from consideration')
        parser.add_argument('-A', '--nohidden', action='store_true', help='exclude hidden files from consideration')
        parser.add_argument('-S', '--size', action='store_true', help='show size of duplicate files')
        parser.add_argument('-t', '--time', action='store_true', help='show modification time of duplicate files')
        parser.add_argument('-m', '--summarize', action='store_true', help='summarize dupe information')
        parser.add_argument('-o', '--order', metavar='BY', choices=['time', 'ctime', 'name'], help="select sort order for output and deleting; by file modification time (BY='time'; default), status change time (BY='ctime'), or filename (BY='name')")
        parser.add_argument('-i', '--reverse', action='store_true', help="reverse order while sorting")
        parser.add_argument('-v', '--version', action='store_true', help="display pydupes version")
        parser.add_argument('-h', '--help', action='store_true', help="display this help message")
        parser.add_argument('-x', '--in-ext', dest='in_exts', metavar='EXT', type=str, action='append', help="extensions of files to include")
        parser.add_argument('-X', '--out-ext', dest='out_exts', metavar='EXT', type=str, action='append', help="extensions of files to exclude")
        parser.add_argument('-d', '--in-dirpattern', dest='in_dirpatterns', metavar='PAT', type=str, action='append', help="dirname regex patterns of dirs to include")
        parser.add_argument('-D', '--out-dirpattern', dest='out_dirpatterns', metavar='PAT', type=str, action='append', help="dirname regex patterns of dirs to exclude")
        parser.add_argument('-f', '--in-filepattern', dest='in_filepatterns', metavar='PAT', type=str, action='append', help="filename regex patterns of files to include")
        parser.add_argument('-F', '--out-filepattern', dest='out_filepatterns', metavar='PAT', type=str, action='append', help="filename regex patterns of files to exclude")
        parser.add_argument('--in-filetype', dest='in_filetypes', metavar='TYPE', type=str, action='append', help="filetype of files to include")
        parser.add_argument('--out-filetype', dest='out_filetypes', metavar='TYPE', type=str, action='append', help="filetype of files to exclude")
        parser.add_argument('--debug', action='store_true', help="debug-level output")
        # NOTE: dirs is defined as optional so that we can avoid errors if -h or -v
        parser.add_argument('dirs', metavar='DIRECTORY', nargs='*', type=str, help='directory to find dupes under')
        return parser

    def settings_from_args(self, args: List[str]) -> DupesSettings:
        parsed_args = self._parser.parse_args(args)
        paths = set([])
        if parsed_args.dirs:
            paths.update(parsed_args.dirs)
        settings = DupesSettings(recursive=parsed_args.recurse, recurse_dirs=parsed_args.recurse_dirs,
            noempty=parsed_args.noempty, minsize=parsed_args.minsize, maxsize=parsed_args.maxsize,
            excludehidden=parsed_args.nohidden, size=parsed_args.size, time=parsed_args.time,
            summarize=parsed_args.summarize, reverse=parsed_args.reverse, printusage=parsed_args.help,
            printversion=parsed_args.version, debug=parsed_args.debug, paths=paths)
        if settings.printusage or settings.printversion:
            return settings
        if parsed_args.in_exts:
            settings.add_exts(parsed_args.in_exts, 'in_extensions')
        if parsed_args.out_exts:
            settings.add_exts(parsed_args.out_exts, 'out_extensions')
        if parsed_args.in_dirpatterns:
            settings.add_patterns(parsed_args.in_dirpatterns, 'in_dirpatterns')
        if parsed_args.out_dirpatterns:
            settings.add_patterns(parsed_args.out_dirpatterns, 'out_dirpatterns')
        if parsed_args.in_filepatterns:
            settings.add_patterns(parsed_args.in_filepatterns, 'in_filepatterns')
        if parsed_args.out_filepatterns:
            settings.add_patterns(parsed_args.out_filepatterns, 'out_filepatterns')
        if parsed_args.in_filetypes:
            settings.add_filetypes(parsed_args.in_filetypes, 'in_filetypes')
        if parsed_args.out_filetypes:
            settings.add_filetypes(parsed_args.out_filetypes, 'out_filetypes')
        if parsed_args.order:
            order = parsed_args.order.lower()
            if order == 'time':
                settings.order = 'time'
            elif order == 'ctime':
                settings.order = 'ctime'
            elif order == 'name':
                settings.order = 'name'
            else:
                raise DupesException(f'invalid order: {parsed_args.order}')
        return settings

    def usage(self):
        self._parser.print_help()
