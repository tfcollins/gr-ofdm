#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Test Start Stop
# Generated: Wed Sep 21 19:04:21 2016
##################################################

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import time


class test_start_stop(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Test Start Stop")

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 10e6

        ##################################################
        # Blocks
        ##################################################
        self.uhd_usrp_source_0 = uhd.usrp_source(
        	",".join(("addr=192.168.40.2", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(2),
        	),
        )
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_center_freq(2.45e9, 0)
        self.uhd_usrp_source_0.set_gain(10, 0)
        self.uhd_usrp_source_0.set_center_freq(2.45e9, 1)
        self.uhd_usrp_source_0.set_gain(10, 1)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_gr_complex*1)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.uhd_usrp_source_0, 0), (self.blocks_null_sink_0, 0))
        self.connect((self.uhd_usrp_source_0, 1), (self.blocks_null_sink_0, 1))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)


def main(top_block_cls=test_start_stop, options=None):

    tb = top_block_cls()
    tb.start()
    print "Waiting 10 seconds"
    time.sleep(10)
    print "Stopping FG"
    tb.stop()
    time.sleep(4)
    try:
        print "Trying to teardown FG"
    	tb = None # This will segfault, only visible by gdb
    except:
        print "Failed"

    print "Reached"

if __name__ == '__main__':
    main()
