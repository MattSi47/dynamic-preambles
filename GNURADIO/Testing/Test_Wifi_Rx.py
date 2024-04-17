#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# GNU Radio version: 3.10.1.1

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from gnuradio import UConn2402
from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
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




class Test_Wifi_Rx(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)

        ##################################################
        # Variables
        ##################################################
        self.tx_gain = tx_gain = .8
        self.samp_rate = samp_rate = 5e6
        self.rx_gain = rx_gain = .5
        self.freq = freq = 5890000000
        self.encoding = encoding = 0
        self.chan_est = chan_est = 0

        ##################################################
        # Blocks
        ##################################################
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
        self.uhd_usrp_source_0.set_antenna("RX2", 0)
        self.uhd_usrp_source_0.set_normalized_gain(rx_gain, 0)
        self.network_socket_pdu_0_0 = network.socket_pdu('UDP_CLIENT', '127.0.0.1', '52001', 10000, False)
        self.ieee802_11_mac_0 = ieee802_11.mac([0x12, 0x34, 0x56, 0x78, 0x90, 0xab], [0x30, 0x14, 0x4a, 0xe6, 0x46, 0xe4], [0x42, 0x42, 0x42, 0x42, 0x42, 0x42])
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.UConn2402_fftXCorr_0 = UConn2402.fftXCorr('/home/spencer/Documents/SeniorDesign/Git/dynamic-preambles/GNURADIO/Universal Preambles/Preambles/SigSet696_MonteCarlo1k_4.csv')
        self.UConn2402_ArbitrarySync2_0 = UConn2402.ArbitrarySync2(0.6, 20000)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.ieee802_11_mac_0, 'app out'), (self.UConn2402_ArbitrarySync2_0, 'stop'))
        self.msg_connect((self.ieee802_11_mac_0, 'app out'), (self.network_socket_pdu_0_0, 'pdus'))
        self.msg_connect((self.ieee802_11_mac_0, 'phy out'), (self.wifi_phy_hier_0, 'mac_in'))
        self.msg_connect((self.wifi_phy_hier_0, 'mac_out'), (self.ieee802_11_mac_0, 'phy in'))
        self.connect((self.UConn2402_ArbitrarySync2_0, 0), (self.wifi_phy_hier_0, 0))
        self.connect((self.UConn2402_fftXCorr_0, 0), (self.UConn2402_ArbitrarySync2_0, 1))
        self.connect((self.uhd_usrp_source_0, 0), (self.UConn2402_ArbitrarySync2_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.UConn2402_fftXCorr_0, 0))
        self.connect((self.wifi_phy_hier_0, 0), (self.blocks_null_sink_0, 0))


    def get_tx_gain(self):
        return self.tx_gain

    def set_tx_gain(self, tx_gain):
        self.tx_gain = tx_gain

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)
        self.wifi_phy_hier_0.set_bandwidth(self.samp_rate)

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
        self.uhd_usrp_source_0.set_center_freq(self.freq, 0)
        self.uhd_usrp_source_0.set_center_freq(self.freq, 1)
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




def main(top_block_cls=Test_Wifi_Rx, options=None):
    tb = top_block_cls()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    try:
        input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
