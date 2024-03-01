/* -*- c++ -*- */
/*
 * Copyright 2024 UConn SD 2402.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#include <gnuradio/io_signature.h>
#include "ArbitrarySync_impl.h"

namespace gr {
  namespace UConn2402 {

    ArbitrarySync::sptr
    ArbitrarySync::make(float threshold, int samples)
    {
      return gnuradio::make_block_sptr<ArbitrarySync_impl>(threshold, samples);
    }


    /*
     * The private constructor
     */
    ArbitrarySync_impl::ArbitrarySync_impl(float threshold, int samples)
      : gr::block("ArbitrarySync",
              gr::io_signature::makev(2, 2, std::vector<int>{ sizeof(gr_complex), sizeof(float) }),
              gr::io_signature::make(1, 1, sizeof(gr_complex)))
    {
      _threshold=threshold;
      _samples=samples;

    }

    /*
     * Our virtual destructor.
     */
    ArbitrarySync_impl::~ArbitrarySync_impl()
    {
    }

    void
    ArbitrarySync_impl::forecast (int noutput_items, gr_vector_int &ninput_items_required)
    {
       ninput_items_required[0] = noutput_items+(_samples-1);
    }

    int
    ArbitrarySync_impl::general_work (int noutput_items,
                       gr_vector_int &ninput_items,
                       gr_vector_const_void_star &input_items,
                       gr_vector_void_star &output_items)
    {
      const gr_complex* in = static_cast<const gr_complex*>(input_items[0]);
      const float* corr = static_cast<const float*>(input_items[1]);
      gr_complex* out = static_cast<gr_complex*>(output_items[0]);

      bool wait = true;
      int samples_out = 0;

      for (int i = 0; i < noutput_items; ++i)
        {
            // If waiting for threshold, check if the input is above threshold
            if (wait)
            {
                if (corr[i] > _threshold)
                {
                    wait = false;
                    samples_out = 0;  // Reset the sample counter
                }
            }

            // Output zeros until the threshold is reached
            if (wait)
            {
                out[i] = gr_complex(0.0f,0.0f);
            }
            else
            {
                // Output the input samples after the threshold is reached
                out[i] = in[i];
                ++samples_out;

                // If "samples" samples have been outputted, reset to output zeros again
                if (samples_out == _samples)
                {
                    wait = true;
                }
            }
        }

      // Do <+signal processing+>
      // Tell runtime system how many input items we consumed on
      // each input stream.
      consume_each(noutput_items);

      // Tell runtime system how many output items we produced.
      return noutput_items;
    }

  } /* namespace UConn2402 */
} /* namespace gr */
