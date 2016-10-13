# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: OFDM Mutichannel Recover
# Author: Travis Collins
# Generated: Tue Sep 20 09:10:31 2016
##################################################

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from gnuradio import blocks
from gnuradio import filter
from gnuradio import gr
from gnuradio.filter import firdes
from ofdm_packet_sync import ofdm_packet_sync  # grc-generated hier_block
from ofdm_sync_channel import ofdm_sync_channel  # grc-generated hier_block
import ofdm
import ofdm.gen_preamble as gp
import ofdm.packet_process as pp
import pmt


class ofdm_mc_recover(gr.hier_block2):

    def __init__(self, cp_len=32, fft_len=64, max_fft_shift=4, occupied_carriers=48, ports=2):
        gr.hier_block2.__init__(
            self, "OFDM Mutichannel Recover",
            gr.io_signaturev(2, 2, [gr.sizeof_gr_complex*1, gr.sizeof_gr_complex*1]),
            gr.io_signaturev(2, 2, [gr.sizeof_gr_complex*occupied_carriers, gr.sizeof_gr_complex*occupied_carriers]),
        )
        self.message_port_register_hier_out("packet")
        self.message_port_register_hier_out("header_dfe")

        ##################################################
        # Parameters
        ##################################################
        self.cp_len = cp_len
        self.fft_len = fft_len
        self.max_fft_shift = max_fft_shift
        self.occupied_carriers = occupied_carriers
        self.ports = ports

        ##################################################
        # Variables
        ##################################################
        self.rcvd_pktq = rcvd_pktq = gr.msg_queue()
        self.modulation = modulation = 'bpsk'
        self.mods = mods = {"bpsk": 2, "qpsk": 4, "8psk": 8, "qam8": 8, "qam16": 16, "qam64": 64, "qam256": 256}
        self.bw = bw = (float(occupied_carriers) / float(fft_len)) / 2.0
        self.watcher = watcher = pp._queue_watcher_thread(rcvd_pktq)
        self.tb = tb = bw*0.08
        self.samp_rate = samp_rate = 32000
        self.rotated_const = rotated_const = gp.gen_framer_info(modulation)
        self.phgain = phgain = 0.25
        self.arity = arity = mods[modulation]

        ##################################################
        # Blocks
        ##################################################
        self.ofdm_sync_channel_0 = ofdm_sync_channel(
            cp_len=cp_len,
            fftlen=fft_len,
            max_fft_shift=max_fft_shift,
            occupied_carriers=occupied_carriers,
        )
        self.ofdm_packet_sync_0 = ofdm_packet_sync(
            cp_len=cp_len,
            fft_len=fft_len,
        )

        self.fft_filter_xxx_0 = filter.fft_filter_ccc(1, (filter.firdes.low_pass (1.0, 1.0, bw+tb, tb, filter.firdes.WIN_HAMMING)), 1)
        self.fft_filter_xxx_0.declare_sample_delay(0)
        self.ofdm_ofdm_mrx_frame_sink_0 = ofdm.ofdm_mrx_frame_sink(rotated_const, range(arity), rcvd_pktq, occupied_carriers, phgain, phgain*phgain /4.0, ports)

        for p in range(ports-1):
            # Add OFDM Sync Channel
            object_name_osc = 'ofdm_sync_channel_'+str(p+1)
            setattr(self, object_name_osc, ofdm_sync_channel(
                    cp_len=cp_len,
                    fftlen=fft_len,
                    max_fft_shift=max_fft_shift,
                    occupied_carriers=occupied_carriers,
                ))

            # Add FFT Filter
            object_name_ft = 'fft_filter_ccc_'+str(p+1)
            setattr(self, object_name_ft, filter.fft_filter_ccc(1, (filter.firdes.low_pass (1.0, 1.0, bw+tb, tb, filter.firdes.WIN_HAMMING)), 1) )
            # self.fft_filter_xxx_0_0.declare_sample_delay(0)
            setattr(getattr(self,object_name_ft),'declare_sample_delay',0)

            # Add null sink
            object_name_ns = 'blocks_null_sink_'+str(p+1)
            setattr(self, object_name_ns, blocks.null_sink(gr.sizeof_char*1) )

            ### Connections
            # Pad to FFT Filter
            self.connect( (self, p+1), (getattr(self,object_name_ft), 0))

            # FFT Filt to OFS
            self.connect( (getattr(self,object_name_ft), 0), (getattr(self,object_name_osc), 0) )

            # PS To OFDM SC
            self.connect( (self.ofdm_packet_sync_0, 0), (getattr(self,object_name_osc), 2))
            self.connect( (self.ofdm_packet_sync_0, 1), (getattr(self,object_name_osc), 1))

            # OSC To OFDM Frame Sink
            self.connect((getattr(self,object_name_osc), 1), (self.ofdm_sync_channel_0, p+2))

            # OSC To Null Sink
            self.connect((getattr(self,object_name_osc), 0), (self.blocks_null_sink_0, 0))

            # OFDM Frame Sink to Pad
            self.connect((self.ofdm_ofdm_mrx_frame_sink_0, p), (self, p))


        ##################################################
        # Connections
        ##################################################
        self.connect((self, 0), (self.fft_filter_xxx_0, 0))
        self.connect((self.fft_filter_xxx_0, 0), (self.ofdm_packet_sync_0, 0))

        self.connect((self.ofdm_packet_sync_0, 0), (self.ofdm_sync_channel_0, 2))
        self.connect((self.ofdm_packet_sync_0, 1), (self.ofdm_sync_channel_0, 1))
        self.connect((self.ofdm_packet_sync_0, 2), (self.ofdm_sync_channel_0, 0))

        self.connect((self.ofdm_sync_channel_0, 0), (self.ofdm_ofdm_mrx_frame_sink_0, 0)) # Flag
        self.connect((self.ofdm_sync_channel_0, 1), (self.ofdm_ofdm_mrx_frame_sink_0, 1))

        self.msg_connect((self.ofdm_ofdm_mrx_frame_sink_0, 'packet'), (self, 'packet'))
        self.msg_connect((self.ofdm_ofdm_mrx_frame_sink_0, 'header_dfe'), (self, 'header_dfe'))

    def get_cp_len(self):
        return self.cp_len

    def set_cp_len(self, cp_len):
        self.cp_len = cp_len
        self.ofdm_packet_sync_0.set_cp_len(self.cp_len)

    def get_fft_len(self):
        return self.fft_len

    def set_fft_len(self, fft_len):
        self.fft_len = fft_len
        self.set_bw((float(self.occupied_carriers) / float(self.fft_len)) / 2.0)
        self.ofdm_sync_channel_0.set_fftlen(self.fft_len)
        self.ofdm_packet_sync_0.set_fft_len(self.fft_len)

    def get_max_fft_shift(self):
        return self.max_fft_shift

    def set_max_fft_shift(self, max_fft_shift):
        self.max_fft_shift = max_fft_shift
        self.ofdm_sync_channel_0_0_0.set_max_fft_shift(self.max_fft_shift)
        self.ofdm_sync_channel_0_0.set_max_fft_shift(self.max_fft_shift)

    def get_occupied_carriers(self):
        return self.occupied_carriers

    def set_occupied_carriers(self, occupied_carriers):
        self.occupied_carriers = occupied_carriers
        self.set_bw((float(self.occupied_carriers) / float(self.fft_len)) / 2.0)
        self.ofdm_sync_channel_0_0_0.set_occupied_carriers(self.occupied_carriers)
        self.ofdm_sync_channel_0_0.set_occupied_carriers(self.occupied_carriers)

    def get_ports(self):
        return self.ports

    def set_ports(self, ports):
        self.ports = ports

    def get_rcvd_pktq(self):
        return self.rcvd_pktq

    def set_rcvd_pktq(self, rcvd_pktq):
        self.rcvd_pktq = rcvd_pktq
        self.set_watcher(pp._queue_watcher_thread(self.rcvd_pktq))

    def get_modulation(self):
        return self.modulation

    def set_modulation(self, modulation):
        self.modulation = modulation
        self.set_rotated_const(gp.gen_framer_info(self.modulation))
        self.set_arity(self.mods[self.modulation])

    def get_mods(self):
        return self.mods

    def set_mods(self, mods):
        self.mods = mods
        self.set_arity(self.mods[self.modulation])

    def get_bw(self):
        return self.bw

    def set_bw(self, bw):
        self.bw = bw
        self.set_tb(self.bw*0.08)
        self.fft_filter_xxx_0_0.set_taps((filter.firdes.low_pass (1.0, 1.0, self.bw+self.tb, self.tb, filter.firdes.WIN_HAMMING)))
        self.fft_filter_xxx_0.set_taps((filter.firdes.low_pass (1.0, 1.0, self.bw+self.tb, self.tb, filter.firdes.WIN_HAMMING)))

    def get_watcher(self):
        return self.watcher

    def set_watcher(self, watcher):
        self.watcher = watcher

    def get_tb(self):
        return self.tb

    def set_tb(self, tb):
        self.tb = tb
        self.fft_filter_xxx_0_0.set_taps((filter.firdes.low_pass (1.0, 1.0, self.bw+self.tb, self.tb, filter.firdes.WIN_HAMMING)))
        self.fft_filter_xxx_0.set_taps((filter.firdes.low_pass (1.0, 1.0, self.bw+self.tb, self.tb, filter.firdes.WIN_HAMMING)))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_rotated_const(self):
        return self.rotated_const

    def set_rotated_const(self, rotated_const):
        self.rotated_const = rotated_const

    def get_phgain(self):
        return self.phgain

    def set_phgain(self, phgain):
        self.phgain = phgain

    def get_arity(self):
        return self.arity

    def set_arity(self, arity):
        self.arity = arity
