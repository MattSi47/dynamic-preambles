/* -*- c++ -*- */
/*
 * Copyright 2024 UConn SD2402.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_UCONN2402_ARBITRARYSYNC2_H
#define INCLUDED_UCONN2402_ARBITRARYSYNC2_H

#include <gnuradio/UConn2402/api.h>
#include <gnuradio/block.h>

namespace gr {
  namespace UConn2402 {

    /*!
     * \brief <+description of block+>
     * \ingroup UConn2402
     *
     */
    class UCONN2402_API ArbitrarySync2 : virtual public gr::block
    {
     public:
      typedef std::shared_ptr<ArbitrarySync2> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of UConn2402::ArbitrarySync2.
       *
       * To avoid accidental use of raw pointers, UConn2402::ArbitrarySync2's
       * constructor is in a private implementation
       * class. UConn2402::ArbitrarySync2::make is the public interface for
       * creating new instances.
       */
      static sptr make(float threshold, int samples);
    };

  } // namespace UConn2402
} // namespace gr

#endif /* INCLUDED_UCONN2402_ARBITRARYSYNC2_H */
