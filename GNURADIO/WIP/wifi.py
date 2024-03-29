#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Wifi
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

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import UConn2402
from gnuradio import blocks
import pmt
from gnuradio import gr
from gnuradio.fft import window
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import network
from gnuradio import uhd
import time
from wifi_phy_hier import wifi_phy_hier  # grc-generated hier_block
import ieee802_11



from gnuradio import qtgui

class wifi(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Wifi", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Wifi")
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

        self.settings = Qt.QSettings("GNU Radio", "wifi")

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
        self.freq = freq = 5890000000
        self.encoding = encoding = 0
        self.chan_est = chan_est = 0

        ##################################################
        # Blocks
        ##################################################
        self.Messaging = Qt.QTabWidget()
        self.Messaging_widget_0 = Qt.QWidget()
        self.Messaging_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.Messaging_widget_0)
        self.Messaging_grid_layout_0 = Qt.QGridLayout()
        self.Messaging_layout_0.addLayout(self.Messaging_grid_layout_0)
        self.Messaging.addTab(self.Messaging_widget_0, 'Device 1')
        self.Messaging_widget_1 = Qt.QWidget()
        self.Messaging_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.Messaging_widget_1)
        self.Messaging_grid_layout_1 = Qt.QGridLayout()
        self.Messaging_layout_1.addLayout(self.Messaging_grid_layout_1)
        self.Messaging.addTab(self.Messaging_widget_1, 'Device 2')
        self.top_layout.addWidget(self.Messaging)
        self.wifi_phy_hier_0_0 = wifi_phy_hier(
            bandwidth=samp_rate,
            chan_est=ieee802_11.Equalizer(chan_est),
            encoding=ieee802_11.Encoding(encoding),
            frequency=freq,
            sensitivity=0.56,
        )
        self.wifi_phy_hier_0 = wifi_phy_hier(
            bandwidth=samp_rate,
            chan_est=ieee802_11.Equalizer(chan_est),
            encoding=ieee802_11.Encoding(encoding),
            frequency=freq,
            sensitivity=0.56,
        )
        self.uhd_usrp_source_0 = uhd.usrp_source(
            ",".join(('', "")),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,2)),
            ),
        )
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_time_now(uhd.time_spec(time.time()), uhd.ALL_MBOARDS)

        self.uhd_usrp_source_0.set_center_freq(freq, 0)
        self.uhd_usrp_source_0.set_antenna("RX2", 0)
        self.uhd_usrp_source_0.set_normalized_gain(rx_gain, 0)

        self.uhd_usrp_source_0.set_center_freq(freq, 1)
        self.uhd_usrp_source_0.set_antenna("RX2", 1)
        self.uhd_usrp_source_0.set_normalized_gain(rx_gain, 1)
        self.uhd_usrp_sink_0_1_0 = uhd.usrp_sink(
            ",".join(('', "")),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,2)),
            ),
            "packet_len",
        )
        self.uhd_usrp_sink_0_1_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0_1_0.set_time_now(uhd.time_spec(time.time()), uhd.ALL_MBOARDS)

        self.uhd_usrp_sink_0_1_0.set_center_freq(freq, 0)
        self.uhd_usrp_sink_0_1_0.set_antenna("TX/RX", 0)
        self.uhd_usrp_sink_0_1_0.set_normalized_gain(tx_gain, 0)

        self.uhd_usrp_sink_0_1_0.set_center_freq(freq, 1)
        self.uhd_usrp_sink_0_1_0.set_antenna("TX/RX", 1)
        self.uhd_usrp_sink_0_1_0.set_normalized_gain(tx_gain, 1)
        self.uhd_usrp_sink_0_1 = uhd.usrp_sink(
            ",".join(('', "")),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,2)),
            ),
            "packet_len",
        )
        self.uhd_usrp_sink_0_1.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0_1.set_time_now(uhd.time_spec(time.time()), uhd.ALL_MBOARDS)

        self.uhd_usrp_sink_0_1.set_center_freq(freq, 0)
        self.uhd_usrp_sink_0_1.set_antenna("TX/RX", 0)
        self.uhd_usrp_sink_0_1.set_normalized_gain(tx_gain, 0)

        self.uhd_usrp_sink_0_1.set_center_freq(freq, 1)
        self.uhd_usrp_sink_0_1.set_antenna("TX/RX", 1)
        self.uhd_usrp_sink_0_1.set_normalized_gain(tx_gain, 1)
        self.qtgui_time_sink_x_1_0_0_0 = qtgui.time_sink_f(
            1024, #size
            5000000, #samp_rate
            "Correlation", #name
            2, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_1_0_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_1_0_0_0.set_y_axis(-.1, 1.1)

        self.qtgui_time_sink_x_1_0_0_0.set_y_label('', "")

        self.qtgui_time_sink_x_1_0_0_0.enable_tags(True)
        self.qtgui_time_sink_x_1_0_0_0.set_trigger_mode(qtgui.TRIG_MODE_NORM, qtgui.TRIG_SLOPE_POS, .8, .000040, 1, "")
        self.qtgui_time_sink_x_1_0_0_0.enable_autoscale(False)
        self.qtgui_time_sink_x_1_0_0_0.enable_grid(False)
        self.qtgui_time_sink_x_1_0_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_1_0_0_0.enable_control_panel(False)
        self.qtgui_time_sink_x_1_0_0_0.enable_stem_plot(False)


        labels = ['Up Chirp', 'Down Chirp', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_1_0_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_1_0_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_1_0_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_1_0_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_1_0_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_1_0_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_1_0_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_1_0_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_1_0_0_0.qwidget(), Qt.QWidget)
        self.Messaging_grid_layout_1.addWidget(self._qtgui_time_sink_x_1_0_0_0_win, 1, 0, 1, 1)
        for r in range(1, 2):
            self.Messaging_grid_layout_1.setRowStretch(r, 1)
        for c in range(0, 1):
            self.Messaging_grid_layout_1.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_1_0_0 = qtgui.time_sink_f(
            1024, #size
            5000000, #samp_rate
            "Correlation", #name
            2, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_1_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_1_0_0.set_y_axis(-.1, 1.1)

        self.qtgui_time_sink_x_1_0_0.set_y_label('', "")

        self.qtgui_time_sink_x_1_0_0.enable_tags(True)
        self.qtgui_time_sink_x_1_0_0.set_trigger_mode(qtgui.TRIG_MODE_NORM, qtgui.TRIG_SLOPE_POS, .8, .000040, 1, "")
        self.qtgui_time_sink_x_1_0_0.enable_autoscale(False)
        self.qtgui_time_sink_x_1_0_0.enable_grid(False)
        self.qtgui_time_sink_x_1_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_1_0_0.enable_control_panel(False)
        self.qtgui_time_sink_x_1_0_0.enable_stem_plot(False)


        labels = ['Up Chirp', 'Down Chirp', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_1_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_1_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_1_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_1_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_1_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_1_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_1_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_1_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_1_0_0.qwidget(), Qt.QWidget)
        self.Messaging_grid_layout_0.addWidget(self._qtgui_time_sink_x_1_0_0_win, 1, 0, 1, 1)
        for r in range(1, 2):
            self.Messaging_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 1):
            self.Messaging_grid_layout_0.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_0_0_1_0 = qtgui.time_sink_c(
            1024, #size
            5e6, #samp_rate
            "Packet", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0_0_1_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0_0_1_0.set_y_axis(-1.5, 1.5)

        self.qtgui_time_sink_x_0_0_1_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_0_1_0.enable_tags(True)
        self.qtgui_time_sink_x_0_0_1_0.set_trigger_mode(qtgui.TRIG_MODE_TAG, qtgui.TRIG_SLOPE_POS, 0.0, .000020, 0, "packet_len")
        self.qtgui_time_sink_x_0_0_1_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0_0_1_0.enable_grid(False)
        self.qtgui_time_sink_x_0_0_1_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0_1_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0_0_1_0.enable_stem_plot(False)


        labels = ['I', 'Q', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['black', 'magenta', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.qtgui_time_sink_x_0_0_1_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0_0_1_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0_0_1_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0_1_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0_1_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0_1_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0_1_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0_1_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_1_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0_1_0.qwidget(), Qt.QWidget)
        self.Messaging_grid_layout_1.addWidget(self._qtgui_time_sink_x_0_0_1_0_win, 2, 0, 1, 1)
        for r in range(2, 3):
            self.Messaging_grid_layout_1.setRowStretch(r, 1)
        for c in range(0, 1):
            self.Messaging_grid_layout_1.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_0_0_1 = qtgui.time_sink_c(
            1024, #size
            5e6, #samp_rate
            "Packet", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0_0_1.set_update_time(0.10)
        self.qtgui_time_sink_x_0_0_1.set_y_axis(-1.5, 1.5)

        self.qtgui_time_sink_x_0_0_1.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_0_1.enable_tags(True)
        self.qtgui_time_sink_x_0_0_1.set_trigger_mode(qtgui.TRIG_MODE_TAG, qtgui.TRIG_SLOPE_POS, 0.0, .000020, 0, "packet_len")
        self.qtgui_time_sink_x_0_0_1.enable_autoscale(False)
        self.qtgui_time_sink_x_0_0_1.enable_grid(False)
        self.qtgui_time_sink_x_0_0_1.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0_1.enable_control_panel(False)
        self.qtgui_time_sink_x_0_0_1.enable_stem_plot(False)


        labels = ['I', 'Q', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['black', 'magenta', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.qtgui_time_sink_x_0_0_1.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0_0_1.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0_0_1.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0_1.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0_1.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0_1.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0_1.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0_1.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_1_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0_1.qwidget(), Qt.QWidget)
        self.Messaging_grid_layout_0.addWidget(self._qtgui_time_sink_x_0_0_1_win, 2, 0, 1, 1)
        for r in range(2, 3):
            self.Messaging_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 1):
            self.Messaging_grid_layout_0.setColumnStretch(c, 1)
        self.qtgui_edit_box_msg_0_0 = qtgui.edit_box_msg(qtgui.STRING, '', 'Send Wifi Message (RF1)', False, True, 'pressed', None)
        self._qtgui_edit_box_msg_0_0_win = sip.wrapinstance(self.qtgui_edit_box_msg_0_0.qwidget(), Qt.QWidget)
        self.Messaging_grid_layout_1.addWidget(self._qtgui_edit_box_msg_0_0_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.Messaging_grid_layout_1.setRowStretch(r, 1)
        for c in range(0, 1):
            self.Messaging_grid_layout_1.setColumnStretch(c, 1)
        self.qtgui_edit_box_msg_0 = qtgui.edit_box_msg(qtgui.STRING, '', 'Send Wifi Message (RF0)', False, True, 'pressed', None)
        self._qtgui_edit_box_msg_0_win = sip.wrapinstance(self.qtgui_edit_box_msg_0.qwidget(), Qt.QWidget)
        self.Messaging_grid_layout_0.addWidget(self._qtgui_edit_box_msg_0_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.Messaging_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 1):
            self.Messaging_grid_layout_0.setColumnStretch(c, 1)
        self.network_socket_pdu_0_0_0 = network.socket_pdu('UDP_CLIENT', '127.0.0.1', '52002', 10000, False)
        self.network_socket_pdu_0_0 = network.socket_pdu('UDP_CLIENT', '127.0.0.1', '52001', 10000, False)
        self.ieee802_11_mac_0_0 = ieee802_11.mac([0x12, 0x34, 0x56, 0x78, 0x90, 0xab], [0x30, 0x14, 0x4a, 0xe6, 0x46, 0xe4], [0x42, 0x42, 0x42, 0x42, 0x42, 0x42])
        self.ieee802_11_mac_0 = ieee802_11.mac([0x12, 0x34, 0x56, 0x78, 0x90, 0xab], [0x30, 0x14, 0x4a, 0xe6, 0x46, 0xe4], [0x42, 0x42, 0x42, 0x42, 0x42, 0x42])
        self.blocks_multiply_const_vxx_1_0 = blocks.multiply_const_cc(0)
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_cc(0)
        self.blocks_multiply_const_vxx_0_0_0 = blocks.multiply_const_cc(0.2)
        self.blocks_multiply_const_vxx_0_0_0.set_min_output_buffer(100000)
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_cc(0.2)
        self.blocks_multiply_const_vxx_0_0.set_min_output_buffer(100000)
        self.blocks_message_strobe_random_0_0 = blocks.message_strobe_random(pmt.intern("Wifi-Device2"), blocks.STROBE_POISSON, 3000, 3000)
        self.blocks_message_strobe_random_0 = blocks.message_strobe_random(pmt.intern("Wifi-Device1"), blocks.STROBE_POISSON, 3000, 3000)
        self.UConn2402_StatusMessage_0_0 = UConn2402.StatusMessage(0)
        self.UConn2402_StatusMessage_0 = UConn2402.StatusMessage(0)
        self.UConn2402_LFMChirpXCorr_0_0 = UConn2402.LFMChirpXCorr(5000000, 2000000, .000040)
        self.UConn2402_LFMChirpXCorr_0 = UConn2402.LFMChirpXCorr(5000000, 2000000, .000040)
        self.UConn2402_GUIMessagePrefixer_0_0 = UConn2402.GUIMessagePrefixer('Wifi-Device2: ')
        self.UConn2402_GUIMessagePrefixer_0 = UConn2402.GUIMessagePrefixer('Wifi-Device1: ')
        self.UConn2402_Chirp_0_0 = UConn2402.Chirp(5000000, 2000000, .000040, 0, "packet_len")
        self.UConn2402_Chirp_0_0.set_min_output_buffer(100000)
        self.UConn2402_Chirp_0 = UConn2402.Chirp(5000000, 2000000, .000040, 0, "packet_len")
        self.UConn2402_Chirp_0.set_min_output_buffer(100000)
        self.UConn2402_ArbitrarySync2_0_0 = UConn2402.ArbitrarySync2(0.8, 20000)
        self.UConn2402_ArbitrarySync2_0 = UConn2402.ArbitrarySync2(0.8, 20000)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.UConn2402_GUIMessagePrefixer_0, 'msg_out'), (self.ieee802_11_mac_0, 'app in'))
        self.msg_connect((self.UConn2402_GUIMessagePrefixer_0, 'clear'), (self.qtgui_edit_box_msg_0, 'val'))
        self.msg_connect((self.UConn2402_GUIMessagePrefixer_0_0, 'msg_out'), (self.ieee802_11_mac_0_0, 'app in'))
        self.msg_connect((self.UConn2402_GUIMessagePrefixer_0_0, 'clear'), (self.qtgui_edit_box_msg_0_0, 'val'))
        self.msg_connect((self.UConn2402_StatusMessage_0, 'status'), (self.ieee802_11_mac_0, 'app in'))
        self.msg_connect((self.UConn2402_StatusMessage_0_0, 'status'), (self.ieee802_11_mac_0_0, 'app in'))
        self.msg_connect((self.blocks_message_strobe_random_0, 'strobe'), (self.UConn2402_StatusMessage_0, 'strobe'))
        self.msg_connect((self.blocks_message_strobe_random_0_0, 'strobe'), (self.UConn2402_StatusMessage_0_0, 'strobe'))
        self.msg_connect((self.ieee802_11_mac_0, 'app out'), (self.UConn2402_ArbitrarySync2_0, 'stop'))
        self.msg_connect((self.ieee802_11_mac_0, 'app out'), (self.network_socket_pdu_0_0, 'pdus'))
        self.msg_connect((self.ieee802_11_mac_0, 'phy out'), (self.wifi_phy_hier_0, 'mac_in'))
        self.msg_connect((self.ieee802_11_mac_0_0, 'app out'), (self.UConn2402_ArbitrarySync2_0_0, 'stop'))
        self.msg_connect((self.ieee802_11_mac_0_0, 'app out'), (self.network_socket_pdu_0_0_0, 'pdus'))
        self.msg_connect((self.ieee802_11_mac_0_0, 'phy out'), (self.wifi_phy_hier_0_0, 'mac_in'))
        self.msg_connect((self.qtgui_edit_box_msg_0, 'msg'), (self.UConn2402_GUIMessagePrefixer_0, 'msg_in'))
        self.msg_connect((self.qtgui_edit_box_msg_0_0, 'msg'), (self.UConn2402_GUIMessagePrefixer_0_0, 'msg_in'))
        self.msg_connect((self.wifi_phy_hier_0, 'mac_out'), (self.ieee802_11_mac_0, 'phy in'))
        self.msg_connect((self.wifi_phy_hier_0_0, 'mac_out'), (self.ieee802_11_mac_0_0, 'phy in'))
        self.connect((self.UConn2402_ArbitrarySync2_0, 0), (self.wifi_phy_hier_0, 0))
        self.connect((self.UConn2402_ArbitrarySync2_0_0, 0), (self.wifi_phy_hier_0_0, 0))
        self.connect((self.UConn2402_Chirp_0, 0), (self.blocks_multiply_const_vxx_0_0_0, 0))
        self.connect((self.UConn2402_Chirp_0, 0), (self.blocks_multiply_const_vxx_1_0, 0))
        self.connect((self.UConn2402_Chirp_0_0, 0), (self.blocks_multiply_const_vxx_0_0, 0))
        self.connect((self.UConn2402_Chirp_0_0, 0), (self.blocks_multiply_const_vxx_1, 0))
        self.connect((self.UConn2402_LFMChirpXCorr_0, 1), (self.UConn2402_ArbitrarySync2_0, 1))
        self.connect((self.UConn2402_LFMChirpXCorr_0, 1), (self.qtgui_time_sink_x_1_0_0, 1))
        self.connect((self.UConn2402_LFMChirpXCorr_0, 0), (self.qtgui_time_sink_x_1_0_0, 0))
        self.connect((self.UConn2402_LFMChirpXCorr_0_0, 1), (self.UConn2402_ArbitrarySync2_0_0, 1))
        self.connect((self.UConn2402_LFMChirpXCorr_0_0, 1), (self.qtgui_time_sink_x_1_0_0_0, 1))
        self.connect((self.UConn2402_LFMChirpXCorr_0_0, 0), (self.qtgui_time_sink_x_1_0_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.uhd_usrp_sink_0_1, 1))
        self.connect((self.blocks_multiply_const_vxx_0_0_0, 0), (self.uhd_usrp_sink_0_1_0, 0))
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.uhd_usrp_sink_0_1, 0))
        self.connect((self.blocks_multiply_const_vxx_1_0, 0), (self.uhd_usrp_sink_0_1_0, 1))
        self.connect((self.uhd_usrp_source_0, 0), (self.UConn2402_ArbitrarySync2_0, 0))
        self.connect((self.uhd_usrp_source_0, 1), (self.UConn2402_ArbitrarySync2_0_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.UConn2402_LFMChirpXCorr_0, 0))
        self.connect((self.uhd_usrp_source_0, 1), (self.UConn2402_LFMChirpXCorr_0_0, 0))
        self.connect((self.wifi_phy_hier_0, 0), (self.UConn2402_Chirp_0, 0))
        self.connect((self.wifi_phy_hier_0, 0), (self.qtgui_time_sink_x_0_0_1, 0))
        self.connect((self.wifi_phy_hier_0_0, 0), (self.UConn2402_Chirp_0_0, 0))
        self.connect((self.wifi_phy_hier_0_0, 0), (self.qtgui_time_sink_x_0_0_1_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "wifi")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_tx_gain(self):
        return self.tx_gain

    def set_tx_gain(self, tx_gain):
        self.tx_gain = tx_gain
        self.uhd_usrp_sink_0_1.set_normalized_gain(self.tx_gain, 0)
        self.uhd_usrp_sink_0_1.set_normalized_gain(self.tx_gain, 1)
        self.uhd_usrp_sink_0_1_0.set_normalized_gain(self.tx_gain, 0)
        self.uhd_usrp_sink_0_1_0.set_normalized_gain(self.tx_gain, 1)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.uhd_usrp_sink_0_1.set_samp_rate(self.samp_rate)
        self.uhd_usrp_sink_0_1_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)
        self.wifi_phy_hier_0.set_bandwidth(self.samp_rate)
        self.wifi_phy_hier_0_0.set_bandwidth(self.samp_rate)

    def get_rx_gain(self):
        return self.rx_gain

    def set_rx_gain(self, rx_gain):
        self.rx_gain = rx_gain
        self.uhd_usrp_source_0.set_normalized_gain(self.rx_gain, 0)
        self.uhd_usrp_source_0.set_normalized_gain(self.rx_gain, 1)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.uhd_usrp_sink_0_1.set_center_freq(self.freq, 0)
        self.uhd_usrp_sink_0_1.set_center_freq(self.freq, 1)
        self.uhd_usrp_sink_0_1_0.set_center_freq(self.freq, 0)
        self.uhd_usrp_sink_0_1_0.set_center_freq(self.freq, 1)
        self.uhd_usrp_source_0.set_center_freq(self.freq, 0)
        self.uhd_usrp_source_0.set_center_freq(self.freq, 1)
        self.wifi_phy_hier_0.set_frequency(self.freq)
        self.wifi_phy_hier_0_0.set_frequency(self.freq)

    def get_encoding(self):
        return self.encoding

    def set_encoding(self, encoding):
        self.encoding = encoding
        self.wifi_phy_hier_0.set_encoding(ieee802_11.Encoding(self.encoding))
        self.wifi_phy_hier_0_0.set_encoding(ieee802_11.Encoding(self.encoding))

    def get_chan_est(self):
        return self.chan_est

    def set_chan_est(self, chan_est):
        self.chan_est = chan_est
        self.wifi_phy_hier_0.set_chan_est(ieee802_11.Equalizer(self.chan_est))
        self.wifi_phy_hier_0_0.set_chan_est(ieee802_11.Equalizer(self.chan_est))




def main(top_block_cls=wifi, options=None):

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
