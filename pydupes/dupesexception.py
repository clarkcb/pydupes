# -*- coding: utf-8 -*-
###############################################################################
#
# dupesexception.py
#
# class DupesException: custom exception
#
###############################################################################
class DupesException(Exception):
    def __init__(self, *args):
        Exception.__init__(self, *args)
