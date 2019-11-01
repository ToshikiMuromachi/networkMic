#
# g`ÌA^Cvbg
#

# !/usr/local/bin/python3
# -*- coding:utf-8 -*-

import numpy as np
import sys

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui

import pyaudio

np.set_printoptions(threshold=np.inf)

sample_rate = 44100
frame_length = 1024
frame_shift = 80


class PlotWindow:
    def __init__(self):
        self.win = pg.GraphicsWindow()
        self.win.setWindowTitle("g`ÌA^Cvbg")
        self.win.resize(1100, 800)
        self.plt = self.win.addPlot()  # vbgÌrWAÖW
        self.ymin = -100
        self.ymax = 80
        self.plt.setYRange(-1.0, 1.0)  # y²ÌãÀAºÀÌÝè
        self.curve = self.plt.plot()  # vbgf[^ðüêéê

        # }CNÝè
        self.CHUNK = frame_length  # 1xÉÇÝæé¹ºÌf[^
        self.RATE = sample_rate  # TvOüg
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=pyaudio.paInt16,
                                      channels=1,
                                      rate=self.RATE,
                                      input=True,
                                      output=True,
                                      frames_per_buffer=self.CHUNK)

        # Abvf[gÔÝè
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(5)

        self.data = np.zeros(self.CHUNK)

    def update(self):
        self.data = self.AudioInput()
        self.curve.setData(self.data)

    def AudioInput(self):
        ret = self.stream.read(self.CHUNK)
        ret = np.frombuffer(ret, dtype="int16") / 32768
        print(ret)
        return ret


if __name__ == "__main__":
    plotwin = PlotWindow()

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
