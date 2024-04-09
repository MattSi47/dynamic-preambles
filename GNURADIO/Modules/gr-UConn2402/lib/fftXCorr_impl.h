/* -*- c++ -*- */
/*
 * Copyright 2024 UConn SD2402.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_UCONN2402_FFTXCORR_IMPL_H
#define INCLUDED_UCONN2402_FFTXCORR_IMPL_H

#include <gnuradio/UConn2402/fftXCorr.h>
#include <gnuradio/fft/fft.h>

namespace gr {
namespace UConn2402 {

class fftXCorr_impl : public fftXCorr
{
private:
    std::vector<gr_complex> d_preamble;
    int numsamples = 0;
    int K = 512; //FFT is stable at 512 on most computers...  DO NOT INCREASE
    gr_complex fft_preamble[512];

    // fft
    fft::fft_complex_fwd d_fft;
    fft::fft_complex_rev d_ifft;

public:
    fftXCorr_impl(const char* filename);
    ~fftXCorr_impl();

    // Where all the action really happens
    void forecast(int noutput_items, gr_vector_int& ninput_items_required);

    int general_work(int noutput_items,
                     gr_vector_int& ninput_items,
                     gr_vector_const_void_star& input_items,
                     gr_vector_void_star& output_items);
    void ifft(const gr_complex* sig, gr_complex* res);
    void fft(const gr_complex* sig, gr_complex* res);
};

} // namespace UConn2402
} // namespace gr

#endif /* INCLUDED_UCONN2402_FFTXCORR_IMPL_H */
