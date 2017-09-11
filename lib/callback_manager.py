#!/usr/bin/env python3
# -*- codding: utf-8 -*-

from logging import critical, error, warning, info, debug


def cbManager(function2overload, firstCallback):
    """
    Better this function for easy initialisation than
    the CbCallback class

    Example of use:

    Initalisation:
        function2overload, manager = cbManager(function2overload, firstCallBack)

    conencting more callbacks:
        manager.connect(anotherCallback)
    """

    cbm = _CbManager(function2overload)
    cbm.connect(firstCallback)
    cbm._activatedOriginalFunction = True
    return cbm._calls, cbm


class _CbManager():
    """
    Qt events doesnt have a connect() method to connect several
    callback like signals do.
    This class implement that mechanism.
    """

    def __init__(self, function2overload):
        self.callbacks = []
        self.savedfunc = function2overload

    def removeCallback(self, cb):
        if cb in self.callbacks:
            self.callbacks.remove(cb)
            return True
        else:
            warning(cb.__name__ + " doesnt exist in this callback manager.")
            return False

    def removeAllCallback():
        self.callbacks = []

    def connect(self, cb):
        if cb in self.callbacks:
            warning(cb.__name__ + " allready connected. Cant add more")
            return False
        else:
            self.callbacks.append(cb)
            return True

    def deactivateOriginalFunction():
        self._activatedOriginalFunction = False

    def reactivateOriginalFunction():
        self._activatedOriginalFunction = True

    def resetOriginFunction():
        self.callbacks = []
        return self.savedfunc
        
    def _calls(self, *args, **kargs):
        for cb in self.callbacks:
            cb(*args, **kargs)
        if self._activatedOriginalFunction:
            return self.savedfunc(*args, **kargs)
