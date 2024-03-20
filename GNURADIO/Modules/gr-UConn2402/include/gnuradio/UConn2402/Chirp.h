/* -*- c++ -*- */
/*
 * Copyright 2024 UConn SD 2402.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_UCONN2402_CHIRP_H
#define INCLUDED_UCONN2402_CHIRP_H

#include <gnuradio/UConn2402/api.h>
#include <gnuradio/tagged_stream_block.h>

namespace gr {
  namespace UConn2402 {

    /*!
     * \brief <+description of block+>
     * \ingroup UConn2402
     *
     */
    class UCONN2402_API Chirp : virtual public gr::tagged_stream_block
    {
     public:
      typedef std::shared_ptr<Chirp> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of UConn2402::Chirp.
       *
       * To avoid accidental use of raw pointers, UConn2402::Chirp's
       * constructor is in a private implementation
       * class. UConn2402::Chirp::make is the public interface for
       * creating new instances.
       */
      static sptr make(int samp_rate, int B, float dur, bool chirp_op, const std::string& pcklen);
    };

  } // namespace UConn2402
} // namespace gr

#endif /* INCLUDED_UCONN2402_CHIRP_H */
