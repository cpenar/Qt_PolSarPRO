#!/usr/bin/env python3
# -*- codding: utf-8 -*-

from logging import warning


def cbManager(function2overload, firstCallback=None):
    """
    Better use this function for easy initialisation than
    the CbManager class

    Example of use:

    Initalisation:
        Note: couldn't avoid to write 2 times the 'function2overload'
        function2overload, manager = cbManager(function2overload)
        or
        func2overload, manager = cbManager(func2overload, firstCallBack)

    Connecting more callbacks:
        manager.connect(anotherCallback)
    """

    cbm = _CbManager(function2overload)
    cbm._activatedOriginalFunction = True
    if firstCallback is not None:
        cbm.connect(firstCallback)
    return cbm._calls, cbm


class _CbManager():
    """
    Qt events doesnt have a connect() method to connect several
    callbacks like signals do.
    This class implements a similar connect() mechanism.
    """

    def __init__(self, function2overload):
        self.callbacks = set()
        self.savedfunc = function2overload

    def removeCallback(self, cb):
        if cb in self.callbacks:
            self.callbacks.remove(cb)
            return True
        else:
            warning(cb.__name__ + " doesnt exist in this callback manager.")
            return False

    def removeAllCallback(self):
        self.callbacks.clear()

    def connect(self, cb):
        if cb in self.callbacks:
            warning(cb.__name__ + " allready connected. Cant add more")
            return False
        else:
            self.callbacks.add(cb)
            return True

    def deactivateOriginalFunction(self):
        self._activatedOriginalFunction = False

    def reactivateOriginalFunction(self):
        self._activatedOriginalFunction = True

    def resetOriginFunction(self):
        """
        usage:
            originalOverloadedFunction = manager.resetOriginFunction()
        Note:
            manager wont be usable after this method !
            so dont do it
        """
        # This line disable most of the methods based on the callbacks
        self.callbacks = None

        return self.originalFunc

    def _calls(self, *args, **kwargs):
        # copy() to avoid error:
        # RuntimeError: Set changed size during iteration
        for cb in self.callbacks.copy():
            cb(*args, **kwargs)
        if self._activatedOriginalFunction:
            return self.savedfunc(*args, **kwargs)
