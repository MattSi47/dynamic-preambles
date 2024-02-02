/* -*- c++ -*- */
/*
 * Copyright 2024 Uconn Senior Design Team 2402.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_UCONN2402_LFMCHIRPXCORR_H
#define INCLUDED_UCONN2402_LFMCHIRPXCORR_H

#include <gnuradio/UConn2402/api.h>
#include <gnuradio/block.h>

namespace gr {
  namespace UConn2402 {

    /*!
     * \brief <+description of block+>
     * \ingroup UConn2402
     *
     */
    class UCONN2402_API LFMChirpXCorr : virtual public gr::block
    {
     public:
      typedef std::shared_ptr<LFMChirpXCorr> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of UConn2402::LFMChirpXCorr.
       *
       * To avoid accidental use of raw pointers, UConn2402::LFMChirpXCorr's
       * constructor is in a private implementation
       * class. UConn2402::LFMChirpXCorr::make is the public interface for
       * creating new instances.
       */
      static sptr make(int samp_rate, int B, float dur);
    };

  } // namespace UConn2402
} // namespace gr

#endif /* INCLUDED_UCONN2402_LFMCHIRPXCORR_H */
