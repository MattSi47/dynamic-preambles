#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# GNU Radio version: 3.10.1.1

from packaging.version import Version as StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from gnuradio import UConn2402
from gnuradio import blocks
import pmt
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import uhd
import time
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore
from wifi_phy_hier import wifi_phy_hier  # grc-generated hier_block
import ieee802_11



from gnuradio import qtgui

class Test_Wifi_Tx(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "Test_Wifi_Tx")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.tx_gain = tx_gain = .8
        self.samp_rate = samp_rate = 5e6
        self.rx_gain = rx_gain = .8
        self.noise = noise = 0
        self.freq = freq = 5890000000
        self.encoding = encoding = 0
        self.chan_est = chan_est = 0
        self.cfo = cfo = 2e3

        ##################################################
        # Blocks
        ##################################################
        self._cfo_range = Range(0, 50e3, 1000, 2e3, 200)
        self._cfo_win = RangeWidget(self._cfo_range, self.set_cfo, "CFO", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._cfo_win)
        self.wifi_phy_hier_0 = wifi_phy_hier(
            bandwidth=samp_rate,
            chan_est=ieee802_11.Equalizer(chan_est),
            encoding=ieee802_11.Encoding(encoding),
            frequency=freq,
            sensitivity=0.56,
        )
        self.uhd_usrp_sink_0_1_0 = uhd.usrp_sink(
            ",".join(('', "")),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
            "packet_len",
        )
        self.uhd_usrp_sink_0_1_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0_1_0.set_time_now(uhd.time_spec(time.time()), uhd.ALL_MBOARDS)

        self.uhd_usrp_sink_0_1_0.set_center_freq(freq + cfo, 0)
        self.uhd_usrp_sink_0_1_0.set_antenna("TX/RX", 0)
        self.uhd_usrp_sink_0_1_0.set_normalized_gain(tx_gain, 0)
        self._noise_range = Range(0, 2, .1, 0, 200)
        self._noise_win = RangeWidget(self._noise_range, self.set_noise, "Noise Voltage", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._noise_win)
        self.ieee802_11_mac_0 = ieee802_11.mac([0x12, 0x34, 0x56, 0x78, 0x90, 0xab], [0x30, 0x14, 0x4a, 0xe6, 0x46, 0xe4], [0x42, 0x42, 0x42, 0x42, 0x42, 0x42])
        self.blocks_null_source_0 = blocks.null_source(gr.sizeof_gr_complex*1)
        self.blocks_multiply_const_vxx_0_0_0 = blocks.multiply_const_cc(0.1)
        self.blocks_multiply_const_vxx_0_0_0.set_min_output_buffer(100000)
        self.blocks_message_strobe_0 = blocks.message_strobe(pmt.intern("Message"), 100)
        self.UConn2402_StatusMessage_0 = UConn2402.StatusMessage(1000)
        self.UConn2402_Preamble_0 = UConn2402.Preamble('/home/spencer/Documents/SeniorDesign/Git/dynamic-preambles/GNURADIO/Universal Preambles/Preambles/SigSet696_MonteCarlo1k_0.csv', "packet_len")
        self.UConn2402_Preamble_0.set_min_output_buffer(100000)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.UConn2402_StatusMessage_0, 'status'), (self.ieee802_11_mac_0, 'app in'))
        self.msg_connect((self.blocks_message_strobe_0, 'strobe'), (self.UConn2402_StatusMessage_0, 'strobe'))
        self.msg_connect((self.ieee802_11_mac_0, 'phy out'), (self.wifi_phy_hier_0, 'mac_in'))
        self.msg_connect((self.wifi_phy_hier_0, 'mac_out'), (self.ieee802_11_mac_0, 'phy in'))
        self.connect((self.UConn2402_Preamble_0, 0), (self.uhd_usrp_sink_0_1_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0_0, 0), (self.UConn2402_Preamble_0, 0))
        self.connect((self.blocks_null_source_0, 0), (self.wifi_phy_hier_0, 0))
        self.connect((self.wifi_phy_hier_0, 0), (self.blocks_multiply_const_vxx_0_0_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "Test_Wifi_Tx")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_tx_gain(self):
        return self.tx_gain

    def set_tx_gain(self, tx_gain):
        self.tx_gain = tx_gain
        self.uhd_usrp_sink_0_1_0.set_normalized_gain(self.tx_gain, 0)
        self.uhd_usrp_sink_0_1_0.set_normalized_gain(self.tx_gain, 1)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.uhd_usrp_sink_0_1_0.set_samp_rate(self.samp_rate)
        self.wifi_phy_hier_0.set_bandwidth(self.samp_rate)

    def get_rx_gain(self):
        return self.rx_gain

    def set_rx_gain(self, rx_gain):
        self.rx_gain = rx_gain

    def get_noise(self):
        return self.noise

    def set_noise(self, noise):
        self.noise = noise

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.uhd_usrp_sink_0_1_0.set_center_freq(self.freq + self.cfo, 0)
        self.uhd_usrp_sink_0_1_0.set_center_freq(self.freq, 1)
        self.wifi_phy_hier_0.set_frequency(self.freq)

    def get_encoding(self):
        return self.encoding

    def set_encoding(self, encoding):
        self.encoding = encoding
        self.wifi_phy_hier_0.set_encoding(ieee802_11.Encoding(self.encoding))

    def get_chan_est(self):
        return self.chan_est

    def set_chan_est(self, chan_est):
        self.chan_est = chan_est
        self.wifi_phy_hier_0.set_chan_est(ieee802_11.Equalizer(self.chan_est))

    def get_cfo(self):
        return self.cfo

    def set_cfo(self, cfo):
        self.cfo = cfo
        self.uhd_usrp_sink_0_1_0.set_center_freq(self.freq + self.cfo, 0)




def main(top_block_cls=Test_Wifi_Tx, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
