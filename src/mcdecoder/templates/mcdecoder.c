#include "{{ ns }}mcparser.h"

typedef struct {
    {{ ns }}uint16 *code;
    {{ ns }}OpDecodedCodeType *decoded_code;
    {{ ns }}OperationCodeType *optype;
    {{ ns }}uint16 code16;
    {{ ns }}uint32 code32;
} OpDecodeContext;

/* op constants */
{% for op in op_parsers %}
    /* {{ op.name }} */
    #define OP_FB_MASK_{{ op.name }} (0x{{ '%08x'|format(op.fixed_bits_mask) }}l) /* fixed bits mask */
    #define OP_FB_{{ op.name }} (0x{{ '%08x'|format(op.fixed_bits) }}l) /* fixed bits */
    {% for arg in op.arg_parsers %}
        #define OP_ARG_MASK_{{ op.name }}_{{ arg.name }} (0x{{ '%08x'|format(arg.mask) }}l) /* arg mask: {{ arg.name }} */
        #define OP_ARG_END_BIT_{{ op.name }}_{{ arg.name }} ({{ arg.end_bit }}) /* arg end bit: {{ arg.name }} */
    {% endfor %}
{% endfor %}

/* individual op parse functions */
{% for op in op_parsers %}
    /* {{ op.name }} */
    static int op_parse_{{ op.name }}(OpDecodeContext *context) {
        if ((context->code{{ op.type_bit_size }} & OP_FB_MASK_{{ op.name }}) != OP_FB_{{ op.name }}) {
            return 1;
        }

        context->optype->code_id = {{ ns }}OpCodeId_{{ op.name }};
        context->optype->format_id = {{ ns }}OP_CODE_FORMAT_{{ op.name }};
        context->decoded_code->type_id = {{ ns }}OP_CODE_FORMAT_{{ op.name }};
        {% for arg in op.arg_parsers %}
            context->decoded_code->code.{{ op.name }}.{{ arg.name }} = (context->code{{ op.type_bit_size }} & OP_ARG_MASK_{{ op.name }}_{{ arg.name }}) >> OP_ARG_END_BIT_{{ op.name }}_{{ arg.name }};
        {% endfor %}
        return 0;
    }
{% endfor %}

/* op parse function */
int {{ ns }}op_parse({{ ns }}uint16 code[{{ ns }}OP_DECODE_MAX], {{ ns }}OpDecodedCodeType *decoded_code, {{ ns }}OperationCodeType *optype) {
    OpDecodeContext context;
    context.code = &code[0];
    context.decoded_code = decoded_code;
    context.optype = optype;
    context.code16 = ({{ ns }}uint16) code[0];
    context.code32 = *(({{ ns }}uint32 *) &code[0]);

    {% for op in op_parsers %}
        if (op_parse_{{ op.name }}(&context) == 0) {
            return 0;
        }
    {% endfor %}

    return 1;
}
