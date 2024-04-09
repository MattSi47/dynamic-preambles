/* -*- c++ -*- */
/*
 * Copyright 2024 UConn SD2402.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_UCONN2402_FFTXCORR_H
#define INCLUDED_UCONN2402_FFTXCORR_H

#include <gnuradio/UConn2402/api.h>
#include <gnuradio/block.h>

namespace gr {
  namespace UConn2402 {

    /*!
     * \brief <+description of block+>
     * \ingroup UConn2402
     *
     */
    class UCONN2402_API fftXCorr : virtual public gr::block
    {
     public:
      typedef std::shared_ptr<fftXCorr> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of UConn2402::fftXCorr.
       *
       * To avoid accidental use of raw pointers, UConn2402::fftXCorr's
       * constructor is in a private implementation
       * class. UConn2402::fftXCorr::make is the public interface for
       * creating new instances.
       */
      static sptr make(const char* filename);
    };

  } // namespace UConn2402
} // namespace gr

#endif /* INCLUDED_UCONN2402_FFTXCORR_H */
