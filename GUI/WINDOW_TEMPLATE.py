#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from lib.store_window import StoreWindow


class Window(StoreWindow):
    def __init__(self, store, **kwargs):
        super().__init__(__name__, store)
        # stuff to do
