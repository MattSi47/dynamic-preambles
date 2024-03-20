#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 UConn SD2402.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy
from gnuradio import gr
import time
import pmt


class StatusMessage(gr.sync_block):
    """
    docstring for block StatusMessage
    """
    def __init__(self, n=100):
        gr.sync_block.__init__(self,
            name="StatusMessage",
            in_sig=None,
            out_sig=None)

        self.n = int(n)
        self.idx = 0
        self.message_port_register_out(pmt.intern("status"))
        self.message_port_register_in(pmt.intern("strobe"))
        self.set_msg_handler(pmt.intern("strobe"), self.status_msg)
    
    def status_msg(self, msg):
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        if (self.n == 0): 
            self.message_port_pub(pmt.intern("status"), pmt.intern(str(msg)+"| time="+ current_time +"\n")) #add time
        elif (self.n > self.idx): 
                self.message_port_pub(pmt.intern("status"), pmt.intern(str(msg)+"| time="+ current_time +"\n")) #add time
                self.idx=self.idx+1




            
    