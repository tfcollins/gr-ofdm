#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2016 <+YOU OR YOUR COMPANY+>.
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#

import numpy
from gnuradio import gr
import pmt

class stop_on_overflow(gr.sync_block):
    """
    docstring for block stop_on_overflow
    """
    def __init__(self):
        gr.sync_block.__init__(self,
            name="stop_on_overflow",
            in_sig=[numpy.complex64],
            out_sig=None)

        self.overflow = False
        self.startup = False
        self.offset = -1


    def work(self, input_items, output_items):

        # in0 = input_items[0]

        nread = self.nitems_read(0) #number of items read on port 0
        ninput_items = len(input_items[0])
        #read all tags associated with port 0 for items in this work function
        tags = self.get_tags_in_range(0, nread, nread+ninput_items)
        for tag in tags:
            # self.key = pmt.symbol_to_string(tag.key)
            if tag.offset == self.offset:
                # print "Same offset skipping"
                # print tag.offset
                # print self.offset
                continue
            else:
                # print "New offset"
                # print tag.offset
                # print self.offset
                self.offset = tag.offset
            # If not first tag then it is an overflow
            if self.startup:
                self.overflow = True
                print "Overflow"
                return -1
            else:
                # print "Startup flag set"
                self.startup = True

        return len(input_items[0])
