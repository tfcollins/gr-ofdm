
import math
from gnuradio import gr, fft
from gnuradio import blocks
#import digital_swig as digital
from gnuradio import digital as digital
#from gnuradio.digital import ofdm_packet_utils as ofdm_packet_utils
import ofdm_packet_utils_whiten as ofdm_packet_utils
from ofdm_receiver import ofdm_receiver
import gnuradio.gr.gr_threading as _threading
import gnuradio.digital.psk as psk
import gnuradio.digital.qam as qam
import ofdm

import copy

# /////////////////////////////////////////////////////////////////////////////
#                   mod/demod with packets as i/o
# /////////////////////////////////////////////////////////////////////////////

class ofdm_mod(gr.hier_block2):
    """
    Modulates an OFDM stream. Based on the options fft_length, occupied_tones, and
    cp_length, this block creates OFDM symbols using a specified modulation option.

    Send packets by calling send_pkt
    """
    def __init__(self, options, msgq_limit=2, pad_for_usrp=True):
        """
	Hierarchical block for sending packets

        Packets to be sent are enqueued by calling send_pkt.
        The output is the complex modulated signal at baseband.

        Args:
            options: pass modulation options from higher layers (fft length, occupied tones, etc.)
            msgq_limit: maximum number of messages in message queue (int)
            pad_for_usrp: If true, packets are padded such that they end up a multiple of 128 samples
        """

	gr.hier_block2.__init__(self, "ofdm_mod",
				gr.io_signature(0, 0, 0),       # Input signature
				gr.io_signature(1, 1, gr.sizeof_gr_complex)) # Output signature

        self._pad_for_usrp = pad_for_usrp
        self._modulation = options.modulation
        self._fft_length = options.fft_length
        self._occupied_tones = options.occupied_tones
        self._cp_length = options.cp_length

        win = [] #[1 for i in range(self._fft_length)]

        # Use freq domain to get doubled-up known symbol for correlation in time domain
        zeros_on_left = int(math.ceil((self._fft_length - self._occupied_tones)/2.0))
        ksfreq = known_symbols_4512_3[0:self._occupied_tones]
        for i in range(len(ksfreq)):
            if((zeros_on_left + i) & 1):
                ksfreq[i] = 0

        # hard-coded known symbols
        preambles = (ksfreq,)

        padded_preambles = list()
        for pre in preambles:
            padded = self._fft_length*[0,]
            padded[zeros_on_left : zeros_on_left + self._occupied_tones] = pre
            padded_preambles.append(padded)

        symbol_length = options.fft_length + options.cp_length

        mods = {"bpsk": 2, "qpsk": 4, "8psk": 8, "qam8": 8, "qam16": 16, "qam64": 64, "qam256": 256}
        arity = mods[self._modulation]

        rot = 1
        if self._modulation == "qpsk":
            rot = (0.707+0.707j)

        # FIXME: pass the constellation objects instead of just the points
        if(self._modulation.find("psk") >= 0):
            constel = psk.psk_constellation(arity)
            rotated_const = map(lambda pt: pt * rot, constel.points())
        elif(self._modulation.find("qam") >= 0):
            constel = qam.qam_constellation(arity)
            rotated_const = map(lambda pt: pt * rot, constel.points())
        #print rotated_const
        self._pkt_input = digital.ofdm_mapper_bcv(rotated_const,
                                                  msgq_limit,
                                                  options.occupied_tones,
                                                  options.fft_length)

        self.preambles = digital.ofdm_insert_preamble(self._fft_length,
                                                      padded_preambles)
        self.ifft = fft.fft_vcc(self._fft_length, False, win, True)
        self.cp_adder = digital.ofdm_cyclic_prefixer(self._fft_length,
                                                     symbol_length)
        self.scale = blocks.multiply_const_cc(1.0 / math.sqrt(self._fft_length))

        self.connect((self._pkt_input, 0), (self.preambles, 0))
        self.connect((self._pkt_input, 1), (self.preambles, 1))
        self.connect(self.preambles, self.ifft, self.cp_adder, self.scale, self)

    def send_pkt(self, payload='', eof=False):
        """
        Send the payload.

        Args:
            payload: data to send (string)
        """
        if eof:
            msg = gr.message(1) # tell self._pkt_input we're not sending any more packets
        else:
            # print "original_payload =", string_to_hex_list(payload)
            pkt = ofdm_packet_utils.make_packet(payload, 1, 1,
                                                self._pad_for_usrp,
                                                whitening=True)

            #print "pkt =", string_to_hex_list(pkt)
            msg = gr.message_from_string(pkt)
        self._pkt_input.msgq().insert_tail(msg)

    def add_options(normal, expert):
        """
        Adds OFDM-specific options to the Options Parser
        """
        normal.add_option("-m", "--modulation", type="string", default="bpsk",
                          help="set modulation type (bpsk, qpsk, 8psk, qam{16,64}) [default=%default]")
        expert.add_option("", "--fft-length", type="intx", default=512,
                          help="set the number of FFT bins [default=%default]")
        expert.add_option("", "--occupied-tones", type="intx", default=200,
                          help="set the number of occupied FFT bins [default=%default]")
        expert.add_option("", "--cp-length", type="intx", default=128,
                          help="set the number of bits in the cyclic prefix [default=%default]")
    # Make a static method to call before instantiation
    add_options = staticmethod(add_options)
