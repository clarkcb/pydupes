# -*- coding: utf-8 -*-
###############################################################################
#
# dupesresult.py
#
# class DupesResult: encapsulates a dupes result
#
###############################################################################
from typing import List

from pyfind import FindFile


class DupesResult(object):
    """a class to encapsulate a dupes result, which is a list of matching
       files for a given file size"""

    __slots__ = ['size', 'files']

    def __init__(self, size: int, files: List[FindFile] = None):
        self.size = size
        self.files = files if files else []

    def append(self, file: FindFile):
        self.files.append(file)

    def __len__(self):
        return len(self.files)
