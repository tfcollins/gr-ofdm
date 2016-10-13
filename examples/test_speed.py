#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Test Speed
# Generated: Wed Sep 21 17:03:19 2016
##################################################

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import doa
import ofdm
import time
import numpy
import sys

class test_speed(gr.top_block):

    def __init__(self,snapshot,samp_rate):
        gr.top_block.__init__(self, "Test Speed")

        ##################################################
        # Variables
        ##################################################
        self.snapshot = snapshot #= 2048
        self.samp_rate = samp_rate #= 100e6
        self.overlap = overlap = 0

        ##################################################
        # Blocks
        ##################################################
        self.uhd_usrp_source_0 = uhd.usrp_source(
        	",".join(("addr=192.168.40.2", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        #self.uhd_usrp_source_0.set_subdev_spec("A:0 A:1 B:0 B:1", 0)
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_center_freq(2.45e9, 0)
        self.uhd_usrp_source_0.set_gain(10, 0)
        #self.uhd_usrp_source_0.set_center_freq(2.45e9, 1)
        #self.uhd_usrp_source_0.set_gain(10, 1)
        #self.uhd_usrp_source_0.set_center_freq(2.45e9, 2)
        #self.uhd_usrp_source_0.set_gain(10, 2)
        #self.uhd_usrp_source_0.set_center_freq(2.45e9, 3)
        #self.uhd_usrp_source_0.set_gain(10, 3)
        self.ofdm_stop_on_overflow_0 = ofdm.stop_on_overflow()
        self.doa_autocorrelate_0 = doa.autocorrelate(4, snapshot, overlap, 0)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_gr_complex*4*4)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.doa_autocorrelate_0, 0), (self.blocks_null_sink_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.doa_autocorrelate_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.doa_autocorrelate_0, 1))
        self.connect((self.uhd_usrp_source_0, 0), (self.doa_autocorrelate_0, 2))
        self.connect((self.uhd_usrp_source_0, 0), (self.doa_autocorrelate_0, 3))
        self.connect((self.uhd_usrp_source_0, 0), (self.ofdm_stop_on_overflow_0, 0))

    def get_snapshot(self):
        return self.snapshot

    def set_snapshot(self, snapshot):
        self.snapshot = snapshot

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)

    def get_overlap(self):
        return self.overlap

    def set_overlap(self, overlap):
        self.overlap = overlap


def main_fg(s, sr, options=None):

    top_block_cls=test_speed
    #print "Constructing FG"
    tb = top_block_cls(s,sr)
    tb.start()
    print "Going to sleep"
    time.sleep(30)
    overflow = tb.ofdm_stop_on_overflow_0.overflow
    done = overflow
    print "Done sleeping"
    print "Overflow: "+str(overflow)
    tb.stop()
    #print "tb stopped"
    time.sleep(4)
    tb = None
    #print "tb cleared"
    return done


def main():

    snapshots = numpy.array(range(5,14))
    snapshots = 2**snapshots

    mcr = 100e6/1
    decimations = numpy.array([8,6,4,2,1])
    samp_rates = mcr/decimations
    print len(samp_rates)
    print len(snapshots)

    outF = open("results.txt", "w")
    line = 'snapshots samp_rate\n'
    outF.write(line)

    for s in snapshots:
        done = False
        for sr in samp_rates:
            print "looped"
            if done:
                continue

            line = str(s)+" "+str(sr)+"\n"
            print line
            try:
                done = main_fg(s, sr)
            except:
                e = sys.exc_info()[0]
                print e
                done = False

            if done:
                print "Done with "+line
                outF.write(line)

        if not done:
            line = str(s)+" NL\n"
            outF.write(line)

    outF.close()


if __name__ == '__main__':
    main()
