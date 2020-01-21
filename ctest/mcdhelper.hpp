#include <string>
#include <map>
#include <cstdint>

namespace mcdhelper
{

#pragma region Types

/** Decoding request */
struct DecodeRequest
{
    std::string decoder_name; /** Name of a decoder */
    const uint8_t* codes;     /** Codes to be input */
};

/** Decoding result */
struct DecodeResult
{
    std::string instruction_name;           /** Name of a matched instruction */
    std::map<std::string, uint32_t> fields; /** Decoded field values */
};

/**
 * Decoding function
 * 
 * @param request Decoding request
 * @param result Decoding result
 * @return True if decoding succeeded. False otherwise
 */
typedef bool (*DecodeFunction)(const DecodeRequest& request, DecodeResult* result);

/** Decoder information */
struct Decoder
{
    std::string decoder_name;       /** Name of a decoder */
    DecodeFunction decode_function; /** Function to decode an instruction */
};

#pragma endregion Types

#pragma region Functions

/**
 * Decode an instruction
 * 
 * @param request Decoding request
 * @param result Decoding result
 * @return True if decoding succeeded. False otherwise
 */
extern bool DecodeInstruction(const DecodeRequest& request, DecodeResult* result);

/**
 * Register a decoder
 * 
 * @param decoder Decoder to be registered
 */
extern void RegistDecoder(const Decoder& decoder);

/** Hook to setup decoders */
extern void SetupDecoders();

#pragma endregion Functions

} // namespace mcdhelper
