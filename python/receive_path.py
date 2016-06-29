#
# Copyright 2005,2006,2011 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# GNU Radio is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# GNU Radio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GNU Radio; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#

from gnuradio import gr
from gnuradio import eng_notation
from gnuradio import blocks
#from gnuradio import digital
import ofdm_mods as ofdm
from gnuradio import analog

import copy
import sys

# /////////////////////////////////////////////////////////////////////////////
#                              receive path
# /////////////////////////////////////////////////////////////////////////////

def gen_multiple_ios(num):
    io = []
    for i in range(num):
        io.append(gr.sizeof_gr_complex)
    return io

class receive_path(gr.hier_block2):
    def __init__(self, rx_callback, options):

        self.rx_channels = len(options.args.split(','))

	gr.hier_block2.__init__(self, "receive_path",
				gr.io_signaturev(self.rx_channels, self.rx_channels, gen_multiple_ios(self.rx_channels) ),
				gr.io_signaturev(2, 2, [gr.sizeof_gr_complex*options.occupied_tones,gr.sizeof_gr_complex*options.occupied_tones]))
                #,gr.sizeof_gr_complex*options.occupied_tones,]))#gr.sizeof_gr_complex*options.occupied_tones]))


        options = copy.copy(options)    # make a copy so we can destructively modify

        self._verbose     = options.verbose
        self._log         = options.log
        self._rx_callback = rx_callback      # this callback is fired when there's a packet available

        # receiver
        self.ofdm_rx = ofdm.ofdm_demod(options,callback=self._rx_callback)

        # # Carrier Sensing Blocks
        # alpha = 0.001
        # thresh = 30   # in dB, will have to adjust
        # self.probe = analog.probe_avg_mag_sqrd_c(thresh,alpha)

        # Connect USRP to OFDM Demodulator
        self.connect((self,0), (self.ofdm_rx,0))
        self.connect((self,1), (self.ofdm_rx,1))

        # Connect probe to output of channel filter
        # self.connect((self.ofdm_rx,0), self.probe)

        # Extra output from FFT Demod
        self.connect((self.ofdm_rx,0), (self,0))
        self.connect((self.ofdm_rx,1), (self,1))

        # Connect equalized signals to output
        # self.connect((self.ofdm_rx,2), (self,1))
        # self.connect((self.ofdm_rx,3), (self,2))

        # Display some information about the setup
        if self._verbose:
            self._print_verbage()

    def carrier_sensed(self):
        """
        Return True if we think carrier is present.
        """
        #return self.probe.level() > X
        return self.probe.unmuted()

    def carrier_threshold(self):
        """
        Return current setting in dB.
        """
        return self.probe.threshold()

    def set_carrier_threshold(self, threshold_in_db):
        """
        Set carrier threshold.

        Args:
            threshold_in_db: set detection threshold (float (dB))
        """
        self.probe.set_threshold(threshold_in_db)


    def add_options(normal, expert):
        """
        Adds receiver-specific options to the Options Parser
        """
        normal.add_option("-W", "--bandwidth", type="eng_float",
                          default=500e3,
                          help="set symbol bandwidth [default=%default]")
        normal.add_option("-v", "--verbose", action="store_true", default=False)
        expert.add_option("", "--log", action="store_true", default=False,
                          help="Log all parts of flow graph to files (CAUTION: lots of data)")

    # Make a static method to call before instantiation
    add_options = staticmethod(add_options)


    def _print_verbage(self):
        """
        Prints information about the receive path
        """
        pass
