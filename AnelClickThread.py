from PyQt5.QtCore import pyqtSignal, QThread
import numpy as np
import cv2
import time as t
from Anel import Anel

class AnelClickThread(QThread):

    def __init__(self, anel: Anel, port: int, io: bool = False, timeBetweenCommands: float = 0.1):
        self.anel = anel
        self.port = port
        self.io = io
        self.timeBetweenCommands = timeBetweenCommands
        super().__init__()

    def run(self):
        if(self.io):
            self.anel.io_on(self.port)
            t.sleep(self.timeBetweenCommands)
            self.anel.io_off(self.port)
        else:
            self.anel.on(self.port)
            t.sleep(self.timeBetweenCommands)
            self.anel.off(self.port)
