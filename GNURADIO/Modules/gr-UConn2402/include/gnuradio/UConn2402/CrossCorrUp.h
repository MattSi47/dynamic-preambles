/* -*- c++ -*- */
/*
 * Copyright 2024 UConn Senior Design Team 2402.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_UCONN2402_CROSSCORRUP_H
#define INCLUDED_UCONN2402_CROSSCORRUP_H

#include <gnuradio/UConn2402/api.h>
#include <gnuradio/block.h>

namespace gr {
  namespace UConn2402 {

    /*!
     * \brief <+description of block+>
     * \ingroup UConn2402
     *
     */
    class UCONN2402_API CrossCorrUp : virtual public gr::block
    {
     public:
      typedef std::shared_ptr<CrossCorrUp> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of UConn2402::CrossCorrUp.
       *
       * To avoid accidental use of raw pointers, UConn2402::CrossCorrUp's
       * constructor is in a private implementation
       * class. UConn2402::CrossCorrUp::make is the public interface for
       * creating new instances.
       */
      static sptr make();
    };

  } // namespace UConn2402
} // namespace gr

#endif /* INCLUDED_UCONN2402_CROSSCORRUP_H */
