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
#include "eval_chan_est_impl.h"

#include <fstream>
#include <iterator>

#include "rtwtypes.h"
#include <EADF_Estimate.h>

namespace gr {
  namespace ofdm {

    eval_chan_est::sptr
    eval_chan_est::make()
    {
      return gnuradio::get_initial_sptr
        (new eval_chan_est_impl());
    }

    /*
     * The private constructor
     */
    eval_chan_est_impl::eval_chan_est_impl()
      : gr::block("eval_chan_est",
              gr::io_signature::make(0, 0, 0),
              gr::io_signature::make(0, 0, 0))
    {
      d_fft_length = 512;
      d_occupied_carriers = 200;
      int unoccupied_carriers = d_fft_length - d_occupied_carriers;
      d_zeros_on_left = (int)ceil(unoccupied_carriers/2.0);

      d_known_header_iq = readFloatBinaryFile("/tmp/preamble.txt", d_fft_length);
      std::cout<<"Buffer Size: "<<d_known_header_iq.size()<<"\n";

      // Create data subcarrier mapping
      gen_mapping(d_occupied_carriers);

      // Setup inputs
      message_port_register_in(pmt::mp("chan_est"));
      set_msg_handler(pmt::mp("chan_est"),
                boost::bind(&eval_chan_est_impl::set_chan_est, this, _1));

      // Setup ML function
      EADF_Estimate_init();
      antennaCal_not_empty_init();
    }

    /*
     * Our virtual destructor.
     */
    eval_chan_est_impl::~eval_chan_est_impl()
    {
      EADF_Estimate_free();
    }

    void
    eval_chan_est_impl::set_chan_est(pmt::pmt_t msg)
    {
        std::vector<std::vector<gr_complex> > chan_est =
      boost::any_cast<std::vector<std::vector<gr_complex> > >(pmt::any_ref(msg));

      // gr_complex error;
      // // Compare to reference
      // for (int c=0; c<chan_est.size(); c++)
      // {
      // for (int i=0; i<4; i++)
      // {
      //   // error = d_known_header_iq[d_subcarrier_map[i]] - chan_est[c][i];
      //   // std::cout<< "Error: "  << error << "\n";
      //   // std::cout << "True: " << d_known_header_iq[d_subcarrier_map[i]] << std::endl;
      //   // std::cout << "RXed: " << chan_est[c][i] << std::endl;
      //   // std::cout << "Map: " << d_subcarrier_map[i] << std::endl;
      //
      //   std::cout << "True: " << d_known_header_iq[d_subcarrier_map[i]] << " | RXed: " << chan_est[c][i] << std::endl;
      // }
      // std::cout << "--------\n";
      // }

      // Convert to ML Type
      creal_T *ml_chan_ests = new creal_T[4];
      for (int i=0; i < chan_est.size(); i++)
      {
        ml_chan_ests[i].re = (chan_est[i][0]).real();
        ml_chan_ests[i].im = (chan_est[i][0]).imag();
      }
      // ml_chan_ests[3].re = 0;
      // ml_chan_ests[3].im = 0;
      // ml_chan_ests[4].re = 0;
      // ml_chan_ests[4].im = 0;

      // Determine DoA
      double est_azimuth = 0;
      double est_elevation = 0;
      EADF_Estimate(ml_chan_ests, &est_azimuth, &est_elevation);
      // std::cout << "DoA: " << est_azimuth << " | " << est_elevation << std::endl;
      delete ml_chan_ests;

    }

    void eval_chan_est_impl::gen_mapping(int d_occupied_carriers)
    {
      std::string carriers = "FE7F";

      // A bit hacky to fill out carriers to occupied_carriers length
      int diff = (d_occupied_carriers - 4*carriers.length());
      while(diff > 7) {
              carriers.insert(0, "f");
              carriers.insert(carriers.length(), "f");
              diff -= 8;
      }

      // if there's extras left to be processed
      // divide remaining to put on either side of current map
      // all of this is done to stick with the concept of a carrier map string that
      // can be later passed by the user, even though it'd be cleaner to just do this
      // on the carrier map itself
      int diff_left=0;
      int diff_right=0;

      // dictionary to convert from integers to ascii hex representation
      char abc[16] = {'0', '1', '2', '3', '4', '5', '6', '7',
                      '8', '9', 'a', 'b', 'c', 'd', 'e', 'f'};
      if(diff > 0) {
              char c[2] = {0,0};

              diff_left = (int)ceil((float)diff/2.0f); // number of carriers to put on the left side
              c[0] = abc[(1 << diff_left) - 1]; // convert to bits and move to ASCI integer
              carriers.insert(0, c);

              diff_right = diff - diff_left; // number of carriers to put on the right side
              c[0] = abc[0xF^((1 << diff_right) - 1)]; // convert to bits and move to ASCI integer
              carriers.insert(carriers.length(), c);
      }

      // It seemed like such a good idea at the time...
      // because we are only dealing with the occupied_carriers
      // at this point, the diff_left in the following compensates
      // for any offset from the 0th carrier introduced
      int i;
      unsigned int j,k;
      for(i = 0; i < (d_occupied_carriers/4)+diff_left; i++) {
              char c = carriers[i];
              for(j = 0; j < 4; j++) {
                      k = (strtol(&c, NULL, 16) >> (3-j)) & 0x1;
                      if(k) {
                              d_subcarrier_map.push_back(4*i + j - diff_left);
                      }
              }
      }
    }


    /* read binary float file, return as array of float */
    std::vector<gr_complex> eval_chan_est_impl::readFloatBinaryFile(std::string filename_str, int ndata)
    {

      const char* filename = filename_str.c_str();
      FILE *infile=NULL;
      gr_complex *dataread;
      int idx;

      /*open file */
      infile = fopen(filename, "r");
      if(!infile) /*show message and exit if fail opening file */
      {
      printf("error opening file %s \n", filename);
      exit(0);
      // return(dataread);
      }

      /*allocated memory/array for float data */
      // dataread = (gr_complex*) calloc(ndata, sizeof(gr_complex));
      dataread = new gr_complex[ndata];

      /*read file and save as float data */
      int data = fread(dataread, sizeof(gr_complex), ndata, infile);
      // std::cout<<"data: "<<data<<"\n";

      /* close file */
      fclose(infile);

      // Convert to vector
      std::vector<gr_complex> header_iq(d_occupied_carriers);

      // Remove FFT padding
      for(int j=0; j<d_occupied_carriers; j++)
        header_iq[j] = dataread[j+d_zeros_on_left];


      return(header_iq);
    }


    // void
    // eval_chan_est_impl::forecast (int noutput_items, gr_vector_int &ninput_items_required)
    // {
    //   /* <+forecast+> e.g. ninput_items_required[0] = noutput_items */
    // }
    //
    // int
    // eval_chan_est_impl::general_work (int noutput_items,
    //                    gr_vector_int &ninput_items,
    //                    gr_vector_const_void_star &input_items,
    //                    gr_vector_void_star &output_items)
    // {
    //   const <+ITYPE+> *in = (const <+ITYPE+> *) input_items[0];
    //   <+OTYPE+> *out = (<+OTYPE+> *) output_items[0];
    //
    //   // Do <+signal processing+>
    //   // Tell runtime system how many input items we consumed on
    //   // each input stream.
    //   consume_each (noutput_items);
    //
    //   // Tell runtime system how many output items we produced.
    //   return noutput_items;
    // }

  } /* namespace ofdm */
} /* namespace gr */
