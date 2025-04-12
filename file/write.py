#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# https://docs.python.org/3.4/tutorial/inputoutput.html#reading-and-writing-files
# http://pythonworld.ru/tipy-dannyx-v-python/fajly-rabota-s-fajlami.html


# Открыть файл в режиме записи
with open("foo.txt", mode="w", encoding="utf-8") as f:
    f.write("123\n")
    f.write("one two\n")
    f.write("one two\n")
    f.write("раз два\n")
