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

#ifndef INCLUDED_OFDM_PREAMBLE_EQUALIZE_IMPL_H
#define INCLUDED_OFDM_PREAMBLE_EQUALIZE_IMPL_H

#include <ofdm/preamble_equalize.h>

namespace gr {
  namespace ofdm {

    class preamble_equalize_impl : public preamble_equalize
    {
     private:
         int d_occupied_carriers;
         int d_fft_length;
         int d_zeros_on_left;

     public:
      preamble_equalize_impl(int fft_length, int cplen, int occupied_carriers);
      ~preamble_equalize_impl();

      // Where all the action really happens
      int work(int noutput_items,
         gr_vector_const_void_star &input_items,
         gr_vector_void_star &output_items);
    };

  } // namespace ofdm
} // namespace gr

#endif /* INCLUDED_OFDM_PREAMBLE_EQUALIZE_IMPL_H */
