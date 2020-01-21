#include "mcdhelper.hpp"

extern "C" {
    #include "{{ns}}mcdecoder.h"
}

namespace {{ mcdecoder.namespace }} {
namespace mcdhelper {

#pragma region Internal functions

{% for inst in instruction_decoders %}
    static void convert_result_{{ inst.name }}(const {{ ns }}OpDecodedCodeType& decoded_code, ::mcdhelper::DecodeResult* result) {
        result->instruction_name = "{{ inst.name }}";
        {% for field in inst.field_decoders %}
            result->fields["{{ field.name }}"] = decoded_code.code.{{ inst.name }}.{{ field.name }};
        {% endfor %}
    }
{% endfor %}

static bool decode_instruction(const ::mcdhelper::DecodeRequest& request, ::mcdhelper::DecodeResult* result) {
    {{ ns }}uint16* code = ({{ ns }}uint16*) request.codes;
    {{ ns }}OpDecodedCodeType decoded_code;
    {{ ns }}OperationCodeType optype;
    int result_code;

    result_code = {{ ns }}op_parse(code, &decoded_code, &optype);

    switch (optype.code_id) {
    {% for inst in instruction_decoders %}
    case {{ ns }}OpCodeId_{{ inst.name }}:
        convert_result_{{ inst.name }}(decoded_code, result);
        break;
    {% endfor %}
    }

    return result_code == 0;
}

#pragma endregion Internal functions

#pragma region External functions

void setup_decoder(void) {   
    ::mcdhelper::Decoder decoder = {
        "{{ mcdecoder.namespace }}",
        decode_instruction,
    };

    ::mcdhelper::regist_decoder(decoder);
}

#pragma endregion External functions

}
}
