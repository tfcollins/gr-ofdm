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

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include "preamble_equalize_impl.h"

#include <volk/volk.h>

namespace gr {
  namespace ofdm {

    preamble_equalize::sptr
    preamble_equalize::make(int fft_length, int cplen, int occupied_carriers)
    {
      return gnuradio::get_initial_sptr
        (new preamble_equalize_impl(fft_length, cplen, occupied_carriers));
    }

    std::vector<int>
    get_in_sizeofs(int fft_length, int occupied_carriers)
    {
            std::vector<int> in_sizeofs;
            in_sizeofs.push_back(sizeof(gr_complex)*fft_length);
            in_sizeofs.push_back(sizeof(gr_complex)*occupied_carriers);
            in_sizeofs.push_back(sizeof(int));
            return in_sizeofs;
    }

    /*
     * The private constructor
     */
    preamble_equalize_impl::preamble_equalize_impl(int fft_length, int cplen, int occupied_carriers)
      : gr::sync_block("preamble_equalize",
              gr::io_signature::makev(3, 3, get_in_sizeofs(fft_length, occupied_carriers) ),
              gr::io_signature::make(1, 1, sizeof(gr_complex)*occupied_carriers )),
        d_occupied_carriers(occupied_carriers),
        d_fft_length(fft_length)
    {
        int unoccupied_carriers = d_fft_length - d_occupied_carriers;
        d_zeros_on_left = (int)ceil(unoccupied_carriers/2.0);
    }

    /*
     * Our virtual destructor.
     */
    preamble_equalize_impl::~preamble_equalize_impl()
    {
    }

    int
    preamble_equalize_impl::work(int noutput_items,
        gr_vector_const_void_star &input_items,
        gr_vector_void_star &output_items)
    {
        gr_complex *out = (gr_complex *) output_items[0];

        const gr_complex *symbols = (const gr_complex *) input_items[0];
        const gr_complex *h_est = (const gr_complex *) input_items[1];
        const int *coarse_freq = (const int *) input_items[2];

        for(unsigned int i = 0; i < noutput_items; i++)
        {
            //   out[i] = d_hestimate[i]*symbol[i+zeros_on_left+d_coarse_freq];

          volk_32fc_x2_multiply_32fc(out+d_occupied_carriers*i,
                                    h_est+d_occupied_carriers*i,
                                    symbols+d_fft_length*i+d_zeros_on_left+coarse_freq[i],
                                    d_occupied_carriers);
        }

        // for (int k=0; k< noutput_items)
        // {
        //     for (int g=0; g<d_occupied_carriers; g++ )
        //     out[g+k*d_occupied_carriers] = h_est[g+k*d_occupied_carriers]*symbols
        // }

      // Tell runtime system how many output items we produced.
      return noutput_items;
    }

  } /* namespace ofdm */
} /* namespace gr */
