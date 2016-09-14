
from gnuradio.digital import ofdm_packet_utils as ofdm_packet_utils
#import ofdm_packet_utils_whiten as ofdm_packet_utils # FIX ME
import gnuradio.gr.gr_threading as _threading
import struct, sys

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

class _queue_watcher_thread(_threading.Thread):
    # def __init__(self, rcvd_pktq, callback):
    def __init__(self, rcvd_pktq):
        _threading.Thread.__init__(self)
        self.setDaemon(1)
        self.rcvd_pktq = rcvd_pktq
        # self.callback = callback
        # self.callback = rx_callback
        print "start called"
        self.keep_running = True
        self.start()


    def run(self):
        print "Run called"
        while self.keep_running:
            # Take packet off queue
            # print "Pre dequeue"
            # print self.rcvd_pktq.count()
            msg = self.rcvd_pktq.delete_head()
            # print "Post dequeue"
            # Decode packet
            ok, payload = ofdm_packet_utils.unmake_packet(msg.to_string())
            # Send to callback
            rx_callback(ok, payload)
            # if self.callback:
                # self.callback(ok, payload)
