/* -*- c++ -*- */
/*
 * Copyright 2024 UConn SD2402.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_UCONN2402_PREAMBLE_IMPL_H
#define INCLUDED_UCONN2402_PREAMBLE_IMPL_H

#include <gnuradio/UConn2402/Preamble.h>

#include <vector>

namespace gr {
namespace UConn2402 {

class Preamble_impl : public Preamble
{
private:
    std::vector<gr_complex> d_preamble;

protected:
    int calculate_output_stream_length(const gr_vector_int& ninput_items);

public:
    Preamble_impl(const char* filename, const std::string& pcklen);
    ~Preamble_impl();
    void open(const char* filename);

    // Where all the action really happens
    int work(int noutput_items,
             gr_vector_int& ninput_items,
             gr_vector_const_void_star& input_items,
             gr_vector_void_star& output_items);
};

} // namespace UConn2402
} // namespace gr

#endif /* INCLUDED_UCONN2402_PREAMBLE_IMPL_H */
