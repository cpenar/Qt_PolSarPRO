#!/usr/bin/env python3
# -*- codding: utf-8 -*-

from lib.store_window import StoreWindow


class Window(StoreWindow):
    def __init__(self, store):
        super().__init__(__name__, store)
        # stuff to do
