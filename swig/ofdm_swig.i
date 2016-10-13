/* -*- c++ -*- */

#define OFDM_API

%include "gnuradio.i"			// the common stuff

//load generated python docstrings
%include "ofdm_swig_doc.i"

%{
#include "ofdm/ofdm_frame_sink.h"
#include "ofdm/ofdm_mrx_frame_sink.h"
#include "ofdm/eval_chan_est.h"
#include "ofdm/frame_acquisition.h"
#include "ofdm/preamble_equalize.h"
//#include "ofdm/frame_logger.h"
%}


%include "ofdm/ofdm_frame_sink.h"
GR_SWIG_BLOCK_MAGIC2(ofdm, ofdm_frame_sink);
%include "ofdm/ofdm_mrx_frame_sink.h"
GR_SWIG_BLOCK_MAGIC2(ofdm, ofdm_mrx_frame_sink);

//%include "ofdm/frame_logger.h"
//GR_SWIG_BLOCK_MAGIC2(ofdm, frame_logger);

%include "ofdm/eval_chan_est.h"
GR_SWIG_BLOCK_MAGIC2(ofdm, eval_chan_est);
%include "ofdm/frame_acquisition.h"
GR_SWIG_BLOCK_MAGIC2(ofdm, frame_acquisition);
%include "ofdm/preamble_equalize.h"
GR_SWIG_BLOCK_MAGIC2(ofdm, preamble_equalize);
