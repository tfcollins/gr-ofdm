/* -*- c++ -*- */
/*
 * Copyright 2016 <+YOU OR YOUR COMPANY+>.
 *
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 *
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifndef INCLUDED_OFDM_OFDM_MRX_FRAME_SINK_IMPL_H
#define INCLUDED_OFDM_OFDM_MRX_FRAME_SINK_IMPL_H

#include <ofdm/ofdm_mrx_frame_sink.h>

namespace gr {
  namespace ofdm {

    class ofdm_mrx_frame_sink_impl : public ofdm_mrx_frame_sink
    {
    private:
      enum state_t {STATE_SYNC_SEARCH, STATE_HAVE_SYNC, STATE_HAVE_HEADER};

      static const int MAX_PKT_LEN    = 4096;
      static const int HEADERBYTELEN   = 4;

      msg_queue::sptr  d_target_queue;	// where to send the packet when received
      state_t            d_state;
      unsigned int       d_header;		// header bits
      int                d_headerbytelen_cnt;	// how many so far

      char              *d_bytes_out;           // hold the current bytes produced by the demapper

      int                d_occupied_carriers;
      unsigned int       d_byte_offset;
      unsigned int       d_partial_byte;

      char               d_packet[MAX_PKT_LEN];    // assembled payload
      int 	         d_packetlen;              // length of packet
      int                d_packet_whitener_offset; // offset into whitener string to use
      int		 d_packetlen_cnt;          // how many so far
      int       d_sink_number;

      gr_complex * d_derotated_output;  // Pointer to output stream to send deroated symbols out
      std::vector<gr_complex*> d_derotated_outputs;
      std::vector<gr_complex*> d_notderotated_outputs;


      std::vector<std::vector<gr_complex> > d_unequalized_header;
      std::vector<std::vector<gr_complex> > d_chan_est;

      std::vector<gr_complex>    d_sym_position;
      std::vector<char>          d_sym_value_out;
      std::vector<gr_complex>    d_dfe;
      unsigned int d_nbits;

      char d_resid;
      unsigned int d_nresid;
      float d_phase;
      float d_freq;
      float d_phase_gain;
      float d_freq_gain;
      float d_eq_gain;

      std::vector<int> d_subcarrier_map;

    protected:
      void enter_search();
      void enter_have_sync();
      void enter_have_header();
      void send_message_dfe();

      bool header_ok()
      {
	   // confirm that two copies of header info are identical
	   return ((d_header >> 16) ^ (d_header & 0xffff)) == 0;
      }

      char slicer(const gr_complex x);
      unsigned int demapper(gr_vector_const_void_star &input_items,
			    char *out);

      bool set_sym_value_out(const std::vector<gr_complex> &sym_position,
			     const std::vector<char> &sym_value_out);

      void send_message(char* messages_data, int length);

    public:
      ofdm_mrx_frame_sink_impl(const std::vector<gr_complex> &sym_position,
			   const std::vector<char> &sym_value_out,
			   msg_queue::sptr target_queue,
			   int occupied_tones,
			   float phase_gain=0.25, float freq_gain=0.25*0.25/4, int num_inputs=2);
      ~ofdm_mrx_frame_sink_impl();

      int work(int noutput_items,
	       gr_vector_const_void_star &input_items,
	       gr_vector_void_star &output_items);
    };

} /* namespace ofdm */
} /* namespace gr */

#endif /* INCLUDED_GR_OFDM_WRX_FRAME_SINK_IMPL_H */
