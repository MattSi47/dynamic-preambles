/* -*- c++ -*- */
/*
 * Copyright 2024 UConn SD 2402.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_UCONN2402_CHIRP_IMPL_H
#define INCLUDED_UCONN2402_CHIRP_IMPL_H

#include <gnuradio/UConn2402/Chirp.h>

namespace gr {
namespace UConn2402 {

class Chirp_impl : public Chirp
{
private:
    int _samp_rate;
    int _B;
    float _dur;
    // const std::string& _chirp_op;
    int numsamples;

    gr_complex* Chirp;

protected:
    int calculate_output_stream_length(const gr_vector_int& ninput_items);

public:
    Chirp_impl(int samp_rate, int B, float dur, bool chirp_op, const std::string& pcklen);
    ~Chirp_impl();

    // Where all the action really happens
    int work(int noutput_items,
             gr_vector_int& ninput_items,
             gr_vector_const_void_star& input_items,
             gr_vector_void_star& output_items);
};

} // namespace UConn2402
} // namespace gr

#endif /* INCLUDED_UCONN2402_CHIRP_IMPL_H */
