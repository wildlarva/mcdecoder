#include <gtest/gtest.h>
#include <cucumber-cpp/autodetect.hpp>
#include <string>
#include <cstdint>
#include <algorithm>
#include <boost/algorithm/string.hpp>

#include "mcdhelper.hpp"

#include "arm_mcdhelper.hpp"
#include "ab_mcdhelper.hpp"
#include "at_mcdhelper.hpp"
#include "atb_mcdhelper.hpp"
#include "riscv_mcdhelper.hpp"
#include "pc_mcdhelper.hpp"
#include "cc_mcdhelper.hpp"
#include "dt16x2_mcdhelper.hpp"
#include "dt32x1_mcdhelper.hpp"

using cucumber::ScenarioScope;

struct McdCtx
{
    std::string decoder_name;
    bool result_code;
    mcdhelper::DecodeResult result;
};

BEFORE_ALL()
{
    arm::mcdhelper::setup_decoder();
    ab::mcdhelper::setup_decoder();
    at::mcdhelper::setup_decoder();
    atb::mcdhelper::setup_decoder();
    riscv::mcdhelper::setup_decoder();
    pc::mcdhelper::setup_decoder();
    cc::mcdhelper::setup_decoder();
    dt16x2::mcdhelper::setup_decoder();
    dt32x1::mcdhelper::setup_decoder();
}

GIVEN("^decoding instructions with the decoder \"([^\"]+)\"$")
{
    REGEX_PARAM(std::string, decoder_name);
    ScenarioScope<McdCtx> context;

    context->decoder_name = decoder_name;
}

WHEN("^I decode \"([^\"]+)\"$")
{
    REGEX_PARAM(std::string, code_str);
    ScenarioScope<McdCtx> context;

    // Get the byte length of code
    // In hex string, 2 characters correspond to 1 byte
    const int byte_char_len = 2;
    int byte_length = std::min((int)(code_str.length() / byte_char_len), 4);

    // Convert hex string to integer array
    uint8_t codes[4];
    for (int i = 0; i < byte_length; i++)
    {
        codes[i] = std::stoul(code_str.substr(i * byte_char_len, byte_char_len), nullptr, 16);
    }

    // Decode
    mcdhelper::DecodeRequest request;
    request.decoder_name = context->decoder_name;
    request.codes = (const uint8_t *)&codes[0];

    context->result_code = mcdhelper::decode_instruction(request, &context->result);
}

THEN("^the decoding should be succeeded$")
{
    ScenarioScope<McdCtx> context;

    EXPECT_TRUE(context->result_code);
}

THEN("^the decoding should be failed$")
{
    ScenarioScope<McdCtx> context;

    EXPECT_FALSE(context->result_code);
}

THEN("^the instruction should be \"([^\"]+)\"$")
{
    REGEX_PARAM(std::string, expected_instruction);
    ScenarioScope<McdCtx> context;

    EXPECT_EQ(expected_instruction, context->result.instruction_name);
}

THEN("^the fields \"([^\"]+)\" should be \"([^\"]+)\"$")
{
    REGEX_PARAM(std::string, fields_str);
    REGEX_PARAM(std::string, expected_values_str);
    ScenarioScope<McdCtx> context;

    // Split fields and values
    std::vector<std::string> fields;
    boost::split(fields, fields_str, boost::is_any_of(","));

    std::vector<std::string> str_expected_values;
    boost::split(str_expected_values, expected_values_str, boost::is_any_of(","));

    // Check the consistency of fields and values
    ASSERT_TRUE(fields.size() == str_expected_values.size());

    // Test the fields
    for (int i = 0; i < fields.size(); i++)
    {
        const std::string &field = fields[i];
        const std::string &str_expected_value = str_expected_values[i];
        uint32_t expected_value = std::stoul(str_expected_value, nullptr, 16);

        EXPECT_EQ(expected_value, context->result.fields[field]);
    }
}
