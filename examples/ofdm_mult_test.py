#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Travis Collins
# Generated: Tue Sep 20 11:31:14 2016
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
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import ofdm
import ofdm.gen_preamble as gp
import ofdm.packet_process as pp
import pmt
import sip
import sys


class ofdm_mult_test(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Travis Collins")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Travis Collins")
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "ofdm_mult_test")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Variables
        ##################################################
        self.occupied_carriers = occupied_carriers = 200
        self.fft_len = fft_len = 512
        self.rcvd_pktq = rcvd_pktq = gr.msg_queue()
        self.modulation = modulation = 'bpsk'
        self.mods = mods = {"bpsk": 2, "qpsk": 4, "8psk": 8, "qam8": 8, "qam16": 16, "qam64": 64, "qam256": 256}
        self.bw = bw = (float(occupied_carriers) / float(fft_len)) / 2.0
        self.watcher = watcher = pp._queue_watcher_thread(rcvd_pktq)
        self.tb = tb = bw*0.08
        self.samp_rate = samp_rate = 100000000/16
        self.rotated_const = rotated_const = gp.gen_framer_info(modulation)
        self.phgain = phgain = 0.25
        self.max_fft_shift = max_fft_shift = 0
        self.cp_len = cp_len = 128
        self.arity = arity = mods[modulation]

        ##################################################
        # Blocks
        ##################################################
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	samp_rate, #bw
        	"", #name
        	1 #number of inputs
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        
        if not True:
          self.qtgui_freq_sink_x_0.disable_legend()
        
        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_freq_sink_x_0.set_plot_pos_half(not True)
        
        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])
        
        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_win)
        self.qtgui_const_sink_x_0 = qtgui.const_sink_c(
        	1024, #size
        	"", #name
        	1 #number of inputs
        )
        self.qtgui_const_sink_x_0.set_update_time(0.10)
        self.qtgui_const_sink_x_0.set_y_axis(-2, 2)
        self.qtgui_const_sink_x_0.set_x_axis(-2, 2)
        self.qtgui_const_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0.enable_autoscale(True)
        self.qtgui_const_sink_x_0.enable_grid(True)
        self.qtgui_const_sink_x_0.enable_axis_labels(True)
        
        if not True:
          self.qtgui_const_sink_x_0.disable_legend()
        
        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "red", "red", "red",
                  "red", "red", "red", "red", "red"]
        styles = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        markers = [0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_0.set_line_alpha(i, alphas[i])
        
        self._qtgui_const_sink_x_0_win = sip.wrapinstance(self.qtgui_const_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_const_sink_x_0_win)
        self.ofdm_mc_recover_0 = ofdm.ofdm_mc_recover(
            cp_len=cp_len,
            fft_len=fft_len,
            max_fft_shift=max_fft_shift,
            occupied_carriers=occupied_carriers,
            ports=2,
        )
        self.ofdm_eval_chan_est_0 = ofdm.eval_chan_est()
        self.blocks_vector_to_stream_0_0 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, occupied_carriers)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_null_sink_0_0 = blocks.null_sink(gr.sizeof_gr_complex*occupied_carriers)
        self.blocks_message_debug_0 = blocks.message_debug()
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_gr_complex*1, '/tmp/data.txt', False)

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.ofdm_mc_recover_0, 'packet'), (self.blocks_message_debug_0, 'store'))    
        self.msg_connect((self.ofdm_mc_recover_0, 'header_dfe'), (self.ofdm_eval_chan_est_0, 'chan_est'))    
        self.connect((self.blocks_file_source_0, 0), (self.blocks_throttle_0, 0))    
        self.connect((self.blocks_throttle_0, 0), (self.ofdm_mc_recover_0, 0))    
        self.connect((self.blocks_throttle_0, 0), (self.ofdm_mc_recover_0, 1))    
        self.connect((self.blocks_throttle_0, 0), (self.qtgui_freq_sink_x_0, 0))    
        self.connect((self.blocks_vector_to_stream_0_0, 0), (self.qtgui_const_sink_x_0, 0))    
        self.connect((self.ofdm_mc_recover_0, 1), (self.blocks_null_sink_0_0, 0))    
        self.connect((self.ofdm_mc_recover_0, 0), (self.blocks_vector_to_stream_0_0, 0))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "ofdm_mult_test")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_occupied_carriers(self):
        return self.occupied_carriers

    def set_occupied_carriers(self, occupied_carriers):
        self.occupied_carriers = occupied_carriers
        self.set_bw((float(self.occupied_carriers) / float(self.fft_len)) / 2.0)
        self.ofdm_mc_recover_0.set_occupied_carriers(self.occupied_carriers)

    def get_fft_len(self):
        return self.fft_len

    def set_fft_len(self, fft_len):
        self.fft_len = fft_len
        self.set_bw((float(self.occupied_carriers) / float(self.fft_len)) / 2.0)
        self.ofdm_mc_recover_0.set_fft_len(self.fft_len)

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

    def get_watcher(self):
        return self.watcher

    def set_watcher(self, watcher):
        self.watcher = watcher

    def get_tb(self):
        return self.tb

    def set_tb(self, tb):
        self.tb = tb

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate)
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)

    def get_rotated_const(self):
        return self.rotated_const

    def set_rotated_const(self, rotated_const):
        self.rotated_const = rotated_const

    def get_phgain(self):
        return self.phgain

    def set_phgain(self, phgain):
        self.phgain = phgain

    def get_max_fft_shift(self):
        return self.max_fft_shift

    def set_max_fft_shift(self, max_fft_shift):
        self.max_fft_shift = max_fft_shift
        self.ofdm_mc_recover_0.set_max_fft_shift(self.max_fft_shift)

    def get_cp_len(self):
        return self.cp_len

    def set_cp_len(self, cp_len):
        self.cp_len = cp_len
        self.ofdm_mc_recover_0.set_cp_len(self.cp_len)

    def get_arity(self):
        return self.arity

    def set_arity(self, arity):
        self.arity = arity


def main(top_block_cls=ofdm_mult_test, options=None):

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
