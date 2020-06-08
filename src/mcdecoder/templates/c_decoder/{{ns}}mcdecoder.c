{# Renders the object/subject of a condition #}
{%- macro instruction_condition_object(instruction, object) -%}
    {%- if object.type == 'field' -%}
        {%- if object.element_index is none -%}
            context->result->instruction.{{ instruction.name }}.{{ object.field }}
        {%- else -%}
            BitElement(context->result->instruction.{{ instruction.name }}.{{ object.field }}, {{ object.element_index }})
        {%- endif -%}
    {%- elif object.type == 'immediate' -%}
        {{ object.value }}
    {%- elif object.type == 'function' -%}
        {{ object.function }}({{ instruction_condition_object(instruction, object.argument) }})
    {%- endif -%}
{%- endmacro -%}

{# Renders a condition recursively #}
{%- macro instruction_condition(instruction, condition) -%}
    {%- if condition.type == 'and' -%}
        {% for child_condition in condition.conditions %}
            {%- if not loop.first %} && {% endif -%}
            ({{ instruction_condition(instruction, child_condition) }})
        {% endfor %}
    {%- elif condition.type == 'or' -%}
        {% for child_condition in condition.conditions %}
            {%- if not loop.first %} || {% endif -%}
            ({{ instruction_condition(instruction, child_condition) }})
        {% endfor %}
    {%- elif condition.type == 'equality' -%}
        {{ instruction_condition_object(instruction, condition.subject) }} {{ condition.operator }} {{ instruction_condition_object(instruction, condition.object) }}
    {%- elif condition.type == 'in' -%}
        {% for value in condition.values %}
            {%- if not loop.first %} || {% endif -%}
            {{ instruction_condition_object(instruction, condition.subject) }} == {{ value }}
        {% endfor %}
    {%- elif condition.type == 'in_range' -%}
        {{ instruction_condition_object(instruction, condition.subject) }} >= {{ condition.value_start }} && {{ instruction_condition_object(instruction, condition.subject) }} <= {{ condition.value_end }}
    {%- endif %}
{%- endmacro -%}

#include "{{ ns }}mcdecoder.h"


/*
 * Types
 */

typedef struct {
    const {{ ns }}DecodeRequest *request;
    {{ ns }}DecodeResult *result;
    uint16_t code16x1;
    uint32_t code16x2;
    uint32_t code32x1;
} DecodeContext;

typedef uint32_t (*SetBitCountFunction)(uint32_t value);


/*
 * Internal function declarations
 */

{% for tree in mcdecoder.decision_trees -%}
    {% for node in tree.root_node.all_nodes -%}
        static bool DecisionNode_code{{ tree.encoding_element_bit_length }}x{{ tree.length_of_encoding_elements }}_{{ node.index }}(DecodeContext *context, uint32_t code);
    {% endfor %}
{% endfor %}
{% for inst in instructions -%}
    static bool DecodeInstruction_{{ inst.name }}(DecodeContext *context);
{% endfor %}
static uint32_t SetBitCount(uint32_t value);
static uint8_t BitElement(uint32_t value, uint8_t element_index);


/*
 * Internal global variables
 */

static const SetBitCountFunction setbit_count = SetBitCount;


/*
 * External function definitions
 */

/* decode function */
bool {{ ns }}DecodeInstruction(const {{ ns }}DecodeRequest *request, {{ ns }}DecodeResult *result) {
    const uint8_t *raw_code = request->codes;
    {% if machine.byteorder == 'little' -%}
        uint16_t word1_16bit = *((uint16_t *) &raw_code[0]);
        uint16_t word2_16bit = *((uint16_t *) &raw_code[2]);
    {% else -%}
        uint16_t word1_16bit = (((uint16_t) raw_code[0]) << 8) | ((uint16_t) raw_code[1]);
        uint16_t word2_16bit = (((uint16_t) raw_code[2]) << 8) | ((uint16_t) raw_code[3]);
    {% endif %}

    DecodeContext context;
    context.request = request;
    context.result = result;
    context.code16x1 = word1_16bit;
    context.code16x2 = (((uint32_t) word1_16bit) << 16) | ((uint32_t) word2_16bit);
    {% if machine.byteorder == 'little' -%}
        context.code32x1 = *((uint32_t *) &raw_code[0]);
    {% else -%}
        context.code32x1 = context.code16x2;
    {% endif %}
    {% for tree in mcdecoder.decision_trees -%}
        if (DecisionNode_code{{ tree.encoding_element_bit_length }}x{{ tree.length_of_encoding_elements }}_{{ tree.root_node.index }}(&context, context.code{{ tree.encoding_element_bit_length }}x{{ tree.length_of_encoding_elements }})) {
            return true;
        }
    {% endfor %}
    return false;
}


/*
 * Internal function definitions
 */

/* decision node functions */
{% for tree in mcdecoder.decision_trees -%}
    {% for node in tree.root_node.all_nodes -%}
        static bool DecisionNode_code{{ tree.encoding_element_bit_length }}x{{ tree.length_of_encoding_elements }}_{{ node.index }}(DecodeContext *context, uint32_t code) {
            {% for inst in node.instructions -%}
                if (DecodeInstruction_{{ inst.name }}(context)) {
                    return true;
                }
            {% endfor %}
            {% if node.fixed_bit_nodes -%}
                switch (code & 0x{{ '%08x'|format(node.mask) }}) {
                    {% for threshold_value, child_node in node.fixed_bit_nodes.items() -%}
                        case 0x{{ '%08x'|format(threshold_value) }}:
                            if (DecisionNode_code{{ tree.encoding_element_bit_length }}x{{ tree.length_of_encoding_elements }}_{{ child_node.index }}(context, code)) {
                                return true;
                            }
                            break;
                    {% endfor %}
                default:
                    break;
                }
            {% endif %}
            {% if node.arbitrary_bit_node -%}
                if (DecisionNode_code{{ tree.encoding_element_bit_length }}x{{ tree.length_of_encoding_elements }}_{{ node.arbitrary_bit_node.index }}(context, code)) {
                    return true;
                }
            {% endif %}
            return false;
        }
    {% endfor %}
{% endfor %}

/* individual decode functions */
{% for inst in instructions %}
    static bool DecodeInstruction_{{ inst.name }}(DecodeContext *context) {
        if ((context->code{{ inst.encoding_element_bit_length }}x{{ inst.length_of_encoding_elements }} & (0x{{ '%08x'|format(inst.fixed_bit_mask) }}l)) != (0x{{ '%08x'|format(inst.fixed_bits) }}l)) {
            return false;
        }

        context->result->instruction_id = {{ ns }}InstructionId_k_{{ inst.name }};
        {% for field in inst.fields -%}
            context->result->instruction.{{ inst.name }}.{{ field.name }} =
            {% for sf in field.subfields -%}
                {% if not loop.first %}| {% endif %}(((context->code{{ inst.encoding_element_bit_length }}x{{ inst.length_of_encoding_elements }} & (0x{{ '%08x'|format(sf.mask) }}l)) >> ({{ sf.lsb_in_instruction }})) << ({{ sf.lsb_in_field }})){% if loop.last %};{% endif %}
            {% endfor %}
        {% endfor %}
        {% if inst.match_condition -%}
            if (!(
                {{ instruction_condition(inst, inst.match_condition) }}
            )) {
                return false;
            }
        {% endif %}
        {% if inst.unmatch_condition -%}
            if (
                {{ instruction_condition(inst, inst.unmatch_condition) }}
            ) {
                return false;
            }
        {% endif %}
        return true;
    }
{% endfor %}

/* functions for conditions */
static uint32_t SetBitCount(uint32_t value) {
    uint32_t count = 0;
    while (value) {
        count += value & 1;
        value >>= 1;
    }
    return count;
}

static uint8_t BitElement(uint32_t value, uint8_t element_index) {
    return (value & (1u << element_index)) >> element_index;
}
