/* -*- c++ -*- */
/*
 * Copyright 2024 UConn SD2402.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#include "Preamble_impl.h"
#include <gnuradio/io_signature.h>

#include <fstream>
#include <vector>

namespace gr {
namespace UConn2402 {

using input_type = gr_complex;
using output_type = gr_complex;
Preamble::sptr Preamble::make(const char* filename, const std::string& pcklen)
{
    return gnuradio::make_block_sptr<Preamble_impl>(filename, pcklen);
}


/*
 * The private constructor
 */
Preamble_impl::Preamble_impl(const char* filename, const std::string& pcklen)
    : gr::tagged_stream_block("Preamble",
                              gr::io_signature::make(1, 1, sizeof(input_type)),
                              gr::io_signature::make(1, 1, sizeof(output_type)),
                              pcklen)
{
    set_tag_propagation_policy(TPP_DONT);
    open(filename);
}

/*
 * Our virtual destructor.
 */
Preamble_impl::~Preamble_impl() {}

int Preamble_impl::calculate_output_stream_length(const gr_vector_int& ninput_items)
{
    return ninput_items[0] + d_preamble.size();
}

void Preamble_impl::open(const char* filename)
{

    // Clear the preamble array before populating it with new values
    d_preamble.clear();
    
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
    std::cerr << "Preamble length: " << d_preamble.size() << " samples" << std::endl;
}

int Preamble_impl::work(int noutput_items,
                        gr_vector_int& ninput_items,
                        gr_vector_const_void_star& input_items,
                        gr_vector_void_star& output_items)
{
    int n_produced = 0;
    const unsigned char* in = (const unsigned char*)input_items[0];
    unsigned char* out = (unsigned char*)output_items[0];


    // add preamble
    memcpy(out, d_preamble.data(), d_preamble.size() * sizeof(gr_complex));
    out += d_preamble.size() * sizeof(gr_complex);
    n_produced += d_preamble.size();

    // add current data
    memcpy(out, (const void*)in, ninput_items[0] * sizeof(gr_complex));
    out += ninput_items[0] * sizeof(gr_complex);
    n_produced += ninput_items[0];


    return n_produced;
}

} /* namespace UConn2402 */
} /* namespace gr */
