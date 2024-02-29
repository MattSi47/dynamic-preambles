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

from PyQt5 import Qt
from PyQt5.QtCore import QObject, pyqtSlot
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import UConn2402
from gnuradio import blocks
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore



from gnuradio import qtgui

class Chirp_Corr(gr.top_block, Qt.QWidget):

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

        self.settings = Qt.QSettings("GNU Radio", "Chirp_Corr")

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
        self.samp_rate = samp_rate = 4e6
        self.gain = gain = .8
        self.Chirp = Chirp = (complex(1,0), complex(6.21835e-05,-1), complex(-0.9998,-0.0200057), complex(-0.0597992,0.99821), complex(0.992863,0.119261), complex(0.197824,-0.980237), complex(-0.955745,-0.294195), complex(-0.405909,0.913914), complex(0.848732,0.528823), complex(0.656627,-0.754216), complex(-0.62525,-0.780424), complex(-0.888578,0.458726), complex(0.254945,0.966956), complex(0.999817,-0.0191353), complex(0.237122,-0.97148), complex(-0.8689,-0.494988), complex(-0.728496,0.68505), complex(0.42276,0.906241), complex(0.995161,-0.0982592), complex(0.25663,-0.96651), complex(-0.803666,-0.59508), complex(-0.859905,0.510455), complex(0.117841,0.993033), complex(0.949434,0.313966), complex(0.700952,-0.713208), complex(-0.311543,-0.950232), complex(-0.983787,-0.179339), complex(-0.642168,0.766564), complex(0.330255,0.943892), complex(0.975853,0.218428), complex(0.71517,-0.698951), complex(-0.176463,-0.984307), complex(-0.905162,-0.425067), complex(-0.879753,0.475431), complex(-0.16005,0.987109), complex(0.66983,0.742514), complex(0.999277,-0.0380146), complex(0.627093,-0.778945), complex(-0.156609,-0.987661), complex(-0.826268,-0.563277), complex(-0.980666,0.19569), complex(-0.563333,0.82623), complex(0.156486,0.98768), complex(0.778826,0.62724), complex(0.999287,-0.0377655), complex(0.742721,-0.6696), complex(0.160419,-0.987049), complex(-0.475046,-0.879961), complex(-0.904948,-0.425522), complex(-0.984406,0.175909), complex(-0.715605,0.698505), complex(-0.219099,0.975703), complex(0.329553,0.944137), complex(0.76604,0.642793), complex(0.983631,0.180197), complex(0.950523,-0.310653), complex(0.701663,-0.712509), complex(0.314971,-0.949101), complex(-0.116723,-0.993164), complex(-0.509441,-0.860505), complex(-0.802923,-0.596083), complex(-0.966174,-0.257892), complex(-0.995294,0.0968989), complex(-0.906848,0.421458), complex(-0.729518,0.683961), complex(-0.496339,0.868129), complex(-0.238691,0.971095), complex(0.0174496,0.999848), complex(0.253256,0.967399), complex(0.457122,0.889404), complex(0.623793,0.78159), complex(0.752953,0.658075), complex(0.847677,0.530513), complex(0.913078,0.407784), complex(0.955121,0.296217), complex(0.979805,0.199957), complex(0.992593,0.121488), complex(0.99807,0.0620949), complex(0.99975,0.0223724), complex(0.999997,0.00249211), complex(0.999997,0.00249211), complex(0.99975,0.0223724), complex(0.99807,0.0621025), complex(0.992593,0.121488), complex(0.979805,0.199957), complex(0.955121,0.296217), complex(0.913075,0.407791), complex(0.847677,0.530513), complex(0.752948,0.658081), complex(0.623793,0.78159), complex(0.457122,0.889404), complex(0.253263,0.967397), complex(0.0174572,0.999848), complex(-0.238699,0.971094), complex(-0.496339,0.868129), complex(-0.729521,0.683959), complex(-0.90685,0.421454), complex(-0.995295,0.0968913), complex(-0.966172,-0.2579), complex(-0.802923,-0.596083), complex(-0.509435,-0.860509), complex(-0.116723,-0.993164), complex(0.314978,-0.949099), complex(0.701663,-0.712509), complex(0.950523,-0.310653), complex(0.983631,0.180197), complex(0.76604,0.642793), complex(0.329546,0.94414), complex(-0.219099,0.975703), complex(-0.715605,0.698505), complex(-0.984408,0.175898), complex(-0.904952,-0.425515), complex(-0.475039,-0.879965), complex(0.160431,-0.987047), complex(0.742727,-0.669595), complex(0.999287,-0.0377541), complex(0.778824,0.627243), complex(0.156482,0.987681), complex(-0.563336,0.826228), complex(-0.980668,0.195678), complex(-0.826262,-0.563287), complex(-0.156598,-0.987662), complex(0.627101,-0.778938), complex(0.999277,-0.038007), complex(0.669816,0.742527), complex(-0.160065,0.987106), complex(-0.879758,0.475421), complex(-0.90516,-0.42507), complex(-0.176463,-0.984307), complex(0.71517,-0.698951), complex(0.975849,0.218447), complex(0.330259,0.94389), complex(-0.64218,0.766554), complex(-0.983787,-0.179339), complex(-0.311532,-0.950236), complex(0.700952,-0.713208), complex(0.949427,0.313987), complex(0.117843,0.993032), complex(-0.859908,0.51045), complex(-0.803657,-0.595092), complex(0.256637,-0.966508), complex(0.995161,-0.0982573), complex(0.42275,0.906246), complex(-0.728497,0.685049), complex(-0.868891,-0.495003), complex(0.237116,-0.971481), complex(0.999817,-0.0191258), complex(0.254958,0.966952), complex(-0.888587,0.458708), complex(-0.625253,-0.780422), complex(0.656632,-0.754211), complex(0.848729,0.528827), complex(-0.40592,0.913909), complex(-0.955742,-0.294204), complex(0.19784,-0.980234), complex(0.992865,0.119246), complex(-0.0598135,0.99821), complex(-0.9998,-0.0200121), complex(7.18395e-05,-1), complex(1,0))

        ##################################################
        # Blocks
        ##################################################
        # Create the options list
        self._Chirp_options = [((1+0j), (6.21835e-05-1j), (-0.9998-0.0200057j), (-0.0597992+0.99821j), (0.992863+0.119261j), (0.197824-0.980237j), (-0.955745-0.294195j), (-0.405909+0.913914j), (0.848732+0.528823j), (0.656627-0.754216j), (-0.62525-0.780424j), (-0.888578+0.458726j), (0.254945+0.966956j), (0.999817-0.0191353j), (0.237122-0.97148j), (-0.8689-0.494988j), (-0.728496+0.68505j), (0.42276+0.906241j), (0.995161-0.0982592j), (0.25663-0.96651j), (-0.803666-0.59508j), (-0.859905+0.510455j), (0.117841+0.993033j), (0.949434+0.313966j), (0.700952-0.713208j), (-0.311543-0.950232j), (-0.983787-0.179339j), (-0.642168+0.766564j), (0.330255+0.943892j), (0.975853+0.218428j), (0.71517-0.698951j), (-0.176463-0.984307j), (-0.905162-0.425067j), (-0.879753+0.475431j), (-0.16005+0.987109j), (0.66983+0.742514j), (0.999277-0.0380146j), (0.627093-0.778945j), (-0.156609-0.987661j), (-0.826268-0.563277j), (-0.980666+0.19569j), (-0.563333+0.82623j), (0.156486+0.98768j), (0.778826+0.62724j), (0.999287-0.0377655j), (0.742721-0.6696j), (0.160419-0.987049j), (-0.475046-0.879961j), (-0.904948-0.425522j), (-0.984406+0.175909j), (-0.715605+0.698505j), (-0.219099+0.975703j), (0.329553+0.944137j), (0.76604+0.642793j), (0.983631+0.180197j), (0.950523-0.310653j), (0.701663-0.712509j), (0.314971-0.949101j), (-0.116723-0.993164j), (-0.509441-0.860505j), (-0.802923-0.596083j), (-0.966174-0.257892j), (-0.995294+0.0968989j), (-0.906848+0.421458j), (-0.729518+0.683961j), (-0.496339+0.868129j), (-0.238691+0.971095j), (0.0174496+0.999848j), (0.253256+0.967399j), (0.457122+0.889404j), (0.623793+0.78159j), (0.752953+0.658075j), (0.847677+0.530513j), (0.913078+0.407784j), (0.955121+0.296217j), (0.979805+0.199957j), (0.992593+0.121488j), (0.99807+0.0620949j), (0.99975+0.0223724j), (0.999997+0.00249211j), (0.999997+0.00249211j), (0.99975+0.0223724j), (0.99807+0.0621025j), (0.992593+0.121488j), (0.979805+0.199957j), (0.955121+0.296217j), (0.913075+0.407791j), (0.847677+0.530513j), (0.752948+0.658081j), (0.623793+0.78159j), (0.457122+0.889404j), (0.253263+0.967397j), (0.0174572+0.999848j), (-0.238699+0.971094j), (-0.496339+0.868129j), (-0.729521+0.683959j), (-0.90685+0.421454j), (-0.995295+0.0968913j), (-0.966172-0.2579j), (-0.802923-0.596083j), (-0.509435-0.860509j), (-0.116723-0.993164j), (0.314978-0.949099j), (0.701663-0.712509j), (0.950523-0.310653j), (0.983631+0.180197j), (0.76604+0.642793j), (0.329546+0.94414j), (-0.219099+0.975703j), (-0.715605+0.698505j), (-0.984408+0.175898j), (-0.904952-0.425515j), (-0.475039-0.879965j), (0.160431-0.987047j), (0.742727-0.669595j), (0.999287-0.0377541j), (0.778824+0.627243j), (0.156482+0.987681j), (-0.563336+0.826228j), (-0.980668+0.195678j), (-0.826262-0.563287j), (-0.156598-0.987662j), (0.627101-0.778938j), (0.999277-0.038007j), (0.669816+0.742527j), (-0.160065+0.987106j), (-0.879758+0.475421j), (-0.90516-0.42507j), (-0.176463-0.984307j), (0.71517-0.698951j), (0.975849+0.218447j), (0.330259+0.94389j), (-0.64218+0.766554j), (-0.983787-0.179339j), (-0.311532-0.950236j), (0.700952-0.713208j), (0.949427+0.313987j), (0.117843+0.993032j), (-0.859908+0.51045j), (-0.803657-0.595092j), (0.256637-0.966508j), (0.995161-0.0982573j), (0.42275+0.906246j), (-0.728497+0.685049j), (-0.868891-0.495003j), (0.237116-0.971481j), (0.999817-0.0191258j), (0.254958+0.966952j), (-0.888587+0.458708j), (-0.625253-0.780422j), (0.656632-0.754211j), (0.848729+0.528827j), (-0.40592+0.913909j), (-0.955742-0.294204j), (0.19784-0.980234j), (0.992865+0.119246j), (-0.0598135+0.99821j), (-0.9998-0.0200121j), (7.18395e-05-1j), (1+0j)), ((1+0j), (6.21835e-05+1j), (-0.9998+0.0200057j), (-0.0597992-0.99821j), (0.992863-0.119261j), (0.197824+0.980237j), (-0.955745+0.294195j), (-0.405909-0.913914j), (0.848732-0.528823j), (0.656627+0.754216j), (-0.62525+0.780424j), (-0.888578-0.458726j), (0.254945-0.966956j), (0.999817+0.0191353j), (0.237122+0.97148j), (-0.8689+0.494988j), (-0.728496-0.68505j), (0.42276-0.906241j), (0.995161+0.0982592j), (0.25663+0.96651j), (-0.803666+0.59508j), (-0.859905-0.510455j), (0.117841-0.993033j), (0.949434-0.313966j), (0.700952+0.713208j), (-0.311543+0.950232j), (-0.983787+0.179339j), (-0.642168-0.766564j), (0.330255-0.943892j), (0.975853-0.218428j), (0.71517+0.698951j), (-0.176463+0.984307j), (-0.905162+0.425067j), (-0.879753-0.475431j), (-0.16005-0.987109j), (0.66983-0.742514j), (0.999277+0.0380146j), (0.627093+0.778945j), (-0.156609+0.987661j), (-0.826268+0.563277j), (-0.980666-0.19569j), (-0.563333-0.82623j), (0.156486-0.98768j), (0.778826-0.62724j), (0.999287+0.0377655j), (0.742721+0.6696j), (0.160419+0.987049j), (-0.475046+0.879961j), (-0.904948+0.425522j), (-0.984406-0.175909j), (-0.715605-0.698505j), (-0.219099-0.975703j), (0.329553-0.944137j), (0.76604-0.642793j), (0.983631-0.180197j), (0.950523+0.310653j), (0.701663+0.712509j), (0.314971+0.949101j), (-0.116723+0.993164j), (-0.509441+0.860505j), (-0.802923+0.596083j), (-0.966174+0.257892j), (-0.995294-0.0968989j), (-0.906848-0.421458j), (-0.729518-0.683961j), (-0.496339-0.868129j), (-0.238691-0.971095j), (0.0174496-0.999848j), (0.253256-0.967399j), (0.457122-0.889404j), (0.623793-0.78159j), (0.752953-0.658075j), (0.847677-0.530513j), (0.913078-0.407784j), (0.955121-0.296217j), (0.979805-0.199957j), (0.992593-0.121488j), (0.99807-0.0620949j), (0.99975-0.0223724j), (0.999997-0.00249211j), (0.999997-0.00249211j), (0.99975-0.0223724j), (0.99807-0.0621025j), (0.992593-0.121488j), (0.979805-0.199957j), (0.955121-0.296217j), (0.913075-0.407791j), (0.847677-0.530513j), (0.752948-0.658081j), (0.623793-0.78159j), (0.457122-0.889404j), (0.253263-0.967397j), (0.0174572-0.999848j), (-0.238699-0.971094j), (-0.496339-0.868129j), (-0.729521-0.683959j), (-0.90685-0.421454j), (-0.995295-0.0968913j), (-0.966172+0.2579j), (-0.802923+0.596083j), (-0.509435+0.860509j), (-0.116723+0.993164j), (0.314978+0.949099j), (0.701663+0.712509j), (0.950523+0.310653j), (0.983631-0.180197j), (0.76604-0.642793j), (0.329546-0.94414j), (-0.219099-0.975703j), (-0.715605-0.698505j), (-0.984408-0.175898j), (-0.904952+0.425515j), (-0.475039+0.879965j), (0.160431+0.987047j), (0.742727+0.669595j), (0.999287+0.0377541j), (0.778824-0.627243j), (0.156482-0.987681j), (-0.563336-0.826228j), (-0.980668-0.195678j), (-0.826262+0.563287j), (-0.156598+0.987662j), (0.627101+0.778938j), (0.999277+0.038007j), (0.669816-0.742527j), (-0.160065-0.987106j), (-0.879758-0.475421j), (-0.90516+0.42507j), (-0.176463+0.984307j), (0.71517+0.698951j), (0.975849-0.218447j), (0.330259-0.94389j), (-0.64218-0.766554j), (-0.983787+0.179339j), (-0.311532+0.950236j), (0.700952+0.713208j), (0.949427-0.313987j), (0.117843-0.993032j), (-0.859908-0.51045j), (-0.803657+0.595092j), (0.256637+0.966508j), (0.995161+0.0982573j), (0.42275-0.906246j), (-0.728497-0.685049j), (-0.868891+0.495003j), (0.237116+0.971481j), (0.999817+0.0191258j), (0.254958-0.966952j), (-0.888587-0.458708j), (-0.625253+0.780422j), (0.656632+0.754211j), (0.848729-0.528827j), (-0.40592-0.913909j), (-0.955742+0.294204j), (0.19784+0.980234j), (0.992865-0.119246j), (-0.0598135-0.99821j), (-0.9998+0.0200121j), (7.18395e-05+1j), (1+0j))]
        # Create the labels list
        self._Chirp_labels = ['Up Chirp', 'Down Chirp']
        # Create the combo box
        self._Chirp_tool_bar = Qt.QToolBar(self)
        self._Chirp_tool_bar.addWidget(Qt.QLabel("Chirp" + ": "))
        self._Chirp_combo_box = Qt.QComboBox()
        self._Chirp_tool_bar.addWidget(self._Chirp_combo_box)
        for _label in self._Chirp_labels: self._Chirp_combo_box.addItem(_label)
        self._Chirp_callback = lambda i: Qt.QMetaObject.invokeMethod(self._Chirp_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._Chirp_options.index(i)))
        self._Chirp_callback(self.Chirp)
        self._Chirp_combo_box.currentIndexChanged.connect(
            lambda i: self.set_Chirp(self._Chirp_options[i]))
        # Create the radio buttons
        self.top_layout.addWidget(self._Chirp_tool_bar)
        self.qtgui_time_sink_x_1 = qtgui.time_sink_f(
            1024, #size
            samp_rate, #samp_rate
            "Chirp Corr", #name
            2, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_1.set_update_time(0.10)
        self.qtgui_time_sink_x_1.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_1.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_1.enable_tags(True)
        self.qtgui_time_sink_x_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_1.enable_autoscale(False)
        self.qtgui_time_sink_x_1.enable_grid(False)
        self.qtgui_time_sink_x_1.enable_axis_labels(True)
        self.qtgui_time_sink_x_1.enable_control_panel(True)
        self.qtgui_time_sink_x_1.enable_stem_plot(False)


        labels = ['CorrUp', 'CorrDown', 'Signal 3', 'Signal 4', 'Signal 5',
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
                self.qtgui_time_sink_x_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_1.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_1.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_1.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_1.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_1.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_1_win = sip.wrapinstance(self.qtgui_time_sink_x_1.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_1_win)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_c(
            1024, #size
            samp_rate, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(True)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
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
                if (i % 2 == 0):
                    self.qtgui_time_sink_x_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self._gain_range = Range(0, 1, .05, .8, 200)
        self._gain_win = RangeWidget(self._gain_range, self.set_gain, "Gain", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._gain_win)
        self.blocks_vector_source_x_1 = blocks.vector_source_c((0, 0, 0)*10, True, 1, [])
        self.blocks_tag_gate_0 = blocks.tag_gate(gr.sizeof_gr_complex * 1, False)
        self.blocks_tag_gate_0.set_single_key("")
        self.blocks_stream_to_tagged_stream_0 = blocks.stream_to_tagged_stream(gr.sizeof_gr_complex, 1, 30, "packet_len")
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(1)
        self.UConn2402_LFMChirpXCorr_0 = UConn2402.LFMChirpXCorr(4000000, 2000000, .000040)
        self.UConn2402_Chirp_0 = UConn2402.Chirp(4000000, 2000000, .000040, 0, "packet_len")


        ##################################################
        # Connections
        ##################################################
        self.connect((self.UConn2402_Chirp_0, 0), (self.blocks_tag_gate_0, 0))
        self.connect((self.UConn2402_Chirp_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.UConn2402_LFMChirpXCorr_0, 0), (self.qtgui_time_sink_x_1, 0))
        self.connect((self.UConn2402_LFMChirpXCorr_0, 1), (self.qtgui_time_sink_x_1, 1))
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.UConn2402_LFMChirpXCorr_0, 1))
        self.connect((self.blocks_stream_to_tagged_stream_0, 0), (self.UConn2402_Chirp_0, 0))
        self.connect((self.blocks_tag_gate_0, 0), (self.UConn2402_LFMChirpXCorr_0, 0))
        self.connect((self.blocks_tag_gate_0, 0), (self.blocks_complex_to_mag_squared_0, 0))
        self.connect((self.blocks_vector_source_x_1, 0), (self.blocks_stream_to_tagged_stream_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "Chirp_Corr")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_1.set_samp_rate(self.samp_rate)

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain

    def get_Chirp(self):
        return self.Chirp

    def set_Chirp(self, Chirp):
        self.Chirp = Chirp
        self._Chirp_callback(self.Chirp)




def main(top_block_cls=Chirp_Corr, options=None):

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
