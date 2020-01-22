#include "{{ ns }}mcdhelper.h"

#include "mcdhelper.h"

extern "C" {
    #include "{{ns}}mcdecoder.h"
}

namespace {{ mcdecoder.namespace }} {
namespace mcdhelper {

    
#pragma region Internal function declarations

static bool DecodeInstruction(const ::mcdhelper::DecodeRequest& request, ::mcdhelper::DecodeResult* result);
{% for inst in instruction_decoders %}
    static void ConvertResult_{{ inst.name }}(const {{ ns }}OpDecodedCodeType& decoded_code, ::mcdhelper::DecodeResult* result);
{% endfor %}
static bool DecodeInstruction(const ::mcdhelper::DecodeRequest& request, ::mcdhelper::DecodeResult* result);

#pragma endregion Internal function declarations

#pragma region External function definitions

void SetupDecoder(void) {   
    ::mcdhelper::Decoder decoder = {
        "{{ mcdecoder.namespace }}",
        DecodeInstruction,
    };

    ::mcdhelper::RegistDecoder(decoder);
}

#pragma endregion External function definitions

#pragma region Internal function definitions

static bool DecodeInstruction(const ::mcdhelper::DecodeRequest& request, ::mcdhelper::DecodeResult* result) {
    {{ ns }}uint16* code = ({{ ns }}uint16*) request.codes;
    {{ ns }}OpDecodedCodeType decoded_code;
    {{ ns }}OperationCodeType optype;

    int result_code = {{ ns }}op_parse(code, &decoded_code, &optype);

    switch (optype.code_id) {
    {% for inst in instruction_decoders %}
    case {{ ns }}OpCodeId_{{ inst.name }}:
        ConvertResult_{{ inst.name }}(decoded_code, result);
        break;
    {% endfor %}
    default:
        break;
    }

    return result_code == 0;
}

{% for inst in instruction_decoders %}
    static void ConvertResult_{{ inst.name }}(const {{ ns }}OpDecodedCodeType& decoded_code, ::mcdhelper::DecodeResult* result) {
        result->instruction_name = "{{ inst.name }}";
        {% for field in inst.field_decoders %}
            result->fields["{{ field.name }}"] = decoded_code.code.{{ inst.name }}.{{ field.name }};
        {% endfor %}
    }
{% endfor %}

#pragma endregion Internal function definitions

}
}
