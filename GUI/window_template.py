#!/usr/bin/env python3
# -*- codding: utf-8 -*-

from PyQt5 import QtWidgets

from lib.gen_window import GenericWindow

class Window(GenericWindow):
    def __init__(self, store):
        super().__init__(__name__, store)
        # stuff to do 
