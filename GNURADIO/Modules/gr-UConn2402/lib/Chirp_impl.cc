/* -*- c++ -*- */
/*
 * Copyright 2024 UConn SD 2402.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#include <gnuradio/io_signature.h>
#include "Chirp_impl.h"

namespace gr {
  namespace UConn2402 {

    using input_type = gr_complex;
    using output_type = gr_complex;
    Chirp::sptr
   
    Chirp::make(int samp_rate, int B, float dur, bool chirp_op, const std::string& pcklen)
    {
      return gnuradio::make_block_sptr<Chirp_impl>(samp_rate, B, dur, chirp_op, pcklen);
    }


    /*
     * The private constructor
     */
    Chirp_impl::Chirp_impl(int samp_rate, int B, float dur, bool chirp_op, const std::string& pcklen)
      : gr::tagged_stream_block("Chirp",
              gr::io_signature::make(1, 1, sizeof(input_type)),
              gr::io_signature::make(1, 1, sizeof(output_type)), pcklen)
    {
    set_tag_propagation_policy(TPP_DONT);
    _samp_rate = samp_rate;
    _B = B;
    _dur = dur;
    numsamples = _samp_rate*_dur;
      
    Chirp = new gr_complex[numsamples];
    gr_complex t[numsamples];

    gr_complex f_limit = gr_complex(float(_B/2),0.0f);
      for (int i = 0; i < (numsamples); ++i) {
      t[i] = gr_complex((float(i) * float(_dur)/float(numsamples-1)),0.0f);
      }

      gr_complex m = f_limit/gr_complex(float(_dur),0.0f);
      gr_complex complex = gr_complex(0.0f,1.0f)*gr_complex(2.0f,0.0f)*gr_complex(float(M_PI),0.0f);
      //std::transform(chirp_op.begin(), chirp_op.end(), chirp_op.begin(), ::tolower);

      //Chirp Gen
    if (chirp_op == true) {
      for (int id=0; id<(numsamples); ++id)
       {
        Chirp[id] = exp(complex* ( (-f_limit*t[id]) + (m*t[id]*t[id]) ) );
      }
    } else if (chirp_op == false) {
      for (int id=0; id<(numsamples); ++id)
       {
        Chirp[id] = exp(complex* ( (f_limit*t[id]) - (m*t[id]*t[id]) ) );
      }
    } else {
      for (int id=0; id<(numsamples); ++id)
       {
        Chirp[id] = exp(complex* ( (-f_limit*t[id]) + (m*t[id]*t[id]) ) );
      }
      std::cerr << "Invalid chirp operation...defaulting to Up Chirp" << std::endl;
    }


    }

    /*
     * Our virtual destructor.
     */
    Chirp_impl::~Chirp_impl() {}

    int
    Chirp_impl::calculate_output_stream_length(const gr_vector_int &ninput_items)
    {
    int nout = ninput_items[0];
    return nout;
      }   

    int
    Chirp_impl::work (int noutput_items,
                       gr_vector_int &ninput_items,
                       gr_vector_const_void_star &input_items,
                       gr_vector_void_star &output_items)
    {
    unsigned char* out = (unsigned char*)output_items[0];
    int n_produced = 0;
    const unsigned char* in = (const unsigned char*)input_items[0];
    size_t itemsize = sizeof(gr_complex);

    //add preamble
    memcpy((void*)out, (const void*)Chirp, numsamples*itemsize);
    out += numsamples*itemsize;
    n_produced += numsamples*itemsize;

    //find,move and resize input tag 
    //std::vector<tag_t> tags;
    //get_tags_in_range(tags, 0, nitems_read(0), nitems_read(0) + ninput_items[0]);
   // add_item_tag(0, tags[0].offset, tags[0].key, tags[0].value);

    //add current data
    memcpy((void*)out, (const void*)in, ninput_items[0]*itemsize);
    out += ninput_items[0]*itemsize;
    n_produced += ninput_items[0]*itemsize;

    return n_produced;
  }

  } /* namespace UConn2402 */
} /* namespace gr */
