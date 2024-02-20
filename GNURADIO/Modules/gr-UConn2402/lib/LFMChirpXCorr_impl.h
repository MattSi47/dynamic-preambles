/* -*- c++ -*- */
/*
 * Copyright 2024 Uconn Senior Design Team 2402.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_UCONN2402_LFMCHIRPXCORR_IMPL_H
#define INCLUDED_UCONN2402_LFMCHIRPXCORR_IMPL_H

#include <gnuradio/UConn2402/LFMChirpXCorr.h>

namespace gr {
  namespace UConn2402 {

    class LFMChirpXCorr_impl : public LFMChirpXCorr
    {
     private:
      int _samp_rate;
      int _B;
      float _dur;
	int numsamples;
      float in_sum_up;
      float in_sum_down;

      gr_complex* Up_array;
      gr_complex* Down_array;
	

     public:
      LFMChirpXCorr_impl(int samp_rate, int B, float dur);
      ~LFMChirpXCorr_impl();

      // Where all the action really happens
      void forecast (int noutput_items, gr_vector_int &ninput_items_required);

      int general_work(int noutput_items,
           gr_vector_int &ninput_items,
           gr_vector_const_void_star &input_items,
           gr_vector_void_star &output_items);

  
    
//float XCorr(const gr_complex* input, gr_complex* pattern);
    };

  } // namespace UConn2402
} // namespace gr

#endif /* INCLUDED_UCONN2402_LFMCHIRPXCORR_IMPL_H */
