/* -*- c++ -*- */
/*
 * Copyright 2024 UConn SD2402.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#include "fftXCorr_impl.h"
#include <gnuradio/io_signature.h>

#include <fstream>
#include <vector>

namespace gr {
namespace UConn2402 {


fftXCorr::sptr fftXCorr::make(const char* filename)
{
    return gnuradio::make_block_sptr<fftXCorr_impl>(filename);
}


/*
 * The private constructor
 */
fftXCorr_impl::fftXCorr_impl(const char* filename)
    : gr::block("fftXCorr",
                gr::io_signature::make(1, 1, sizeof(gr_complex)),
                gr::io_signature::make(1, 1, sizeof(float))),
      d_fft(K, 1),
      d_ifft(K, 1)
{
    std::ifstream file(filename);
    if (!file.is_open()) {
        std::cerr << "Error opening file: " << filename << std::endl;
        return;
    }


    std::string line;
    if (!std::getline(file, line)) {
        std::cerr << "Error: Empty file or unable to read a line." << std::endl;
        return;
    }

    std::stringstream ss(line);
    std::string token;

    while (std::getline(ss, token, ',')) {
        double real, imag;
        if (std::sscanf(token.c_str(), "(%lf|%lf)", &real, &imag) == 2) {
            d_preamble.emplace_back(real, imag);
        } else {
            std::cerr << "Invalid File Format| Error parsing token: " << token
                      << std::endl;
        }
    }
    if (d_preamble.size() > 512) {
        std::cerr << "***File too large for fft size!" << std::endl;
    } else {
        numsamples = d_preamble.size();

        // conj
        for (auto& val : d_preamble) {
            val = std::conj(val);
        }
        // Reverse
        std::reverse(d_preamble.begin(), d_preamble.end());
        // Pad zeros
        while (d_preamble.size() < 512) {
            d_preamble.emplace_back(0.0, 0.0);
        }
        fft(&d_preamble[0], &fft_preamble[0]);
    }
}

/*
 * Our virtual destructor.
 */
fftXCorr_impl::~fftXCorr_impl() {}
void fftXCorr_impl::fft(const gr_complex* sig, gr_complex* res)
{
    memcpy(d_fft.get_inbuf(), sig, sizeof(gr_complex) * K);
    d_fft.execute();
    memcpy(res, d_fft.get_outbuf(), sizeof(gr_complex) * K);
}
void fftXCorr_impl::ifft(const gr_complex* sig, gr_complex* res)
{
    memcpy(d_ifft.get_inbuf(), sig, sizeof(gr_complex) * K);
    d_ifft.execute();
    memcpy(res, d_ifft.get_outbuf(), sizeof(gr_complex) * K);
}
void fftXCorr_impl::forecast(int noutput_items, gr_vector_int& ninput_items_required)
{
    ninput_items_required[0] = noutput_items + (numsamples - 1);
}

int fftXCorr_impl::general_work(int noutput_items,
                                gr_vector_int& ninput_items,
                                gr_vector_const_void_star& input_items,
                                gr_vector_void_star& output_items)
{
    const gr_complex* in = static_cast<const gr_complex*>(input_items[0]);
    float* XCorr = static_cast<float*>(output_items[0]);


    //  Do <+signal processing+>
    //  Tell runtime system how many input items we consumed on
    //  each input stream.
    if (ninput_items[0] < (numsamples - 1)) {
        consume_each(0); // input sample not enough, return to next buffer?
        return 0;
    }

    if (numsamples == 0) {
        consume_each(0);
        return 0;
    }


    int L = K - (numsamples - 1);
    int nb = int((ninput_items[0] - (numsamples - 1)) / L);
    gr_complex fft_in[K];
    for (int i = 0; i < nb; ++i) {
        fft(&in[i * L], fft_in);
        gr_complex fft_out[K];
        gr_complex outputbuff[K];

        for (int id = 0; id < K; ++id) {
            fft_out[id] = fft_preamble[id] * fft_in[id];
        }
        ifft(&fft_out[0], outputbuff);


        // Sum outputs of length L
        float pwr_oneblock[K] = { 0 };
        for (int p = 0; p < K; ++p) {
            pwr_oneblock[p] = abs(in[p + (i * L)] * in[p + (i * L)]);
        }


        // Sum first "numsamples" from block
        float pwrsum[L] = { 0 };
        for (int j = 0; j < numsamples; ++j) {
            pwrsum[0] += pwr_oneblock[j];
        }

        // Remaining L-1 samples and output
        XCorr[i * L] =
            (abs(outputbuff[numsamples - 1]) / (sqrt(pwrsum[0]) * sqrt(numsamples))) * 1 /
            K;
        for (int n = 1; n < L; ++n) {
            pwrsum[n] =
                pwrsum[n - 1] - pwr_oneblock[n - 1] + pwr_oneblock[numsamples + n - 1];
            XCorr[i * L + n] = (abs(outputbuff[(numsamples - 1) + n]) /
                                (sqrt(pwrsum[n]) * sqrt(numsamples))) *
                               1 / K;
        }
    }

    consume_each(nb * L);
    return nb * L;
}

} /* namespace UConn2402 */
} /* namespace gr */
