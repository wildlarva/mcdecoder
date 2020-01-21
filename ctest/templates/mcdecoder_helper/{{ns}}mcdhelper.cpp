#include "{{ ns }}mcdhelper.hpp"

#include "mcdhelper.hpp"

extern "C" {
    #include "{{ ns }}mcdecoder.h"
}

namespace {{ mcdecoder.namespace }} {
namespace mcdhelper {

#pragma region Internal functions

{% for inst in instruction_decoders -%}
    static void convert_result_{{ inst.name }}(const {{ ns }}DecodeResult& concrete_result, ::mcdhelper::DecodeResult* result) {
        result->instruction_name = "{{ inst.name }}";
        {% for field in inst.field_decoders -%}
            result->fields["{{ field.name }}"] = concrete_result.instruction.{{ inst.name }}.{{ field.name }};
        {% endfor %}
    }
{% endfor %}

static bool decode_instruction(const ::mcdhelper::DecodeRequest& request, ::mcdhelper::DecodeResult* result) {
    {{ ns }}DecodeRequest concrete_request;
    {{ ns }}DecodeResult concrete_result;
    int result_code;

    concrete_request.codes = request.codes;

    result_code = {{ ns }}decode_instruction(&concrete_request, &concrete_result);

    switch (concrete_result.instruction_id) {
    {% for inst in instruction_decoders -%}
    case {{ ns }}InstructionId_k_{{ inst.name }}:
        convert_result_{{ inst.name }}(concrete_result, result);
        break;
    {% endfor %}
    }

    return result_code;
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
