#!/usr/bin/env python3
# -*- codding: utf-8 -*-

from logging import critical, error, warning, info, debug


class CbManager():
    def __init__(self):
        self.replacers = []

    def removeCallbackFromReplacer(self, replacer, cb):
        if cb in replacer['callbacks']:
            replacer['callbacks'].remove(cb)
        else:
            warning(cb.__name__ + " doesnt exist in " +
                    replacer['oldfunc'].__name__ + " replacer")

    def addCallback(self, oldfunc, cb):
        # do we allready have a replacer for that func ?
        for replacer in self.replacers:
            if replacer['newfunc'] is oldfunc:
                replacer['callbacks'].append(cb)
                return replacer['newfunc'], replacer

        # we didnt find any replacer for that oldfunc
        # we create a new one
        replacer = {}
        replacer['callbacks'] = [cb]
        replacer['oldfunc'] = oldfunc
        replacer['newfunc'] = lambda *args, **kargs: (
                self.calls(replacer, *args, **kargs))
        oldfunc = replacer['newfunc']
        self.replacers.append(replacer)
        return replacer['newfunc'], replacer

    def calls(self, replacer, *args, **kargs):
        for cb in replacer['callbacks']:
            cb(*args, **kargs)
        replacer['oldfunc'](*args, **kargs)
