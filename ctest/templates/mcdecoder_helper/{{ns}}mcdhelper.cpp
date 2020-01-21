#include "{{ ns }}mcdhelper.hpp"

#include "mcdhelper.hpp"

extern "C" {
    #include "{{ ns }}mcdecoder.h"
}

namespace {{ mcdecoder.namespace }} {
namespace mcdhelper {

#pragma region Internal functions

{% for inst in instruction_decoders -%}
    static void ConvertResult_{{ inst.name }}(const {{ ns }}DecodeResult& concrete_result, ::mcdhelper::DecodeResult* result) {
        result->instruction_name = "{{ inst.name }}";
        {% for field in inst.field_decoders -%}
            result->fields["{{ field.name }}"] = concrete_result.instruction.{{ inst.name }}.{{ field.name }};
        {% endfor %}
    }
{% endfor %}

static bool DecodeInstruction(const ::mcdhelper::DecodeRequest& request, ::mcdhelper::DecodeResult* result) {
    {{ ns }}DecodeRequest concrete_request;
    concrete_request.codes = request.codes;

    {{ ns }}DecodeResult concrete_result;
    bool succeeded = {{ ns }}DecodeInstruction(&concrete_request, &concrete_result);

    switch (concrete_result.instruction_id) {
    {% for inst in instruction_decoders -%}
    case {{ ns }}InstructionId_k_{{ inst.name }}:
        ConvertResult_{{ inst.name }}(concrete_result, result);
        break;
    {% endfor %}
    }

    return succeeded;
}

#pragma endregion Internal functions

#pragma region External functions

void SetupDecoder(void) {   
    ::mcdhelper::Decoder decoder = {
        "{{ mcdecoder.namespace }}",
        DecodeInstruction,
    };

    ::mcdhelper::RegistDecoder(decoder);
}

#pragma endregion External functions

}
}
