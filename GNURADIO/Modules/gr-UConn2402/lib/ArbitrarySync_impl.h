/* -*- c++ -*- */
/*
 * Copyright 2024 UConn SD 2402.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_UCONN2402_ARBITRARYSYNC_IMPL_H
#define INCLUDED_UCONN2402_ARBITRARYSYNC_IMPL_H

#include <gnuradio/UConn2402/ArbitrarySync.h>

namespace gr {
  namespace UConn2402 {

    class ArbitrarySync_impl : public ArbitrarySync
    {
     private:
      float _threshold;
      int _samples;
      
     public:
      ArbitrarySync_impl(float threshold, int samples);
      ~ArbitrarySync_impl();

      // Where all the action really happens
      void forecast (int noutput_items, gr_vector_int &ninput_items_required);

      int general_work(int noutput_items,
           gr_vector_int &ninput_items,
           gr_vector_const_void_star &input_items,
           gr_vector_void_star &output_items);

    };

  } // namespace UConn2402
} // namespace gr

#endif /* INCLUDED_UCONN2402_ARBITRARYSYNC_IMPL_H */
