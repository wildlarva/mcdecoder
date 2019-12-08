#include "mcparser.h"

/* op constants */
{% for op in op_parsers %}
    /* {{ op.name }} */
    #define OP_FB_MASK_{{ op.name }} (0x{{ '%x'|format(op.fixed_bits_mask) }}l) /* fixed bits mask */
    #define OP_FB_{{ op.name }} (0x{{ '%x'|format(op.fixed_bits) }}l) /* fixed bits */
    {% for arg in op.arg_parsers %}
        #define OP_ARG_MASK_{{ op.name }}_{{ arg.name }} (0x{{ '%x'|format(arg.mask) }}l) /* arg mask: {{ arg.name }} */
        #define OP_ARG_END_BIT_{{ op.name }}_{{ arg.name }} ({{ arg.end_bit }}) /* arg end bit: {{ arg.name }} */
    {% endfor %}
{% endfor %}

/* individual op parse functions */
{% for op in op_parsers %}
    /* {{ op.name }} */
    static int op_parse_{{ op.name }}(uint16 code[OP_DECODE_MAX], OpDecodedCodeType *decoded_code, OperationCodeType *optype) {
        uint32 code32 = *(uint32 *) &code[0];
        if ((code32 & OP_FB_MASK_{{ op.name }}) != OP_FB_{{ op.name }}) {
            return 1;
        }

        optype->code_id = OpCodeId_{{ op.name }};
        optype->format_id = OP_CODE_FORMAT_{{ op.name }};
        decoded_code->type_id = OP_CODE_FORMAT_{{ op.name }};
        {% for arg in op.arg_parsers %}
            decoded_code->code.{{ op.name }}.{{ arg.name }} = (code32 & OP_ARG_MASK_{{ op.name }}_{{ arg.name }}) >> OP_ARG_END_BIT_{{ op.name }}_{{ arg.name }};
        {% endfor %}
        return 0;
    }
{% endfor %}

/* op parse function */
int op_parse(uint16 code[OP_DECODE_MAX], OpDecodedCodeType *decoded_code, OperationCodeType *optype) {
    {% for op in op_parsers %}
        if (op_parse_{{ op.name }}(code, decoded_code, optype) == 0) {
            return 0;
        }
    {% endfor %}

    return 1;
}
