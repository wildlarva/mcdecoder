#include "mcdhelper.hpp"

namespace mcdhelper
{

#pragma region Global variables

static std::map<std::string, Decoder> decoders;

#pragma endregion Global variables

#pragma region External functions

bool decode_instruction(const DecodeRequest &request, DecodeResult *result)
{
    std::map<std::string, Decoder>::iterator pair = decoders.find(request.decoder_name);
    if (pair == decoders.end())
    {
        return false;
    }

    return pair->second.decode_function(request, result);
}

void regist_decoder(const Decoder &decoder)
{
    decoders[decoder.decoder_name] = decoder;
}

#pragma endregion External functions

} // namespace mcdhelper
