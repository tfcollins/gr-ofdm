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
#include "frame_logger_impl.h"

#include <fstream>
#include <string>

namespace gr {
  namespace ofdm {

    frame_logger::sptr
    frame_logger::make( int num_inputs, int occupied_tones, std::string logfilename_base)
    {
      return gnuradio::get_initial_sptr
        (new frame_logger_impl(num_inputs, occupied_tones, logfilename_base));
    }

    /*
     * The private constructor
     */
    frame_logger_impl::frame_logger_impl( int num_inputs, int occupied_tones, std::string logfilename_base)
      : gr::sync_block("frame_logger",
              gr::io_signature::make(num_inputs, num_inputs, sizeof(gr_complex*occupied_tones)),
              gr::io_signature::make(0, 0, 0))
    {
        // Open log files
        std::ofstream d_logfile;
        d_logfile.open (logfilename);

        // Determine how long a frame should be
        d_frameLength = occupied_tones*modscheme*packet_size;

        // Inputs must be in integers of frames
        set_output_multiple(d_frameLength);
    }

    /*
     * Our virtual destructor.
     */
    frame_logger_impl::~frame_logger_impl()
    {
        // Close file
        d_logfile.close();
    }

    int
    frame_logger_impl::work(int noutput_items,
        gr_vector_const_void_star &input_items,
        gr_vector_void_star &output_items)
    {

      int frames = noutput_items/d_frameLength;

      for (int frame=0; frame<frames; frame++)
      {
          // // Write frame data to file

          // Write check result

          // Write decoded data

          // Write equalized data

          // Write unequalized data

      }

      // Tell runtime system how many output items we produced.
      return noutput_items;
    }

  } /* namespace ofdm */
} /* namespace gr */
