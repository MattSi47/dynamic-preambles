#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 UConn SD2402.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy
from gnuradio import gr
import pmt
import time

class GUIMessagePrefixer(gr.sync_block):
    """
    docstring for block GUIMessagePrefixer
    """
    def __init__(self, prefix="test: "):
        gr.sync_block.__init__(self,
            name="GUIMessagePrefixer",
            in_sig=None,
            out_sig=None)

        self.prefix= prefix

        self.message_port_register_in(pmt.intern("msg_in"))
        self.message_port_register_out(pmt.intern("msg_out"))
        self.message_port_register_out(pmt.intern("clear"))
        self.set_msg_handler(pmt.intern("msg_in"), self.handle_msg)
    
    def handle_msg(self, msg):
        if str(msg) != "":  #Reject empty strings
            self.message_port_pub(pmt.intern("msg_out"), pmt.intern(str(self.prefix)+str(msg)+ "\n")) #add prefix
            time.sleep(.1)# time delay for clear
            self.message_port_pub(pmt.intern("clear"), pmt.intern("")) #clear stream