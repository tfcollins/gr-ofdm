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

#ifndef INCLUDED_OFDM_EVAL_CHAN_EST_IMPL_H
#define INCLUDED_OFDM_EVAL_CHAN_EST_IMPL_H

#include <ofdm/eval_chan_est.h>

namespace gr {
  namespace ofdm {

    class eval_chan_est_impl : public eval_chan_est
    {
     private:
      std::vector<int> d_subcarrier_map;
      std::vector<gr_complex> d_known_header_iq;
      int d_zeros_on_left;
      int d_fft_length;
      int d_occupied_carriers;

     public:
      eval_chan_est_impl();
      ~eval_chan_est_impl();

      void set_chan_est(pmt::pmt_t msg);
      std::vector<gr_complex> readFloatBinaryFile(std::string filename, int ndata);
      void gen_mapping(int d_occupied_carriers);

      // // Where all the action really happens
      // void forecast (int noutput_items, gr_vector_int &ninput_items_required);
      //
      // int general_work(int noutput_items,
      //      gr_vector_int &ninput_items,
      //      gr_vector_const_void_star &input_items,
      //      gr_vector_void_star &output_items);
    };

  } // namespace ofdm
} // namespace gr

#endif /* INCLUDED_OFDM_EVAL_CHAN_EST_IMPL_H */
