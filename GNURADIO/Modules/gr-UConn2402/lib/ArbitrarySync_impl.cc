/* -*- c++ -*- */
/*
 * Copyright 2024 UConn SD 2402.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#include "ArbitrarySync_impl.h"
#include <gnuradio/io_signature.h>

namespace gr {
namespace UConn2402 {

ArbitrarySync::sptr ArbitrarySync::make(float threshold, int samples)
{
    return gnuradio::make_block_sptr<ArbitrarySync_impl>(threshold, samples);
}


/*
 * The private constructor
 */
ArbitrarySync_impl::ArbitrarySync_impl(float threshold, int samples)
    : gr::block("ArbitrarySync",
                gr::io_signature::makev(
                    2, 2, std::vector<int>{ sizeof(gr_complex), sizeof(float) }),
                gr::io_signature::make(1, 1, sizeof(gr_complex)))
{
    d_state = STATE_IDLE;
    _threshold = threshold;
    _samples = samples;
    sampidx = 0;
}

/*
 * Our virtual destructor.
 */
ArbitrarySync_impl::~ArbitrarySync_impl() {}

void ArbitrarySync_impl::forecast(int noutput_items, gr_vector_int& ninput_items_required)
{
    ninput_items_required[0] = noutput_items;
    ninput_items_required[1] = noutput_items;
}

int ArbitrarySync_impl::general_work(int noutput_items,
                                     gr_vector_int& ninput_items,
                                     gr_vector_const_void_star& input_items,
                                     gr_vector_void_star& output_items)
{
    const gr_complex* in = static_cast<const gr_complex*>(input_items[0]);
    const float* corr = static_cast<const float*>(input_items[1]);
    gr_complex* out = static_cast<gr_complex*>(output_items[0]);

    switch (d_state) {
    case STATE_IDLE: {

        int ii = 0;

        while (ii < noutput_items) {

            if (corr[ii] > _threshold) {

                d_state = STATE_DATA;
                std::cout << "Packet detected" << std::endl;
                break;
            }
            out[ii] = gr_complex(0.0f, 0.0f);
            ii++;
        }


        consume_each(ii);
        return ii;
    }

    case STATE_DATA: {
        int idx = 0;
        while (idx < noutput_items) {

            out[idx] = in[idx];
            sampidx++;
            idx++;

            if (sampidx >= _samples) {
                std::cout << "Packet sent: " << sampidx <<std::endl;
                sampidx = 0;
                d_state = STATE_IDLE;
                break;
            }
        }
        consume_each(sampidx);
        return (sampidx);
    }
    default: {
        std::cout << "sync block state error" << std::endl;
        d_state = STATE_IDLE;
        consume_each(0);
        return (0);
    }
    }
}

} /* namespace UConn2402 */
} /* namespace gr */
