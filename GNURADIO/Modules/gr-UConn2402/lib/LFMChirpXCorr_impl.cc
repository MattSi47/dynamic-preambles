/* -*- c++ -*- */
/*
 * Copyright 2024 Uconn Senior Design Team 2402.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#include <gnuradio/io_signature.h>
#include "LFMChirpXCorr_impl.h"
#include <gnuradio/fft/fft_v.h>


namespace gr {
  namespace UConn2402 {

    using input_type = gr_complex;
    using output_type = float;
    LFMChirpXCorr::sptr
    LFMChirpXCorr::make(int samp_rate, int B, float dur)
    {
      return gnuradio::make_block_sptr<LFMChirpXCorr_impl>(samp_rate, B, dur
        );
    }


    /*
     * The private constructor
     */
    LFMChirpXCorr_impl::LFMChirpXCorr_impl(int samp_rate, int B, float dur)
      : gr::block("LFMChirpXCorr",
              gr::io_signature::make(1, 1, sizeof(input_type)),
              gr::io_signature::make(2, 2, sizeof(output_type)))
    {
      _samp_rate = samp_rate;
      _B = B;
      _dur = dur;
      numsamples = _samp_rate*_dur;
      
    Up_array = new gr_complex[numsamples];
    Down_array = new gr_complex[numsamples];
    gr_complex t[numsamples];

    gr_complex f_limit = gr_complex(float(_B/2),0.0f);
      for (int i = 0; i < (numsamples); ++i) {
      t[i] = gr_complex((float(i) * float(_dur)/float(numsamples-1)),0.0f);
      //std::cout << t[i] << std::endl;
      }

      gr_complex m = f_limit/gr_complex(float(_dur),0.0f);
      gr_complex complex = gr_complex(0.0f,1.0f)*gr_complex(2.0f,0.0f)*gr_complex(float(M_PI),0.0f);

      //Chirp Gen
      for (int id=0; id<(numsamples); ++id)
       {
        Up_array[id] = exp(complex* ( (-f_limit*t[id]) + (m*t[id]*t[id]) ) );
        //std::cout << "complex" << Up_array[id] << ", " ;
        Down_array[id] = exp(complex* ( (f_limit*t[id]) - (m*t[id]*t[id]) ) );
      }
     // std::cout <<std::endl;

      /*
      std::cout << "down array" << std::endl;
      for (int id=0; id<(numsamples); ++id)
       {
        std::cout << "complex" << Down_array[id] << ", " ;
       }
       std::cout <<std::endl;
       */
      


    
      std::cout << "Chirp gen done" << std::endl;
    float sum_up;
     float sum_down; 
    for (int id2=0; id2<(numsamples); id2++) {
      sum_up += abs(Up_array[id2]) * abs(Up_array[id2]);
      sum_down += abs(Down_array[id2]) * abs(Down_array[id2]);
    }
 in_sum_up= 1/sum_up;
 in_sum_down= 1/sum_down;

    //sum_up = gr_complex(1.0f,0.0f)/(sum_up);
    //sum_down = gr_complex(1.0f,0.0f)/(sum_down);


    }

    /*
     * Our virtual destructor.
     */
    LFMChirpXCorr_impl::~LFMChirpXCorr_impl() {}

/*
float LFMChirpXCorr_impl::XCorr(const gr_complex* input, gr_complex* pattern)
{

    gr_complex sum = 0, sum_abs_1 = 0, sum_abs_2 = 0;

    for (int id2=0; id2<(numsamples); id2++) {
        sum += (input[id2] * pattern[id2]);
        sum_abs_1 += abs(input[id2]) * abs(input[id2]);
        sum_abs_2 += abs(pattern[id2]) * abs(pattern[id2]);
    }
    return real((abs(sum) / sqrt(sum_abs_1) / sqrt(sum_abs_2)));
}
*/
    void LFMChirpXCorr_impl::forecast (int noutput_items, gr_vector_int &ninput_items_required)
    {
        ninput_items_required[0] = noutput_items + (numsamples);
    }

    int LFMChirpXCorr_impl::general_work (int noutput_items,
                       gr_vector_int &ninput_items,
                       gr_vector_const_void_star &input_items,
                       gr_vector_void_star &output_items)
    {
      const gr_complex* in = static_cast<const gr_complex*>(input_items[0]);
      float* XUp = static_cast<float*>(output_items[0]);
      float* XDown = static_cast<float*>(output_items[1]);

      //#pragma message("Implement the signal processing in your block and remove this warning")
      // Do <+signal processing+>
      // Tell runtime system how many input items we consumed on
      // each input stream.
      if (ninput_items[0] < (numsamples)) {
        consume_each(0); // input sample not enough, return to next buffer?
        return 0;
    }




    gr_complex* up = Up_array;
    gr_complex* down = Down_array;

    int nInputLimit = ninput_items[0] - (numsamples); // number of limited input samples can be used
    float sq_input[ninput_items[0]];
    for (int index=0; index<(ninput_items[0]); index++) {
    sq_input[index] = abs(in[index]) * abs(in[index]);
    }

    for (int idx=0; idx < nInputLimit; idx++) {
  
      /*
      XUp[idx] = XCorr(&in[idx], Up_array);
      XDown[idx] = XCorr(&in[idx], Down_array);
      */

  //CorrFunction
  const gr_complex* input = &in[idx];
  const float* _sq_input = &sq_input[idx];


    gr_complex sum_Xup = 0, sum_Xdown = 0;
    float sum_input = 0;
    for (int index=0; index<(numsamples); index++) {
      sum_input += _sq_input[index];
      sum_Xup += (input[index] * up[index]);
      sum_Xdown += (input[index] * down[index]);
    }
  //CorrFunction
    XUp[idx]= abs(sum_Xup)*abs(sum_Xup) / sum_input * in_sum_up;
    XDown[idx]= abs(sum_Xdown)*abs(sum_Xdown) / sum_input * in_sum_down;
    //XUp[idx]= real(abs(sum_Xup) / sqrt(sum_input) * sum_up);
   // XDown[idx]= real(abs(sum_Xdown) / sqrt(sum_input) * sum_down);
  
    } 


    consume_each(nInputLimit);
    return nInputLimit;
    }

  } /* namespace UConn2402 */
} /* namespace gr */
