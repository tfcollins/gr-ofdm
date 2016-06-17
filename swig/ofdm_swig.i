/* -*- c++ -*- */

#define OFDM_API

%include "gnuradio.i"			// the common stuff

//load generated python docstrings
%include "ofdm_swig_doc.i"

%{
#include "ofdm/ofdm_frame_sink.h"
%}


%include "ofdm/ofdm_frame_sink.h"
GR_SWIG_BLOCK_MAGIC2(ofdm, ofdm_frame_sink);
