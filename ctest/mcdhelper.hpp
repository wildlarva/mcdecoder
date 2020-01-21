#include <string>
#include <map>
#include <cstdint>

namespace mcdhelper
{

#pragma region Data types

typedef struct
{
    std::string decoder_name; // Name of a decoder
    const uint8_t *codes; // Codes to be input
} DecodeRequest;

typedef struct
{
    std::string instruction_name; // Name of a matched instruction
    std::map<std::string, uint32_t> fields; // Decoded field values
} DecodeResult;

typedef bool (*DecodeFunction)(const DecodeRequest &request, DecodeResult *result);

typedef struct
{
    std::string decoder_name;  // Name of a decoder
    DecodeFunction decode_function; // Function to decode an instruction
} Decoder;

#pragma endregion Data types

#pragma region Functions

extern bool decode_instruction(const DecodeRequest &request, DecodeResult *result);
extern void regist_decoder(const Decoder &decoder);

#pragma endregion Functions

} // namespace mcdhelper
