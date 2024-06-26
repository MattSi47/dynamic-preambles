#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: AP Control
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
from PyQt5.QtCore import QObject, pyqtSlot
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import UConn2402
from gnuradio import blocks
from gnuradio import filter
from gnuradio import gr
from gnuradio.fft import window
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import network
from gnuradio import uhd
import time
from ieee802_15_4_oqpsk_phy import ieee802_15_4_oqpsk_phy  # grc-generated hier_block
from wifi_phy_hier import wifi_phy_hier  # grc-generated hier_block
import ieee802_11
import ieee802_15_4



from gnuradio import qtgui

class AP(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "AP Control", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("AP Control")
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

        self.settings = Qt.QSettings("GNU Radio", "AP")

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
        self.filepath_zigbee = filepath_zigbee = '/home/spencer/Documents/SeniorDesign/Git/dynamic-preambles/GNURADIO/Universal Preambles/Preambles/SigSet696_MonteCarlo1k_3.csv'
        self.filepath_wifi = filepath_wifi = '/home/spencer/Documents/SeniorDesign/Git/dynamic-preambles/GNURADIO/Universal Preambles/Preambles/SigSet696_MonteCarlo1k_0.csv'
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
        self.Messaging.addTab(self.Messaging_widget_0, 'Packet Messaging (press ENTER)')
        self.top_layout.addWidget(self.Messaging)
        self.graph = Qt.QTabWidget()
        self.graph_widget_0 = Qt.QWidget()
        self.graph_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.graph_widget_0)
        self.graph_grid_layout_0 = Qt.QGridLayout()
        self.graph_layout_0.addLayout(self.graph_grid_layout_0)
        self.graph.addTab(self.graph_widget_0, 'Wifi')
        self.graph_widget_1 = Qt.QWidget()
        self.graph_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.graph_widget_1)
        self.graph_grid_layout_1 = Qt.QGridLayout()
        self.graph_layout_1.addLayout(self.graph_grid_layout_1)
        self.graph.addTab(self.graph_widget_1, 'Zigbee')
        self.top_layout.addWidget(self.graph)
        # Create the options list
        self._filepath_zigbee_options = ['/home/spencer/Documents/SeniorDesign/Git/dynamic-preambles/GNURADIO/Universal Preambles/Preambles/SigSet696_MonteCarlo1k_3.csv', '/home/spencer/Documents/SeniorDesign/Git/dynamic-preambles/GNURADIO/Universal Preambles/Preambles/SigSet696_MonteCarlo1k_4.csv']
        # Create the labels list
        self._filepath_zigbee_labels = ['Preamble 4', 'Preamble 5']
        # Create the combo box
        # Create the radio buttons
        self._filepath_zigbee_group_box = Qt.QGroupBox("Preamble (Tx Only)" + ": ")
        self._filepath_zigbee_box = Qt.QHBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._filepath_zigbee_button_group = variable_chooser_button_group()
        self._filepath_zigbee_group_box.setLayout(self._filepath_zigbee_box)
        for i, _label in enumerate(self._filepath_zigbee_labels):
            radio_button = Qt.QRadioButton(_label)
            self._filepath_zigbee_box.addWidget(radio_button)
            self._filepath_zigbee_button_group.addButton(radio_button, i)
        self._filepath_zigbee_callback = lambda i: Qt.QMetaObject.invokeMethod(self._filepath_zigbee_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._filepath_zigbee_options.index(i)))
        self._filepath_zigbee_callback(self.filepath_zigbee)
        self._filepath_zigbee_button_group.buttonClicked[int].connect(
            lambda i: self.set_filepath_zigbee(self._filepath_zigbee_options[i]))
        self.Messaging_grid_layout_0.addWidget(self._filepath_zigbee_group_box, 1, 1, 1, 1)
        for r in range(1, 2):
            self.Messaging_grid_layout_0.setRowStretch(r, 1)
        for c in range(1, 2):
            self.Messaging_grid_layout_0.setColumnStretch(c, 1)
        # Create the options list
        self._filepath_wifi_options = ['/home/spencer/Documents/SeniorDesign/Git/dynamic-preambles/GNURADIO/Universal Preambles/Preambles/SigSet696_MonteCarlo1k_0.csv', '/home/spencer/Documents/SeniorDesign/Git/dynamic-preambles/GNURADIO/Universal Preambles/Preambles/SigSet696_MonteCarlo1k_1.csv', '/home/spencer/Documents/SeniorDesign/Git/dynamic-preambles/GNURADIO/Universal Preambles/Preambles/SigSet696_MonteCarlo1k_2.csv']
        # Create the labels list
        self._filepath_wifi_labels = ['Preamble 1', 'Preamble 2', 'Preamble 3']
        # Create the combo box
        # Create the radio buttons
        self._filepath_wifi_group_box = Qt.QGroupBox("Preamble (Tx Only)" + ": ")
        self._filepath_wifi_box = Qt.QHBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._filepath_wifi_button_group = variable_chooser_button_group()
        self._filepath_wifi_group_box.setLayout(self._filepath_wifi_box)
        for i, _label in enumerate(self._filepath_wifi_labels):
            radio_button = Qt.QRadioButton(_label)
            self._filepath_wifi_box.addWidget(radio_button)
            self._filepath_wifi_button_group.addButton(radio_button, i)
        self._filepath_wifi_callback = lambda i: Qt.QMetaObject.invokeMethod(self._filepath_wifi_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._filepath_wifi_options.index(i)))
        self._filepath_wifi_callback(self.filepath_wifi)
        self._filepath_wifi_button_group.buttonClicked[int].connect(
            lambda i: self.set_filepath_wifi(self._filepath_wifi_options[i]))
        self.Messaging_grid_layout_0.addWidget(self._filepath_wifi_group_box, 1, 0, 1, 1)
        for r in range(1, 2):
            self.Messaging_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 1):
            self.Messaging_grid_layout_0.setColumnStretch(c, 1)
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
                channels=list(range(0,1)),
            ),
        )
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_time_now(uhd.time_spec(time.time()), uhd.ALL_MBOARDS)

        self.uhd_usrp_source_0.set_center_freq(freq, 0)
        self.uhd_usrp_source_0.set_normalized_gain(rx_gain, 0)
        self.uhd_usrp_sink_0_0 = uhd.usrp_sink(
            ",".join(('', "")),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
            'packet_len',
        )
        self.uhd_usrp_sink_0_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0_0.set_time_now(uhd.time_spec(time.time()), uhd.ALL_MBOARDS)

        self.uhd_usrp_sink_0_0.set_center_freq(freq, 0)
        self.uhd_usrp_sink_0_0.set_normalized_gain(tx_gain, 0)
        self.uhd_usrp_sink_0_0.set_min_output_buffer(415488)
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
            ",".join(('', "")),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
            'packet_len',
        )
        self.uhd_usrp_sink_0.set_samp_rate(5e6)
        self.uhd_usrp_sink_0.set_time_now(uhd.time_spec(time.time()), uhd.ALL_MBOARDS)

        self.uhd_usrp_sink_0.set_center_freq(freq, 0)
        self.uhd_usrp_sink_0.set_normalized_gain(tx_gain, 0)
        self.uhd_usrp_sink_0.set_min_output_buffer(65536)
        self.rational_resampler_xxx_1 = filter.rational_resampler_ccc(
                interpolation=5,
                decimation=4,
                taps=[],
                fractional_bw=0)
        self.rational_resampler_xxx_1.set_min_output_buffer(65536)
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccf(
                interpolation=4,
                decimation=5,
                taps=[],
                fractional_bw=0)
        self.qtgui_time_sink_x_1_0_0_1_0 = qtgui.time_sink_f(
            1024, #size
            5000000, #samp_rate
            "Preamble 5 Correlation (Rx)", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_1_0_0_1_0.set_update_time(0.10)
        self.qtgui_time_sink_x_1_0_0_1_0.set_y_axis(-.1, 1.1)

        self.qtgui_time_sink_x_1_0_0_1_0.set_y_label('', "")

        self.qtgui_time_sink_x_1_0_0_1_0.enable_tags(True)
        self.qtgui_time_sink_x_1_0_0_1_0.set_trigger_mode(qtgui.TRIG_MODE_NORM, qtgui.TRIG_SLOPE_POS, .8, .000040, 0, "")
        self.qtgui_time_sink_x_1_0_0_1_0.enable_autoscale(False)
        self.qtgui_time_sink_x_1_0_0_1_0.enable_grid(False)
        self.qtgui_time_sink_x_1_0_0_1_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_1_0_0_1_0.enable_control_panel(False)
        self.qtgui_time_sink_x_1_0_0_1_0.enable_stem_plot(False)

        self.qtgui_time_sink_x_1_0_0_1_0.disable_legend()

        labels = ['Preamble 1', 'Down Chirp', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['cyan', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [0, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_1_0_0_1_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_1_0_0_1_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_1_0_0_1_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_1_0_0_1_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_1_0_0_1_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_1_0_0_1_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_1_0_0_1_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_1_0_0_1_0_win = sip.wrapinstance(self.qtgui_time_sink_x_1_0_0_1_0.qwidget(), Qt.QWidget)
        self.graph_grid_layout_1.addWidget(self._qtgui_time_sink_x_1_0_0_1_0_win, 0, 1, 1, 1)
        for r in range(0, 1):
            self.graph_grid_layout_1.setRowStretch(r, 1)
        for c in range(1, 2):
            self.graph_grid_layout_1.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_1_0_0_1 = qtgui.time_sink_f(
            1024, #size
            5000000, #samp_rate
            "Preamble 4 Correlation (Rx)", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_1_0_0_1.set_update_time(0.10)
        self.qtgui_time_sink_x_1_0_0_1.set_y_axis(-.1, 1.1)

        self.qtgui_time_sink_x_1_0_0_1.set_y_label('', "")

        self.qtgui_time_sink_x_1_0_0_1.enable_tags(True)
        self.qtgui_time_sink_x_1_0_0_1.set_trigger_mode(qtgui.TRIG_MODE_NORM, qtgui.TRIG_SLOPE_POS, .8, .000040, 0, "")
        self.qtgui_time_sink_x_1_0_0_1.enable_autoscale(False)
        self.qtgui_time_sink_x_1_0_0_1.enable_grid(False)
        self.qtgui_time_sink_x_1_0_0_1.enable_axis_labels(True)
        self.qtgui_time_sink_x_1_0_0_1.enable_control_panel(False)
        self.qtgui_time_sink_x_1_0_0_1.enable_stem_plot(False)

        self.qtgui_time_sink_x_1_0_0_1.disable_legend()

        labels = ['Preamble 1', 'Down Chirp', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [0, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_1_0_0_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_1_0_0_1.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_1_0_0_1.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_1_0_0_1.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_1_0_0_1.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_1_0_0_1.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_1_0_0_1.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_1_0_0_1_win = sip.wrapinstance(self.qtgui_time_sink_x_1_0_0_1.qwidget(), Qt.QWidget)
        self.graph_grid_layout_1.addWidget(self._qtgui_time_sink_x_1_0_0_1_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.graph_grid_layout_1.setRowStretch(r, 1)
        for c in range(0, 1):
            self.graph_grid_layout_1.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_1_0_0_0_0 = qtgui.time_sink_f(
            1024, #size
            5000000, #samp_rate
            "Preamble 3 Correlation (Rx)", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_1_0_0_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_1_0_0_0_0.set_y_axis(-.1, 1.1)

        self.qtgui_time_sink_x_1_0_0_0_0.set_y_label('', "")

        self.qtgui_time_sink_x_1_0_0_0_0.enable_tags(True)
        self.qtgui_time_sink_x_1_0_0_0_0.set_trigger_mode(qtgui.TRIG_MODE_NORM, qtgui.TRIG_SLOPE_POS, .8, .000040, 0, "")
        self.qtgui_time_sink_x_1_0_0_0_0.enable_autoscale(False)
        self.qtgui_time_sink_x_1_0_0_0_0.enable_grid(False)
        self.qtgui_time_sink_x_1_0_0_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_1_0_0_0_0.enable_control_panel(False)
        self.qtgui_time_sink_x_1_0_0_0_0.enable_stem_plot(False)

        self.qtgui_time_sink_x_1_0_0_0_0.disable_legend()

        labels = ['Preamble 3', 'Down Chirp', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['cyan', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [0, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_1_0_0_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_1_0_0_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_1_0_0_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_1_0_0_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_1_0_0_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_1_0_0_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_1_0_0_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_1_0_0_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_1_0_0_0_0.qwidget(), Qt.QWidget)
        self.graph_grid_layout_0.addWidget(self._qtgui_time_sink_x_1_0_0_0_0_win, 0, 2, 1, 1)
        for r in range(0, 1):
            self.graph_grid_layout_0.setRowStretch(r, 1)
        for c in range(2, 3):
            self.graph_grid_layout_0.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_1_0_0_0 = qtgui.time_sink_f(
            1024, #size
            5000000, #samp_rate
            "Preamble 2 Correlation (Rx)", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_1_0_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_1_0_0_0.set_y_axis(-.1, 1.1)

        self.qtgui_time_sink_x_1_0_0_0.set_y_label('', "")

        self.qtgui_time_sink_x_1_0_0_0.enable_tags(True)
        self.qtgui_time_sink_x_1_0_0_0.set_trigger_mode(qtgui.TRIG_MODE_NORM, qtgui.TRIG_SLOPE_POS, .8, .000040, 0, "")
        self.qtgui_time_sink_x_1_0_0_0.enable_autoscale(False)
        self.qtgui_time_sink_x_1_0_0_0.enable_grid(False)
        self.qtgui_time_sink_x_1_0_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_1_0_0_0.enable_control_panel(False)
        self.qtgui_time_sink_x_1_0_0_0.enable_stem_plot(False)

        self.qtgui_time_sink_x_1_0_0_0.disable_legend()

        labels = ['Preamble 2', 'Down Chirp', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['green', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [0, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
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
        self.graph_grid_layout_0.addWidget(self._qtgui_time_sink_x_1_0_0_0_win, 0, 1, 1, 1)
        for r in range(0, 1):
            self.graph_grid_layout_0.setRowStretch(r, 1)
        for c in range(1, 2):
            self.graph_grid_layout_0.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_1_0_0 = qtgui.time_sink_f(
            1024, #size
            5000000, #samp_rate
            "Preamble 1 Correlation (Rx)", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_1_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_1_0_0.set_y_axis(-.1, 1.1)

        self.qtgui_time_sink_x_1_0_0.set_y_label('', "")

        self.qtgui_time_sink_x_1_0_0.enable_tags(True)
        self.qtgui_time_sink_x_1_0_0.set_trigger_mode(qtgui.TRIG_MODE_NORM, qtgui.TRIG_SLOPE_POS, .8, .000040, 0, "")
        self.qtgui_time_sink_x_1_0_0.enable_autoscale(False)
        self.qtgui_time_sink_x_1_0_0.enable_grid(False)
        self.qtgui_time_sink_x_1_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_1_0_0.enable_control_panel(False)
        self.qtgui_time_sink_x_1_0_0.enable_stem_plot(False)

        self.qtgui_time_sink_x_1_0_0.disable_legend()

        labels = ['Preamble 1', 'Down Chirp', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [0, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
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
        self.graph_grid_layout_0.addWidget(self._qtgui_time_sink_x_1_0_0_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.graph_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 1):
            self.graph_grid_layout_0.setColumnStretch(c, 1)
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
        self.graph_layout_1.addWidget(self._qtgui_time_sink_x_0_0_1_0_win)
        self.qtgui_time_sink_x_0_0_1 = qtgui.time_sink_c(
            1024, #size
            5e6, #samp_rate
            "Packet (Tx)", #name
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
        self.graph_layout_0.addWidget(self._qtgui_time_sink_x_0_0_1_win)
        self.qtgui_edit_box_msg_0_0 = qtgui.edit_box_msg(qtgui.STRING, '', 'Send Zigbee Message', False, True, 'pressed', None)
        self._qtgui_edit_box_msg_0_0_win = sip.wrapinstance(self.qtgui_edit_box_msg_0_0.qwidget(), Qt.QWidget)
        self.Messaging_grid_layout_0.addWidget(self._qtgui_edit_box_msg_0_0_win, 0, 1, 1, 1)
        for r in range(0, 1):
            self.Messaging_grid_layout_0.setRowStretch(r, 1)
        for c in range(1, 2):
            self.Messaging_grid_layout_0.setColumnStretch(c, 1)
        self.qtgui_edit_box_msg_0 = qtgui.edit_box_msg(qtgui.STRING, '', 'Send Wifi Message', False, True, 'pressed', None)
        self._qtgui_edit_box_msg_0_win = sip.wrapinstance(self.qtgui_edit_box_msg_0.qwidget(), Qt.QWidget)
        self.Messaging_grid_layout_0.addWidget(self._qtgui_edit_box_msg_0_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.Messaging_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 1):
            self.Messaging_grid_layout_0.setColumnStretch(c, 1)
        self.network_socket_pdu_0_0 = network.socket_pdu('UDP_CLIENT', '127.0.0.1', '52001', 10000, False)
        self.ieee802_15_4_rime_stack_0 = ieee802_15_4.rime_stack([129], [131], [132], [23,42])
        self.ieee802_15_4_oqpsk_phy_0 = ieee802_15_4_oqpsk_phy()
        self.ieee802_15_4_mac_0 = ieee802_15_4.mac(True,0x8841,0,0x1aaa,0xffff,0x3344)
        self.ieee802_11_mac_0 = ieee802_11.mac([0x12, 0x34, 0x56, 0x78, 0x90, 0xab], [0x30, 0x14, 0x4a, 0xe6, 0x46, 0xe4], [0x42, 0x42, 0x42, 0x42, 0x42, 0x42])
        self.blocks_threshold_ff_0_1_0 = blocks.threshold_ff(0.8, 0.8, 0)
        self.blocks_threshold_ff_0_1 = blocks.threshold_ff(0.8, 0.8, 0)
        self.blocks_threshold_ff_0_0_0 = blocks.threshold_ff(0.8, 0.8, 0)
        self.blocks_threshold_ff_0_0 = blocks.threshold_ff(0.8, 0.8, 0)
        self.blocks_threshold_ff_0 = blocks.threshold_ff(0.8, 0.8, 0)
        self.blocks_tagged_stream_multiply_length_0 = blocks.tagged_stream_multiply_length(gr.sizeof_gr_complex*1, "packet_len", 5/4)
        self.blocks_tagged_stream_multiply_length_0.set_min_output_buffer(65536)
        self.blocks_or_xx_0_0 = blocks.or_ii()
        self.blocks_or_xx_0 = blocks.or_ii()
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_cc(.2)
        self.blocks_multiply_const_vxx_0.set_min_output_buffer(415488)
        self.blocks_int_to_float_0_0 = blocks.int_to_float(1, 1)
        self.blocks_int_to_float_0 = blocks.int_to_float(1, 1)
        self.blocks_float_to_int_0_2_0 = blocks.float_to_int(1, 1)
        self.blocks_float_to_int_0_2 = blocks.float_to_int(1, 1)
        self.blocks_float_to_int_0_1 = blocks.float_to_int(1, 1)
        self.blocks_float_to_int_0_0 = blocks.float_to_int(1, 1)
        self.blocks_float_to_int_0 = blocks.float_to_int(1, 1)
        self.UConn2402_fftXCorr_2 = UConn2402.fftXCorr('/home/spencer/Documents/SeniorDesign/Git/dynamic-preambles/GNURADIO/Universal Preambles/Preambles/SigSet696_MonteCarlo1k_2.csv')
        self.UConn2402_fftXCorr_1 = UConn2402.fftXCorr('/home/spencer/Documents/SeniorDesign/Git/dynamic-preambles/GNURADIO/Universal Preambles/Preambles/SigSet696_MonteCarlo1k_1.csv')
        self.UConn2402_fftXCorr_0_1 = UConn2402.fftXCorr('/home/spencer/Documents/SeniorDesign/Git/dynamic-preambles/GNURADIO/Universal Preambles/Preambles/SigSet696_MonteCarlo1k_4.csv')
        self.UConn2402_fftXCorr_0_0 = UConn2402.fftXCorr('/home/spencer/Documents/SeniorDesign/Git/dynamic-preambles/GNURADIO/Universal Preambles/Preambles/SigSet696_MonteCarlo1k_3.csv')
        self.UConn2402_fftXCorr_0 = UConn2402.fftXCorr('/home/spencer/Documents/SeniorDesign/Git/dynamic-preambles/GNURADIO/Universal Preambles/Preambles/SigSet696_MonteCarlo1k_0.csv')
        self.UConn2402_Preamble_1 = UConn2402.Preamble(filepath_zigbee, "packet_len")
        self.UConn2402_Preamble_1.set_min_output_buffer(65536)
        self.UConn2402_Preamble_0 = UConn2402.Preamble(filepath_wifi, "packet_len")
        self.UConn2402_Preamble_0.set_min_output_buffer(415488)
        self.UConn2402_GUIMessagePrefixer_0_0 = UConn2402.GUIMessagePrefixer('AP-Zigbee: ')
        self.UConn2402_GUIMessagePrefixer_0 = UConn2402.GUIMessagePrefixer('AP-Wifi: ')
        self.UConn2402_ArbitrarySync2_1 = UConn2402.ArbitrarySync2(0.8, 50000)
        self.UConn2402_ArbitrarySync2_0 = UConn2402.ArbitrarySync2(0.8, 20000)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.UConn2402_GUIMessagePrefixer_0, 'msg_out'), (self.ieee802_11_mac_0, 'app in'))
        self.msg_connect((self.UConn2402_GUIMessagePrefixer_0, 'clear'), (self.qtgui_edit_box_msg_0, 'val'))
        self.msg_connect((self.UConn2402_GUIMessagePrefixer_0_0, 'msg_out'), (self.ieee802_15_4_rime_stack_0, 'bcin'))
        self.msg_connect((self.UConn2402_GUIMessagePrefixer_0_0, 'clear'), (self.qtgui_edit_box_msg_0_0, 'val'))
        self.msg_connect((self.ieee802_11_mac_0, 'app out'), (self.UConn2402_ArbitrarySync2_1, 'stop'))
        self.msg_connect((self.ieee802_11_mac_0, 'app out'), (self.network_socket_pdu_0_0, 'pdus'))
        self.msg_connect((self.ieee802_11_mac_0, 'phy out'), (self.wifi_phy_hier_0, 'mac_in'))
        self.msg_connect((self.ieee802_15_4_mac_0, 'pdu out'), (self.ieee802_15_4_oqpsk_phy_0, 'txin'))
        self.msg_connect((self.ieee802_15_4_mac_0, 'app out'), (self.ieee802_15_4_rime_stack_0, 'fromMAC'))
        self.msg_connect((self.ieee802_15_4_oqpsk_phy_0, 'rxout'), (self.ieee802_15_4_mac_0, 'pdu in'))
        self.msg_connect((self.ieee802_15_4_rime_stack_0, 'bcout'), (self.UConn2402_ArbitrarySync2_0, 'stop'))
        self.msg_connect((self.ieee802_15_4_rime_stack_0, 'toMAC'), (self.ieee802_15_4_mac_0, 'app in'))
        self.msg_connect((self.ieee802_15_4_rime_stack_0, 'bcout'), (self.network_socket_pdu_0_0, 'pdus'))
        self.msg_connect((self.qtgui_edit_box_msg_0, 'msg'), (self.UConn2402_GUIMessagePrefixer_0, 'msg_in'))
        self.msg_connect((self.qtgui_edit_box_msg_0_0, 'msg'), (self.UConn2402_GUIMessagePrefixer_0_0, 'msg_in'))
        self.msg_connect((self.wifi_phy_hier_0, 'mac_out'), (self.ieee802_11_mac_0, 'phy in'))
        self.connect((self.UConn2402_ArbitrarySync2_0, 0), (self.ieee802_15_4_oqpsk_phy_0, 0))
        self.connect((self.UConn2402_ArbitrarySync2_1, 0), (self.wifi_phy_hier_0, 0))
        self.connect((self.UConn2402_Preamble_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.UConn2402_Preamble_0, 0), (self.qtgui_time_sink_x_0_0_1, 0))
        self.connect((self.UConn2402_Preamble_1, 0), (self.qtgui_time_sink_x_0_0_1_0, 0))
        self.connect((self.UConn2402_Preamble_1, 0), (self.uhd_usrp_sink_0, 0))
        self.connect((self.UConn2402_fftXCorr_0, 0), (self.blocks_threshold_ff_0, 0))
        self.connect((self.UConn2402_fftXCorr_0, 0), (self.qtgui_time_sink_x_1_0_0, 0))
        self.connect((self.UConn2402_fftXCorr_0_0, 0), (self.blocks_threshold_ff_0_1, 0))
        self.connect((self.UConn2402_fftXCorr_0_0, 0), (self.qtgui_time_sink_x_1_0_0_1, 0))
        self.connect((self.UConn2402_fftXCorr_0_1, 0), (self.blocks_threshold_ff_0_1_0, 0))
        self.connect((self.UConn2402_fftXCorr_0_1, 0), (self.qtgui_time_sink_x_1_0_0_1_0, 0))
        self.connect((self.UConn2402_fftXCorr_1, 0), (self.blocks_threshold_ff_0_0, 0))
        self.connect((self.UConn2402_fftXCorr_1, 0), (self.qtgui_time_sink_x_1_0_0_0, 0))
        self.connect((self.UConn2402_fftXCorr_2, 0), (self.blocks_threshold_ff_0_0_0, 0))
        self.connect((self.UConn2402_fftXCorr_2, 0), (self.qtgui_time_sink_x_1_0_0_0_0, 0))
        self.connect((self.blocks_float_to_int_0, 0), (self.blocks_or_xx_0, 0))
        self.connect((self.blocks_float_to_int_0_0, 0), (self.blocks_or_xx_0, 2))
        self.connect((self.blocks_float_to_int_0_1, 0), (self.blocks_or_xx_0, 1))
        self.connect((self.blocks_float_to_int_0_2, 0), (self.blocks_or_xx_0_0, 0))
        self.connect((self.blocks_float_to_int_0_2_0, 0), (self.blocks_or_xx_0_0, 1))
        self.connect((self.blocks_int_to_float_0, 0), (self.UConn2402_ArbitrarySync2_1, 1))
        self.connect((self.blocks_int_to_float_0_0, 0), (self.UConn2402_ArbitrarySync2_0, 1))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.uhd_usrp_sink_0_0, 0))
        self.connect((self.blocks_or_xx_0, 0), (self.blocks_int_to_float_0, 0))
        self.connect((self.blocks_or_xx_0_0, 0), (self.blocks_int_to_float_0_0, 0))
        self.connect((self.blocks_tagged_stream_multiply_length_0, 0), (self.UConn2402_Preamble_1, 0))
        self.connect((self.blocks_threshold_ff_0, 0), (self.blocks_float_to_int_0, 0))
        self.connect((self.blocks_threshold_ff_0_0, 0), (self.blocks_float_to_int_0_1, 0))
        self.connect((self.blocks_threshold_ff_0_0_0, 0), (self.blocks_float_to_int_0_0, 0))
        self.connect((self.blocks_threshold_ff_0_1, 0), (self.blocks_float_to_int_0_2, 0))
        self.connect((self.blocks_threshold_ff_0_1_0, 0), (self.blocks_float_to_int_0_2_0, 0))
        self.connect((self.ieee802_15_4_oqpsk_phy_0, 0), (self.rational_resampler_xxx_1, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.UConn2402_ArbitrarySync2_0, 0))
        self.connect((self.rational_resampler_xxx_1, 0), (self.blocks_tagged_stream_multiply_length_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.UConn2402_ArbitrarySync2_1, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.UConn2402_fftXCorr_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.UConn2402_fftXCorr_0_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.UConn2402_fftXCorr_0_1, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.UConn2402_fftXCorr_1, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.UConn2402_fftXCorr_2, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.wifi_phy_hier_0, 0), (self.UConn2402_Preamble_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "AP")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_tx_gain(self):
        return self.tx_gain

    def set_tx_gain(self, tx_gain):
        self.tx_gain = tx_gain
        self.uhd_usrp_sink_0.set_normalized_gain(self.tx_gain, 0)
        self.uhd_usrp_sink_0_0.set_normalized_gain(self.tx_gain, 0)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.uhd_usrp_sink_0_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)
        self.wifi_phy_hier_0.set_bandwidth(self.samp_rate)

    def get_rx_gain(self):
        return self.rx_gain

    def set_rx_gain(self, rx_gain):
        self.rx_gain = rx_gain
        self.uhd_usrp_source_0.set_normalized_gain(self.rx_gain, 0)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.uhd_usrp_sink_0.set_center_freq(self.freq, 0)
        self.uhd_usrp_sink_0_0.set_center_freq(self.freq, 0)
        self.uhd_usrp_source_0.set_center_freq(self.freq, 0)
        self.wifi_phy_hier_0.set_frequency(self.freq)

    def get_filepath_zigbee(self):
        return self.filepath_zigbee

    def set_filepath_zigbee(self, filepath_zigbee):
        self.filepath_zigbee = filepath_zigbee
        self._filepath_zigbee_callback(self.filepath_zigbee)
        self.UConn2402_Preamble_1.open(self.filepath_zigbee)

    def get_filepath_wifi(self):
        return self.filepath_wifi

    def set_filepath_wifi(self, filepath_wifi):
        self.filepath_wifi = filepath_wifi
        self._filepath_wifi_callback(self.filepath_wifi)
        self.UConn2402_Preamble_0.open(self.filepath_wifi)

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




def main(top_block_cls=AP, options=None):

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
