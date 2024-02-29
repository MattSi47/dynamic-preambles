/* -*- c++ -*- */
/*
 * Copyright 2024 Uconn Senior Design Team 2402.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#include "LFMChirpXCorr_impl.h"
#include <gnuradio/io_signature.h>


namespace gr {
namespace UConn2402 {


LFMChirpXCorr::sptr LFMChirpXCorr::make(int samp_rate, int B, float dur)
{
    return gnuradio::make_block_sptr<LFMChirpXCorr_impl>(samp_rate, B, dur);
}


/*
 * The private constructor
 */
LFMChirpXCorr_impl::LFMChirpXCorr_impl(int samp_rate, int B, float dur)
    : gr::block("LFMChirpXCorr",
                gr::io_signature::makev(2, 2,  std::vector<int>{sizeof(gr_complex), sizeof(float)}),
                gr::io_signature::make(2, 2, sizeof(float))),
      d_fft(K, 1),
      d_ifft(K, 1)
{
    _samp_rate = samp_rate;
    _B = B;
    _dur = dur;
    numsamples = _samp_rate * _dur;

    gr_complex Up_array[K];
    gr_complex Down_array[K];
    gr_complex t[numsamples];

/*
    while (K <= numsamples) {
      K = K << 1; 
    }
    std::cout << K << std::endl;
*/
    fft_upchirp = new gr_complex[K];
    fft_downchirp = new gr_complex[K];

    // Time array
    gr_complex f_limit = gr_complex(float(_B / 2), 0.0f);
    for (int i = 0; i < (numsamples); ++i) {
        t[i] = gr_complex((float(i) * float(_dur) / float(numsamples)), 0.0f);
    }

    gr_complex m = f_limit / gr_complex(float(_dur), 0.0f);
    gr_complex complex =
        gr_complex(0.0f, 1.0f) * gr_complex(2.0f, 0.0f) * gr_complex(float(M_PI), 0.0f);

    // Chirp Gen
    for (int id = 0; id < (numsamples); ++id) {
        Up_array[id] =
            std::conj(exp((complex * ((-f_limit * t[id]) + (m * t[id] * t[id])))));
        Down_array[id] =
            std::conj(exp((complex * ((f_limit * t[id]) - (m * t[id] * t[id])))));
    }

    // Reverse Up_array
    for (int i = 0; i < numsamples / 2; ++i) {
        std::swap(Up_array[i], Up_array[numsamples - i]);
    }

    // Reverse Down_array
    for (int i = 0; i < numsamples / 2; ++i) {
        std::swap(Down_array[i], Down_array[numsamples - i]);
    }

    // Pad array with zeros
    std::fill(Up_array + numsamples, Up_array + K - 1, 0);
    std::fill(Down_array + numsamples, Down_array + K - 1, 0);

    // fft of chirps
    fft(Up_array, fft_upchirp);
    fft(Down_array, fft_downchirp);

    std::cout << "Chirp gen done" << std::endl;
}

/*
 * Our virtual destructor.
 */
LFMChirpXCorr_impl::~LFMChirpXCorr_impl() {}


void LFMChirpXCorr_impl::fft(const gr_complex* sig, gr_complex* res)
{
    memcpy(d_fft.get_inbuf(), sig, sizeof(gr_complex) * K);
    d_fft.execute();
    memcpy(res, d_fft.get_outbuf(), sizeof(gr_complex) * K);
}
void LFMChirpXCorr_impl::ifft(const gr_complex* sig, gr_complex* res)
{
    memcpy(d_ifft.get_inbuf(), sig, sizeof(gr_complex) * K);
    d_ifft.execute();
    memcpy(res, d_ifft.get_outbuf(), sizeof(gr_complex) * K);
}

void LFMChirpXCorr_impl::forecast(int noutput_items, gr_vector_int& ninput_items_required)
{
    ninput_items_required[0] = noutput_items + (numsamples - 1);
}

int LFMChirpXCorr_impl::general_work(int noutput_items,
                                     gr_vector_int& ninput_items,
                                     gr_vector_const_void_star& input_items,
                                     gr_vector_void_star& output_items)
{
    const gr_complex* in = static_cast<const gr_complex*>(input_items[0]);
    const float* pwr = static_cast<const float*>(input_items[1]);
    float* XUp = static_cast<float*>(output_items[0]);
    float* XDown = static_cast<float*>(output_items[1]);

    //  Do <+signal processing+>
    //  Tell runtime system how many input items we consumed on
    //  each input stream.
    if (ninput_items[0] < (numsamples - 1)) {
        consume_each(0); // input sample not enough, return to next buffer?
        return 0;
    }


    int L = K - (numsamples-1);
    int nb = int((ninput_items[0] - (numsamples - 1)) / L);
    gr_complex fft_in[K];
    for (int i = 0; i < nb; ++i) {
        fft(&in[i * L], fft_in);
        gr_complex fft_up_out[K];
        gr_complex fft_down_out[K];
        gr_complex Up_outputbuff[K];
        gr_complex Down_outputbuff[K];
        float absUp_outputbuff[K];
        float absDown_outputbuff[K];
        for (int id = 0; id < K; ++id) {
            fft_up_out[id] = fft_upchirp[id] * fft_in[id];
            fft_down_out[id] = fft_downchirp[id] * fft_in[id];
            
            //*(1 / 160.0f) * gr_complex(1 / float(K), 0.0f)
        }
        ifft(&fft_up_out[0], Up_outputbuff);
        ifft(&fft_down_out[0], Down_outputbuff);
        //sumpwr = 1/(sumpwr) * 1/float(numsamples);
        for (int idx = 0; idx < K; ++idx){
            absUp_outputbuff[idx] = real(Up_outputbuff[idx]);
            absDown_outputbuff[idx] = real(Down_outputbuff[idx]);
        }

    
        //Sum outputs of length L 
        float pwr_oneblock[K]={0};
        memcpy(&pwr_oneblock, &pwr[i*L], sizeof(float) * K);

        //Sum first "numsamples" from block
        float pwrsum[L]={0};
        for (int j=0; j<numsamples; ++j){
            pwrsum[0] += pwr_oneblock[j];
        }

        //Remaining L-1 samples and output 
        XDown[i*L] = absDown_outputbuff[numsamples-1]/pwrsum[0];
        XUp[i*L] = absUp_outputbuff[numsamples-1]/pwrsum[0];
        for (int n=1; n<L; ++n){
            pwrsum[n]=pwrsum[n-1]-pwr_oneblock[n-1]+pwr_oneblock[numsamples+n-1];
            XDown[i*L+n] = absDown_outputbuff[numsamples-(n-1)]/pwrsum[n];
            XUp[i*L+n] = absUp_outputbuff[numsamples-(n-1)]/pwrsum[n]; 
        }




        //memcpy(&XUp[i * L], &absUp_outputbuff[numsamples - 1], sizeof(float) * L);
        //memcpy(&XDown[i * L], &absDown_outputbuff[numsamples - 1], sizeof(float) * L);

        // memcpy(&XUp[i * L], &Up_outputbuff[numsamples - 1], sizeof(gr_complex) * L);
       // memcpy(&XDown[i * L], &Down_outputbuff[numsamples - 1], sizeof(gr_complex) * L);
    }

    consume_each(nb * L);
    return nb * L;
}

} /* namespace UConn2402 */
} /* namespace gr */
