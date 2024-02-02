/* -*- c++ -*- */
/*
 * Copyright 2024 UConn Senior Design Team 2402.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_UCONN2402_CROSSCORRUP_IMPL_H
#define INCLUDED_UCONN2402_CROSSCORRUP_IMPL_H

#include <gnuradio/UConn2402/CrossCorrUp.h>

namespace gr {
  namespace UConn2402 {

    class CrossCorrUp_impl : public CrossCorrUp
    {
     private:
      // Nothing to declare in this block.
      gr_complex f_array_a[160];

     public:
      CrossCorrUp_impl();
      ~CrossCorrUp_impl();

      // Where all the action really happens
      void forecast (int noutput_items, gr_vector_int &ninput_items_required);

      int general_work(int noutput_items,
           gr_vector_int &ninput_items,
           gr_vector_const_void_star &input_items,
           gr_vector_void_star &output_items);

    float CrossCorr(const gr_complex* input, gr_complex* pattern);
    };

  } // namespace UConn2402
} // namespace gr

#endif /* INCLUDED_UCONN2402_CROSSCORRUP_IMPL_H */
