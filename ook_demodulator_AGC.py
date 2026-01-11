#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Agc version of demodulator
# Author: PANAGIVTHS
# GNU Radio version: 3.10.9.2

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from gnuradio import analog
from gnuradio import blocks
import pmt
from gnuradio import digital
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import sip



class ook_demodulator_AGC(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Agc version of demodulator", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Agc version of demodulator")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
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

        self.settings = Qt.QSettings("GNU Radio", "ook_demodulator_AGC")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 1000000
        self.decim = decim = 20
        self.bit_samples = bit_samples = 700
        self.samp_rate_new = samp_rate_new = samp_rate / decim
        self.n_keep = n_keep = int(bit_samples * 0.3)
        self.bitss = bitss = 4
        self.sps = sps = samp_rate_new / bitss
        self.selected_frequency = selected_frequency = 1333313000
        self.n_skip = n_skip = int((bit_samples - n_keep) / 2)
        self.cutoff_linear_vol = cutoff_linear_vol = 0.5

        ##################################################
        # Blocks
        ##################################################

        self._selected_frequency_range = qtgui.Range(80000, 3650000000, 10000, 1333313000, 200)
        self._selected_frequency_win = qtgui.RangeWidget(self._selected_frequency_range, self.set_selected_frequency, "'selected_frequency'", "counter_slider", int, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._selected_frequency_win)
        self.qtgui_time_sink_x_1_0 = qtgui.time_sink_f(
            256, #size
            samp_rate_new, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_1_0.set_update_time(0.25)
        self.qtgui_time_sink_x_1_0.set_y_axis(-1, 2)

        self.qtgui_time_sink_x_1_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_1_0.enable_tags(True)
        self.qtgui_time_sink_x_1_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_1_0.enable_autoscale(False)
        self.qtgui_time_sink_x_1_0.enable_grid(False)
        self.qtgui_time_sink_x_1_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_1_0.enable_control_panel(False)
        self.qtgui_time_sink_x_1_0.enable_stem_plot(False)


        labels = ['RX Threshold', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_1_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_1_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_1_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_1_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_1_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_1_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_1_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_1_0_win = sip.wrapinstance(self.qtgui_time_sink_x_1_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_1_0_win)
        self.low_pass_filter_0 = filter.fir_filter_ccf(
            decim,
            firdes.low_pass(
                1,
                samp_rate,
                2500,
                5000,
                window.WIN_HAMMING,
                6.76))
        self.fir_filter_xxx_1 = filter.fir_filter_fff(bit_samples, [0]*n_skip + [1]*n_keep + [0]*(bit_samples - n_keep - n_skip))
        self.fir_filter_xxx_1.declare_sample_delay(0)
        self.digital_symbol_sync_xx_0 = digital.symbol_sync_ff(
            digital.TED_EARLY_LATE,
            sps,
            0.045,
            1.0,
            1.0,
            0.1,
            bit_samples,
            digital.constellation_bpsk().base(),
            digital.IR_MMSE_8TAP,
            128,
            [])
        self.digital_correlate_access_code_tag_xx_0 = digital.correlate_access_code_tag_bb('10101001', 1, 'frame_start')
        self.digital_binary_slicer_fb_0 = digital.binary_slicer_fb()
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_threshold_ff_0 = blocks.threshold_ff(cutoff_linear_vol, cutoff_linear_vol, 0)
        self.blocks_tagged_stream_align_0 = blocks.tagged_stream_align(gr.sizeof_char*1, 'frame_start')
        self.blocks_pack_k_bits_bb_0 = blocks.pack_k_bits_bb(8)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_gr_complex*1, '/home/panagivths/Downloads/hello_world-capture.raw', False, 0, 0)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_char*1, '/home/panagivths/Documents/GitHub/ECE455-Hardware-Security/output.txt', False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.blocks_complex_to_mag_0 = blocks.complex_to_mag(1)
        self.blocks_add_const_vxx_0 = blocks.add_const_ff((-(n_keep / 2.0)))
        self.analog_pwr_squelch_xx_0 = analog.pwr_squelch_cc((-50), (1e-4), 0, True)
        self.analog_feedforward_agc_cc_0 = analog.feedforward_agc_cc((int(sps * bitss / 10)), 1.0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_feedforward_agc_cc_0, 0), (self.blocks_complex_to_mag_0, 0))
        self.connect((self.analog_pwr_squelch_xx_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.digital_binary_slicer_fb_0, 0))
        self.connect((self.blocks_complex_to_mag_0, 0), (self.digital_symbol_sync_xx_0, 0))
        self.connect((self.blocks_complex_to_mag_0, 0), (self.qtgui_time_sink_x_1_0, 0))
        self.connect((self.blocks_file_source_0, 0), (self.analog_pwr_squelch_xx_0, 0))
        self.connect((self.blocks_pack_k_bits_bb_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.blocks_tagged_stream_align_0, 0), (self.blocks_pack_k_bits_bb_0, 0))
        self.connect((self.blocks_threshold_ff_0, 0), (self.fir_filter_xxx_1, 0))
        self.connect((self.blocks_throttle_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.digital_correlate_access_code_tag_xx_0, 0))
        self.connect((self.digital_correlate_access_code_tag_xx_0, 0), (self.blocks_tagged_stream_align_0, 0))
        self.connect((self.digital_symbol_sync_xx_0, 0), (self.blocks_threshold_ff_0, 0))
        self.connect((self.fir_filter_xxx_1, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.analog_feedforward_agc_cc_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "ook_demodulator_AGC")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_samp_rate_new(self.samp_rate / self.decim)
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, 2500, 5000, window.WIN_HAMMING, 6.76))

    def get_decim(self):
        return self.decim

    def set_decim(self, decim):
        self.decim = decim
        self.set_samp_rate_new(self.samp_rate / self.decim)

    def get_bit_samples(self):
        return self.bit_samples

    def set_bit_samples(self, bit_samples):
        self.bit_samples = bit_samples
        self.set_n_keep(int(self.bit_samples * 0.3))
        self.set_n_skip(int((self.bit_samples - self.n_keep) / 2))
        self.fir_filter_xxx_1.set_taps([0]*self.n_skip + [1]*self.n_keep + [0]*(self.bit_samples - self.n_keep - self.n_skip))

    def get_samp_rate_new(self):
        return self.samp_rate_new

    def set_samp_rate_new(self, samp_rate_new):
        self.samp_rate_new = samp_rate_new
        self.set_sps(self.samp_rate_new / self.bitss)
        self.qtgui_time_sink_x_1_0.set_samp_rate(self.samp_rate_new)

    def get_n_keep(self):
        return self.n_keep

    def set_n_keep(self, n_keep):
        self.n_keep = n_keep
        self.set_n_skip(int((self.bit_samples - self.n_keep) / 2))
        self.blocks_add_const_vxx_0.set_k((-(self.n_keep / 2.0)))
        self.fir_filter_xxx_1.set_taps([0]*self.n_skip + [1]*self.n_keep + [0]*(self.bit_samples - self.n_keep - self.n_skip))

    def get_bitss(self):
        return self.bitss

    def set_bitss(self, bitss):
        self.bitss = bitss
        self.set_sps(self.samp_rate_new / self.bitss)

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.digital_symbol_sync_xx_0.set_sps(self.sps)

    def get_selected_frequency(self):
        return self.selected_frequency

    def set_selected_frequency(self, selected_frequency):
        self.selected_frequency = selected_frequency

    def get_n_skip(self):
        return self.n_skip

    def set_n_skip(self, n_skip):
        self.n_skip = n_skip
        self.fir_filter_xxx_1.set_taps([0]*self.n_skip + [1]*self.n_keep + [0]*(self.bit_samples - self.n_keep - self.n_skip))

    def get_cutoff_linear_vol(self):
        return self.cutoff_linear_vol

    def set_cutoff_linear_vol(self, cutoff_linear_vol):
        self.cutoff_linear_vol = cutoff_linear_vol
        self.blocks_threshold_ff_0.set_hi(self.cutoff_linear_vol)
        self.blocks_threshold_ff_0.set_lo(self.cutoff_linear_vol)




def main(top_block_cls=ook_demodulator_AGC, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
