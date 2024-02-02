/* -*- c++ -*- */
/*
 * Copyright 2024 UConn Senior Design Team 2402.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#include <gnuradio/io_signature.h>
#include "CrossCorrDown_impl.h"
#include <gnuradio/io_signature.h>
#include <math.h>

using namespace std; 

namespace gr {
  namespace UConn2402 {

   // #pragma message("set the following appropriately and remove this warning")
    using input_type = gr_complex;
   // #pragma message("set the following appropriately and remove this warning")
    using output_type = float;
    CrossCorrDown::sptr
    CrossCorrDown::make()
    {
      return gnuradio::make_block_sptr<CrossCorrDown_impl>(
        );
    }


    /*
     * The private constructor
     */
    CrossCorrDown_impl::CrossCorrDown_impl()
      : gr::block("CrossCorrDown",
              gr::io_signature::make(1 /* min inputs */, 1 /* max inputs */, sizeof(input_type)),
              gr::io_signature::make(1 /* min outputs */, 1 /*max outputs */, sizeof(output_type)))
    {}

    /*
     * Our virtual destructor.
     */
    CrossCorrDown_impl::~CrossCorrDown_impl() {}

    float CrossCorrDown_impl::CrossCorr(const gr_complex* input, gr_complex* pattern)
{

    gr_complex sum = 0, sum_abs_1 = 0, sum_abs_2 = 0;

    for (int i = 0; i < 160; i++) {
        sum += (input[i] * pattern[i]);
        sum_abs_1 += abs(input[i]) * abs(input[i]);
        sum_abs_2 += abs(pattern[i]) * abs(pattern[i]);
    }
    return real((abs(sum) / sqrt(sum_abs_1) / sqrt(sum_abs_2)));
}

    void CrossCorrDown_impl::forecast (int noutput_items, gr_vector_int &ninput_items_required)
    {
      ninput_items_required[0] = noutput_items + 160;
    }

    int
    CrossCorrDown_impl::general_work (int noutput_items,
                       gr_vector_int &ninput_items,
                       gr_vector_const_void_star &input_items,
                       gr_vector_void_star &output_items)
    {
     static gr_complex f_array_a[160] = {gr_complex(1.000000f,0.000062f), gr_complex(-0.999800f,-0.059799f), gr_complex(0.992863f,0.197824f), gr_complex(-0.955745f,-0.405908f), gr_complex(0.848732f,0.656626f), gr_complex(-0.625251f,-0.888576f), gr_complex(0.254946f,0.999817f), gr_complex(0.237120f,-0.868900f), gr_complex(-0.728495f,0.422759f), gr_complex(0.995161f,0.256628f), gr_complex(-0.803666f,-0.859904f), gr_complex(0.117841f,0.949435f), gr_complex(0.700951f,-0.311545f), gr_complex(-0.983788f,-0.642169f), gr_complex(0.330258f,0.975854f), gr_complex(0.715166f,-0.176462f), gr_complex(-0.905162f,-0.879754f), gr_complex(-0.160048f,0.669832f), gr_complex(0.999277f,0.627092f), gr_complex(-0.156612f,-0.826269f), gr_complex(-0.980665f,-0.563327f), gr_complex(0.156490f,0.778828f), gr_complex(0.999287f,0.742721f), gr_complex(0.160416f,-0.475047f), gr_complex(-0.904951f,-0.984406f), gr_complex(-0.715600f,-0.219093f), gr_complex(0.329554f,0.766044f), gr_complex(0.983632f,0.950521f), gr_complex(0.701660f,0.314967f), gr_complex(-0.116731f,-0.509440f), gr_complex(-0.802926f,-0.966175f), gr_complex(-0.995294f,-0.906845f), gr_complex(-0.729516f,-0.496337f), gr_complex(-0.238689f,0.017459f), gr_complex(0.253263f,0.457127f), gr_complex(0.623795f,0.752950f), gr_complex(0.847679f,0.913080f), gr_complex(0.955122f,0.979805f), gr_complex(0.992594f,0.998070f), gr_complex(0.999750f,0.999997f), gr_complex(0.999997f,0.999750f), gr_complex(0.998070f,0.992594f), gr_complex(0.979805f,0.955122f), gr_complex(0.913080f,0.847679f), gr_complex(0.752950f,0.623795f), gr_complex(0.457127f,0.253263f), gr_complex(0.017459f,-0.238689f), gr_complex(-0.496337f,-0.729516f), gr_complex(-0.906845f,-0.995294f), gr_complex(-0.966175f,-0.802926f), gr_complex(-0.509440f,-0.116731f), gr_complex(0.314967f,0.701660f), gr_complex(0.950521f,0.983632f), gr_complex(0.766044f,0.329554f), gr_complex(-0.219093f,-0.715600f), gr_complex(-0.984406f,-0.904951f), gr_complex(-0.475047f,0.160416f), gr_complex(0.742721f,0.999287f), gr_complex(0.778828f,0.156490f), gr_complex(-0.563327f,-0.980665f), gr_complex(-0.826269f,-0.156612f), gr_complex(0.627092f,0.999277f), gr_complex(0.669832f,-0.160048f), gr_complex(-0.879754f,-0.905162f), gr_complex(-0.176462f,0.715166f), gr_complex(0.975854f,0.330258f), gr_complex(-0.642169f,-0.983788f), gr_complex(-0.311545f,0.700951f), gr_complex(0.949435f,0.117841f), gr_complex(-0.859904f,-0.803666f), gr_complex(0.256628f,0.995161f), gr_complex(0.422759f,-0.728495f), gr_complex(-0.868900f,0.237120f), gr_complex(0.999817f,0.254946f), gr_complex(-0.888576f,-0.625251f), gr_complex(0.656626f,0.848732f), gr_complex(-0.405908f,-0.955745f), gr_complex(0.197824f,0.992863f), gr_complex(-0.059799f,-0.999800f), gr_complex(0.000062f,1.000000f), gr_complex(0.000000f,1.000000f), gr_complex(0.020006f,-0.998210f), gr_complex(-0.119260f,0.980238f), gr_complex(0.294195f,-0.913914f), gr_complex(-0.528823f,0.754216f), gr_complex(0.780424f,-0.458729f), gr_complex(-0.966955f,0.019136f), gr_complex(0.971480f,0.494987f), gr_complex(-0.685051f,-0.906242f), gr_complex(0.098261f,0.966510f), gr_complex(0.595080f,-0.510456f), gr_complex(-0.993032f,-0.313965f), gr_complex(0.713209f,0.950231f), gr_complex(0.179336f,-0.766563f), gr_complex(-0.943891f,-0.218426f), gr_complex(0.698954f,0.984307f), gr_complex(0.425066f,-0.475430f), gr_complex(-0.987109f,-0.742513f), gr_complex(0.038017f,0.778945f), gr_complex(0.987660f,0.563276f), gr_complex(-0.195692f,-0.826234f), gr_complex(-0.987680f,-0.627237f), gr_complex(0.037768f,0.669601f), gr_complex(0.987049f,0.879960f), gr_complex(0.425516f,-0.175912f), gr_complex(-0.698510f,-0.975704f), gr_complex(-0.944137f,-0.642788f), gr_complex(-0.180192f,0.310659f), gr_complex(0.712512f,0.949102f), gr_complex(0.993164f,0.860506f), gr_complex(0.596078f,0.257889f), gr_complex(-0.096900f,-0.421464f), gr_complex(-0.683964f,-0.868130f), gr_complex(-0.971096f,-0.999848f), gr_complex(-0.967397f,-0.889402f), gr_complex(-0.781588f,-0.658078f), gr_complex(-0.530509f,-0.407781f), gr_complex(-0.296214f,-0.199955f), gr_complex(-0.121481f,-0.062094f), gr_complex(-0.022366f,-0.002485f), gr_complex(-0.002485f,-0.022366f), gr_complex(-0.062094f,-0.121481f), gr_complex(-0.199955f,-0.296214f), gr_complex(-0.407781f,-0.530509f), gr_complex(-0.658078f,-0.781588f), gr_complex(-0.889402f,-0.967397f), gr_complex(-0.999848f,-0.971096f), gr_complex(-0.868130f,-0.683964f), gr_complex(-0.421464f,-0.096900f), gr_complex(0.257889f,0.596078f), gr_complex(0.860506f,0.993164f), gr_complex(0.949102f,0.712512f), gr_complex(0.310659f,-0.180192f), gr_complex(-0.642788f,-0.944137f), gr_complex(-0.975704f,-0.698510f), gr_complex(-0.175912f,0.425516f), gr_complex(0.879960f,0.987049f), gr_complex(0.669601f,0.037768f), gr_complex(-0.627237f,-0.987680f), gr_complex(-0.826234f,-0.195692f), gr_complex(0.563276f,0.987660f), gr_complex(0.778945f,0.038017f), gr_complex(-0.742513f,-0.987109f), gr_complex(-0.475430f,0.425066f), gr_complex(0.984307f,0.698954f), gr_complex(-0.218426f,-0.943891f), gr_complex(-0.766563f,0.179336f), gr_complex(0.950231f,0.713209f), gr_complex(-0.313965f,-0.993032f), gr_complex(-0.510456f,0.595080f), gr_complex(0.966510f,0.098261f), gr_complex(-0.906242f,-0.685051f), gr_complex(0.494987f,0.971480f), gr_complex(0.019136f,-0.966955f), gr_complex(-0.458729f,0.780424f), gr_complex(0.754216f,-0.528823f), gr_complex(-0.913914f,0.294195f), gr_complex(0.980238f,-0.119260f), gr_complex(-0.998210f,0.020006f), gr_complex(1.000000f,0.000000f)};
    
    
    
    const gr_complex* in = static_cast<const gr_complex*>(input_items[0]);
    float* out = static_cast<float*>(output_items[0]);

    if (ninput_items[0] < 160) {
        consume_each(0); // input sample not enough, return to next buffer?
        return 0;
    }

    int nInputLimit = ninput_items[0] - 160; // number of limited input samples can be used
    for (int i = 0; i < nInputLimit; i++) {
        out[i] = CrossCorr(&in[i], f_array_a);
    }

    consume_each(nInputLimit);
    return nInputLimit;
    }

  } /* namespace UConn2402 */
} /* namespace gr */
