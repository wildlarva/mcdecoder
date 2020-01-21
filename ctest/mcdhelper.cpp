#include "mcdhelper.hpp"

namespace mcdhelper
{

#pragma region Internal global variables

static std::map<std::string, Decoder> decoders;

#pragma endregion Internal global variables

#pragma region External functions

bool DecodeInstruction(const DecodeRequest& request, DecodeResult* result)
{
    std::map<std::string, Decoder>::iterator pair = decoders.find(request.decoder_name);
    if (pair == decoders.end())
    {
        return false;
    }

    return pair->second.decode_function(request, result);
}

void RegistDecoder(const Decoder& decoder)
{
    decoders[decoder.decoder_name] = decoder;
}

#pragma endregion External functions

} // namespace mcdhelper
