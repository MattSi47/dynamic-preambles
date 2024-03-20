/* -*- c++ -*- */
/*
 * Copyright 2024 UConn SD 2402.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_UCONN2402_ArbitrarySync2_IMPL_H
#define INCLUDED_UCONN2402_ArbitrarySync2_IMPL_H

enum STATE_OPTIONS { STATE_IDLE, STATE_DATA };
#include <gnuradio/UConn2402/ArbitrarySync2.h>

namespace gr {
  namespace UConn2402 {

    class ArbitrarySync2_impl : public ArbitrarySync2
    {
     private:
      float _threshold;
      int _samples;
      int sampidx = 0; 
      int startindex = 0; 
      bool stop_flg = 0;
      STATE_OPTIONS d_state;
      
     public:
      ArbitrarySync2_impl(float threshold, int samples);
      ~ArbitrarySync2_impl();
      

      // Where all the action really happens
      void forecast (int noutput_items, gr_vector_int &ninput_items_required);
      void stop(pmt::pmt_t stop);

      int general_work(int noutput_items,
           gr_vector_int &ninput_items,
           gr_vector_const_void_star &input_items,
           gr_vector_void_star &output_items);

    };

  } // namespace UConn2402
} // namespace gr

#endif /* INCLUDED_UCONN2402_ArbitrarySync2_IMPL_H */
