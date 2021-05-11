# -*- coding: utf-8 -*-
###############################################################################
#
# finder.py
#
# class DupesFinder: finds and reports file duplicates
#
###############################################################################
import asyncio
import hashlib
import os
from typing import List

from pyfind import Finder, FindFile

from .common import log
from .dupesresult import DupesResult
from .dupessettings import DupesSettings


class DupesFinder(object):
    """a class to find and report file duplicates"""

    __slots__ = ['settings', 'file_finder']

    CHUNK_SIZE = 8192

    def __init__(self, settings: DupesSettings):
        self.settings = settings
        self.__validate_settings()
        self.file_finder = Finder(settings)

    def __validate_settings(self):
        """Assert required settings in FindSettings instance"""
        assert len(self.settings.paths) > 0, 'Startpath not defined'
        for p in self.settings.paths:
            assert os.path.exists(p), 'Startpath not found'
            assert os.access(p, os.R_OK), 'Startpath not readable'

    async def get_dupes(self, size: int, files: List[FindFile]) -> List[DupesResult]:
        hash_dict = {}
        for f in files:
            md5 = hashlib.md5()
            with open(f.relativepath, 'rb') as fo:
                while chunk := fo.read(self.CHUNK_SIZE):
                    md5.update(chunk)
            hexdigest = md5.hexdigest()
            if hexdigest in hash_dict:
                hash_dict[hexdigest].append(f)
            else:
                hash_dict[hexdigest] = [f]
        results = []
        for hash in [h for h in hash_dict.keys() if len(hash_dict[h]) > 1]:
            results.append(DupesResult(size, hash_dict[hash]))
        return results

    async def find(self) -> List[DupesResult]:
        """Find duplicate files under paths"""
        findfiles = []
        find_sessions = []
        if self.settings.recursive:
            find_sessions.append((True, self.settings.paths.union(self.settings.recurse_dirs)))
        else:
            if self.settings.recurse_dirs:
                find_sessions.append((True, self.settings.recurse_dirs))
            if self.settings.paths:
                find_sessions.append((False, self.settings.paths))
        for s in find_sessions:
            self.settings.recursive = s[0]
            self.settings.paths = s[1]
            findfiles.extend(await self.file_finder.find())
        size_files_dict = {}
        for f in findfiles:
            if f.stat.st_size == 0 and self.settings.noempty:
                continue
            if f.stat.st_size < self.settings.minsize:
                continue
            if self.settings.maxsize > 0 and f.stat.st_size > self.settings.maxsize:
                continue
            if f.stat.st_size not in size_files_dict:
                size_files_dict[f.stat.st_size] = []
            size_files_dict[f.stat.st_size].append(f)
        # filter out size entries if len < 2
        size_files_dict = {k:v for (k,v) in size_files_dict.items() if len(v) > 1}
        sorted_sizes = list(sorted([s for s in size_files_dict.keys()]))

        results = []
        if sorted_sizes:
            if sorted_sizes[0] == 0:
                results.append(DupesResult(0, size_files_dict[0]))
                sorted_sizes = sorted_sizes[1:]
            # do file comparison tasks from largest to smallest
            tasks = []
            for s in reversed(sorted_sizes):
                tasks.append(self.get_dupes(s, size_files_dict[s]))

            results_lists = await asyncio.gather(*tasks)
            for r in results_lists:
                results.extend(r)
            results = list(sorted(results, key=lambda r: r.size))
        return results
