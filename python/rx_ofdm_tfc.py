#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Tempate Qt
# Generated: Tue Jun 14 17:25:14 2016
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt4 import Qt
from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import sip
import sys

from gnuradio import digital

# from current dir
from receive_path import receive_path
from uhd_interface_multi import uhd_receiver
#from uhd_interface import uhd_receiver

import visuals

import struct, sys

class ofdm_multichannel_receiver(gr.top_block, Qt.QWidget):

    def __init__(self,callback,options):

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 32000
        self.num_channels = len(options.args.split(','))
        print "System is setup with "+str(self.num_channels)+" receive chain(s)"

        # Add all visuals
        visuals.add_visuals(self)

        ##################################################
        # Blocks
        ##################################################

        options.bandwidth = 100000000/16

        if(options.rx_freq is not None):
            self.source = uhd_receiver(options.args,
                                       options.bandwidth, options.rx_freq,
                                       options.lo_offset, options.rx_gain,
                                       options.spec, options.antenna,
                                       options.clock_source, options.verbose)
        elif(options.from_file is not None):
            self.source = blocks.file_source(gr.sizeof_gr_complex, options.from_file)
        else:
            self.source = blocks.null_source(gr.sizeof_gr_complex)

        # Set up receive path
        # do this after for any adjustments to the options that may
        # occur in the sinks (specifically the UHD sink)
        self.rxpath = receive_path(callback, options, self.num_channels)

        ##################################################
        # Connections
        ##################################################

        for p in range(self.num_channels):
            # Connect USRP's to receive path
            self.connect((self.source,p), (self.rxpath,p))

            # Add v2s
            object_name_v2s = 'vec2stream_'+str(p)
            setattr(self, object_name_v2s, blocks.vector_to_stream(gr.sizeof_gr_complex*1,options.occupied_tones))

            # Connect receive path to v2s
            self.connect((self.rxpath,p), (getattr(self,object_name_v2s), 0))

            # Connect v2s to Constellation
            self.connect( (getattr(self,object_name_v2s), 0), (self.qtgui_const_sink_x_0, p))

        # Connect USRP to FFT plots
        # self.connect((self.source,0), (self.qtgui_freq_sink_x_0, 0))
        # self.connect((self.source,0), (self.qtgui_freq_sink_x_0, 0))

        # print "Adding to freq sinks: "+str(self.num_channels)
        # for o in range(self.num_channels):
            # self.connect((self.source,o+1), (self.qtgui_freq_sink_x_0, o))



    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "ofdm_multichannel_receiver")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()


    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)


def main(top_block_cls=ofdm_multichannel_receiver, options=None):

    global n_rcvd, n_right, printout

    n_rcvd = 0
    n_right = 0
    printout = False

    def rx_callback(ok, payload):
        global n_rcvd, n_right
        n_rcvd += 1
        (pktno,) = struct.unpack('!H', payload[0:2])
        if ok:
            n_right += 1
        if printout:
            print "ok: %r \t pktno: %d \t n_rcvd: %d \t n_right: %d" % (ok, pktno, n_rcvd, n_right)

        if 0:
            printlst = list()
            for x in payload[2:]:
                t = hex(ord(x)).replace('0x', '')
                if(len(t) == 1):
                    t = '0' + t
                printlst.append(t)
            printable = ''.join(printlst)

            if printout:
                print printable
                print "\n"

    ################################################
    # SETUP options
    # {'from_file': None, 'verbose': False, 'antenna': None, 'discontinuous': False,
    # 'args': 'addr=192.168.20.2', 'tx_freq': 900000000.0, 'fft_length': 512,
    # 'modulation': 'bpsk', 'bandwidth': 500000.0, 'snr': 30.0, 'log': False,
    # 'clock_source': None, 'lo_offset': 0, 'occupied_tones': 200,
    # 'cp_length': 128, 'freq': None, 'rx_freq': 900000000.0, 'spec': None, 'rx_gain': None}
    # options['from_file'] = None
    # options.verbose = False
    # options.antenna = None
    # options.discontinuous = False
    # options.args = 'addr=192.168.20.2'
    # options.tx_freq = 900000000
    # options.fft_length = 512
    # options.modulation = 'bpsk'
    # options.bandwidth = 500000
    # options.snr = 30
    # options.log = False
    # options.clock_source = None
    # options.lo_offset = 0
    # options.occupied_tones = 200
    # options.cp_length = 128
    # options.freq = None
    # options.rx_freq = 900000000
    # options.spec = None
    # options.rx_gain = None
    parser = OptionParser(option_class=eng_option, conflict_handler="resolve")
    expert_grp = parser.add_option_group("Expert")
    parser.add_option("","--discontinuous", action="store_true", default=False,
                      help="enable discontinuous")
    parser.add_option("","--from-file", default=None,
                      help="input file of samples to demod")

    receive_path.add_options(parser, expert_grp)
    uhd_receiver.add_options(parser)
    digital.ofdm_demod.add_options(parser, expert_grp)

    (options, args) = parser.parse_args ()

    if options.from_file is None:
        if options.rx_freq is None:
            options.rx_freq = 900000000

    ################################################
    if gr.enable_realtime_scheduling() != gr.RT_OK:
        print "Error: failed to enable real-time scheduling."

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(rx_callback,options)
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
