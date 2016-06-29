### Setup visuals
from PyQt4 import Qt
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip

def add_visuals(self):

    gr.top_block.__init__(self, "Tempate Qt")
    Qt.QWidget.__init__(self)
    self.setWindowTitle("Tempate Qt")
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

    self.settings = Qt.QSettings("GNU Radio", "tempate_qt")
    self.restoreGeometry(self.settings.value("geometry").toByteArray())

    self.qtgui_const_sink_x_0 = qtgui.const_sink_c(
        1024, #size
        "", #name
        self.num_channels #number of inputs
    )
    self.qtgui_const_sink_x_0.set_update_time(0.10)
    self.qtgui_const_sink_x_0.set_y_axis(-2, 2)
    self.qtgui_const_sink_x_0.set_x_axis(-2, 2)
    self.qtgui_const_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
    self.qtgui_const_sink_x_0.enable_autoscale(False)
    self.qtgui_const_sink_x_0.enable_grid(False)

    if not True:
      self.qtgui_const_sink_x_0.disable_legend()

    labels = ["", "", "", "", "",
              "", "", "", "", ""]
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
    for i in xrange(self.num_channels):
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

    #########

    self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            1024, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            self.samp_rate, #bw
            "", #name
            (self.num_channels) #number of inputs
    )
    self.qtgui_freq_sink_x_0.set_update_time(0.10)
    self.qtgui_freq_sink_x_0.set_y_axis(-140, 10)
    self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
    self.qtgui_freq_sink_x_0.enable_autoscale(False)
    self.qtgui_freq_sink_x_0.enable_grid(False)
    self.qtgui_freq_sink_x_0.set_fft_average(1.0)
    self.qtgui_freq_sink_x_0.enable_control_panel(False)

    if not True:
      self.qtgui_freq_sink_x_0.disable_legend()

    if "complex" == "float" or "complex" == "msg_float":
      self.qtgui_freq_sink_x_0.set_plot_pos_half(not True)

    labels = ["", "", "", "", "",
              "", "", "", "", ""]
    widths = [1, 1, 1, 1, 1,
              1, 1, 1, 1, 1]
    colors = ["blue", "red", "green", "black", "cyan",
              "magenta", "yellow", "dark red", "dark green", "dark blue"]
    alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
              1.0, 1.0, 1.0, 1.0, 1.0]
    for i in xrange(self.num_channels):
        if len(labels[i]) == 0:
            self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
        else:
            self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
        self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
        self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
        self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

    self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.pyqwidget(), Qt.QWidget)
    self.top_layout.addWidget(self._qtgui_freq_sink_x_0_win)
