#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import threading
import time

from PyQt5.Qt import QMainWindow, QLabel, QFont, QApplication, Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont('Courier', 25))

        def loop():
            i = 0

            while True:
                self.label.setText(str(i))

                i += 1
                time.sleep(1)

        thread = threading.Thread(target=loop)
        thread.start()

        self.setCentralWidget(self.label)


app = QApplication([])

mw = MainWindow()
mw.show()

app.exec()
