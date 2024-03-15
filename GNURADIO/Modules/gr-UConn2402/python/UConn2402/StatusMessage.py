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
    def __init__(self, msg= "Device active", interval=3.0):
        gr.sync_block.__init__(self,
            name="StatusMessage",
            in_sig=None,
            out_sig=None)

        self.msg = msg
        self.interval= interval
        self.message_port_register_out(pmt.intern("status"))
        status_msg(self)
        self.message_port_pub(pmt.intern("status"), pmt.intern(str(self.msg)+ "\n"))

def status_msg(self):
        while (True):
            print(self.interval)
            time.sleep(self.interval)
            #t = time.localtime()
            #current_time = time.strftime("%H:%M:%S", t)
            self.message_port_pub(pmt.intern("status"), pmt.intern(str(self.msg)+ "\n"))


            
    