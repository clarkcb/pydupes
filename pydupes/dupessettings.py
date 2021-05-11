# -*- coding: utf-8 -*-
###############################################################################
#
# dupessettings.py
#
# class DupesSettings: encapsulates settings
#
###############################################################################
from pyfind import FindSettings
from .dupesexception import DupesException


class DupesSettings(FindSettings):
    """a class to encapsulate settings for a particular dupes session"""

    __slots__ = FindSettings.__slots__ + ['recurse_dirs', 'noempty', 'size', 'time', 'summarize', 'order', 'reverse']

    def __init__(self, **kwargs):
        FindSettings.__init__(self, **{k:v for (k,v) in kwargs.items() if k in FindSettings.__slots__})
        if self.printusage or self.printversion:
            return
        if isinstance(self.paths, list):
            self.paths = set(self.paths)
        if 'recurse_dirs' in kwargs and kwargs['recurse_dirs']:
            if isinstance(kwargs['recurse_dirs'], (list, set)):
                self.recurse_dirs = set(kwargs['recurse_dirs'])
            elif isinstance(kwargs['recurse_dirs'], str):
                self.recurse_dirs = set([kwargs['recurse_dirs']])
        else:
            self.recurse_dirs = set()
        if self.recursive and self.recurse_dirs:
            raise DupesException('options --recurse and --recurse: are not compatible')
        self.noempty = 'noempty' in kwargs and kwargs['noempty']
        self.size = 'size' in kwargs and kwargs['size']
        self.time = 'time' in kwargs and kwargs['time']
        self.summarize = 'summarize' in kwargs and kwargs['summarize']
        self.order = 'time'
        if self.minsize == -1:
            self.minsize = 0
        if self.maxsize == -1:
            self.maxsize = 0
        self.reverse = 'reverse' in kwargs and kwargs['reverse']

    def __str__(self):
        print_dict = {}
        s = '{0}('.format(self.__class__.__name__)
        for p in sorted(self.__slots__):
            val = getattr(self, p)
            if isinstance(val, set):
                if len(val) > 0 and hasattr(list(val)[0], 'pattern'):
                    print_dict[p] = str([x.pattern for x in val])
                else:
                    print_dict[p] = str(list(val))
            elif isinstance(val, str):
                if val:
                    print_dict[p] = '"{0}"'.format(val)
                else:
                    print_dict[p] = '""'
            else:
                print_dict[p] = '{0!s}'.format(val)
        next_elem = 0
        for p in sorted(print_dict.keys()):
            if next_elem:
                s += ', '
            s += '{0}: {1}'.format(p, print_dict[p])
            next_elem += 1
        s += ')'
        return s
