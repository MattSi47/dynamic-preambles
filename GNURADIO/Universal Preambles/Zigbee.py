#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: IEEE 802.15.4 Transceiver using OQPSK PHY
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
from gnuradio import channels
from gnuradio import filter
from gnuradio import gr
from gnuradio.fft import window
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import network
from ieee802_15_4_oqpsk_phy import ieee802_15_4_oqpsk_phy  # grc-generated hier_block
import ieee802_15_4



from gnuradio import qtgui

class Zigbee(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "IEEE 802.15.4 Transceiver using OQPSK PHY", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("IEEE 802.15.4 Transceiver using OQPSK PHY")
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

        self.settings = Qt.QSettings("GNU Radio", "Zigbee")

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
        self.filepath = filepath = '/home/uconn/dynamic-preambles/GNURADIO/Universal Preambles/Preambles/SigSet696_MonteCarlo1k_3.csv'

        ##################################################
        # Blocks
        ##################################################
        self.Messaging = Qt.QTabWidget()
        self.Messaging_widget_0 = Qt.QWidget()
        self.Messaging_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.Messaging_widget_0)
        self.Messaging_grid_layout_0 = Qt.QGridLayout()
        self.Messaging_layout_0.addLayout(self.Messaging_grid_layout_0)
        self.Messaging.addTab(self.Messaging_widget_0, 'Device 3')
        self.top_layout.addWidget(self.Messaging)
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
        self.qtgui_time_sink_x_1_0_0_0 = qtgui.time_sink_f(
            1024, #size
            5000000, #samp_rate
            "Correlation (Rx)", #name
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
        self.Messaging_grid_layout_0.addWidget(self._qtgui_time_sink_x_1_0_0_0_win, 2, 0, 1, 1)
        for r in range(2, 3):
            self.Messaging_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 1):
            self.Messaging_grid_layout_0.setColumnStretch(c, 1)
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
        self.Messaging_grid_layout_0.addWidget(self._qtgui_time_sink_x_0_0_1_win, 3, 0, 1, 1)
        for r in range(3, 4):
            self.Messaging_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 1):
            self.Messaging_grid_layout_0.setColumnStretch(c, 1)
        self.qtgui_edit_box_msg_0 = qtgui.edit_box_msg(qtgui.STRING, '', 'Send Zigbee Message (RF0)', False, True, 'pressed', None)
        self._qtgui_edit_box_msg_0_win = sip.wrapinstance(self.qtgui_edit_box_msg_0.qwidget(), Qt.QWidget)
        self.Messaging_grid_layout_0.addWidget(self._qtgui_edit_box_msg_0_win, 1, 0, 1, 1)
        for r in range(1, 2):
            self.Messaging_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 1):
            self.Messaging_grid_layout_0.setColumnStretch(c, 1)
        self.network_socket_pdu_1 = network.socket_pdu('UDP_CLIENT', '127.0.0.1', '52001', 10000, False)
        self.ieee802_15_4_rime_stack_0 = ieee802_15_4.rime_stack([129], [131], [132], [23,42])
        self.ieee802_15_4_oqpsk_phy_0 = ieee802_15_4_oqpsk_phy()
        self.ieee802_15_4_mac_0 = ieee802_15_4.mac(True,0x8841,0,0x1aaa,0xffff,0x3344)
        # Create the options list
        self._filepath_options = ['/home/uconn/dynamic-preambles/GNURADIO/Universal Preambles/Preambles/SigSet696_MonteCarlo1k_3.csv', '/home/uconn/dynamic-preambles/GNURADIO/Universal Preambles/Preambles/SigSet696_MonteCarlo1k_4.csv']
        # Create the labels list
        self._filepath_labels = ['Preamble 4', 'Preamble 5']
        # Create the combo box
        # Create the radio buttons
        self._filepath_group_box = Qt.QGroupBox("Preamble" + ": ")
        self._filepath_box = Qt.QHBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._filepath_button_group = variable_chooser_button_group()
        self._filepath_group_box.setLayout(self._filepath_box)
        for i, _label in enumerate(self._filepath_labels):
            radio_button = Qt.QRadioButton(_label)
            self._filepath_box.addWidget(radio_button)
            self._filepath_button_group.addButton(radio_button, i)
        self._filepath_callback = lambda i: Qt.QMetaObject.invokeMethod(self._filepath_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._filepath_options.index(i)))
        self._filepath_callback(self.filepath)
        self._filepath_button_group.buttonClicked[int].connect(
            lambda i: self.set_filepath(self._filepath_options[i]))
        self.Messaging_grid_layout_0.addWidget(self._filepath_group_box, 0, 0, 1, 1)
        for r in range(0, 1):
            self.Messaging_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 1):
            self.Messaging_grid_layout_0.setColumnStretch(c, 1)
        self.channels_channel_model_0 = channels.channel_model(
            noise_voltage=0.0,
            frequency_offset=0.0,
            epsilon=1.0,
            taps=[1.0 + 1.0j],
            noise_seed=0,
            block_tags=True)
        self.blocks_tagged_stream_multiply_length_0 = blocks.tagged_stream_multiply_length(gr.sizeof_gr_complex*1, "packet_len", 5/4)
        self.blocks_tagged_stream_multiply_length_0.set_min_output_buffer(81920)
        self.UConn2402_fftXCorr_0 = UConn2402.fftXCorr('/home/spencer/Documents/SeniorDesign/Git/dynamic-preambles/GNURADIO/Universal Preambles/Preambles/SigSet696_MonteCarlo1k_4.csv')
        self.UConn2402_Preamble_0 = UConn2402.Preamble('/home/spencer/Documents/SeniorDesign/Git/dynamic-preambles/GNURADIO/Universal Preambles/Preambles/SigSet696_MonteCarlo1k_4.csv', "packet_len")
        self.UConn2402_Preamble_0.set_min_output_buffer(81920)
        self.UConn2402_GUIMessagePrefixer_0 = UConn2402.GUIMessagePrefixer('Zigbee-Device3: ')
        self.UConn2402_ArbitrarySync2_0 = UConn2402.ArbitrarySync2(0.8, 20000)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.UConn2402_GUIMessagePrefixer_0, 'msg_out'), (self.ieee802_15_4_rime_stack_0, 'bcin'))
        self.msg_connect((self.UConn2402_GUIMessagePrefixer_0, 'clear'), (self.qtgui_edit_box_msg_0, 'val'))
        self.msg_connect((self.ieee802_15_4_mac_0, 'pdu out'), (self.ieee802_15_4_oqpsk_phy_0, 'txin'))
        self.msg_connect((self.ieee802_15_4_mac_0, 'app out'), (self.ieee802_15_4_rime_stack_0, 'fromMAC'))
        self.msg_connect((self.ieee802_15_4_oqpsk_phy_0, 'rxout'), (self.ieee802_15_4_mac_0, 'pdu in'))
        self.msg_connect((self.ieee802_15_4_rime_stack_0, 'bcout'), (self.UConn2402_ArbitrarySync2_0, 'stop'))
        self.msg_connect((self.ieee802_15_4_rime_stack_0, 'toMAC'), (self.ieee802_15_4_mac_0, 'app in'))
        self.msg_connect((self.ieee802_15_4_rime_stack_0, 'bcout'), (self.network_socket_pdu_1, 'pdus'))
        self.msg_connect((self.qtgui_edit_box_msg_0, 'msg'), (self.UConn2402_GUIMessagePrefixer_0, 'msg_in'))
        self.connect((self.UConn2402_ArbitrarySync2_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.UConn2402_Preamble_0, 0), (self.channels_channel_model_0, 0))
        self.connect((self.UConn2402_Preamble_0, 0), (self.qtgui_time_sink_x_0_0_1, 0))
        self.connect((self.UConn2402_fftXCorr_0, 0), (self.UConn2402_ArbitrarySync2_0, 1))
        self.connect((self.UConn2402_fftXCorr_0, 0), (self.qtgui_time_sink_x_1_0_0_0, 0))
        self.connect((self.blocks_tagged_stream_multiply_length_0, 0), (self.UConn2402_Preamble_0, 0))
        self.connect((self.channels_channel_model_0, 0), (self.UConn2402_ArbitrarySync2_0, 0))
        self.connect((self.channels_channel_model_0, 0), (self.UConn2402_fftXCorr_0, 0))
        self.connect((self.ieee802_15_4_oqpsk_phy_0, 0), (self.rational_resampler_xxx_1, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.ieee802_15_4_oqpsk_phy_0, 0))
        self.connect((self.rational_resampler_xxx_1, 0), (self.blocks_tagged_stream_multiply_length_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "Zigbee")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_tx_gain(self):
        return self.tx_gain

    def set_tx_gain(self, tx_gain):
        self.tx_gain = tx_gain

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_rx_gain(self):
        return self.rx_gain

    def set_rx_gain(self, rx_gain):
        self.rx_gain = rx_gain

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq

    def get_filepath(self):
        return self.filepath

    def set_filepath(self, filepath):
        self.filepath = filepath
        self._filepath_callback(self.filepath)




def main(top_block_cls=Zigbee, options=None):

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
