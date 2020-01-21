#ifndef _{{ ns }}MC_DECODER_H_
#define _{{ ns }}MC_DECODER_H_

#include <stdint.h>
#include <stdbool.h>


/*
 * Types
 */

typedef struct {
	const uint8_t *codes;
} {{ ns }}DecodeRequest;

typedef enum {
	{% for inst in instruction_decoders -%}
		{{ ns }}InstructionId_k_{{ inst.name }},
	{% endfor %}
	{{ ns }}InstructionId_kUnknown,
} {{ ns }}InstructionId;

#define {{ ns }}INSTRUCTION_ID_MAX {{ ns }}InstructionId_kUnknown

{% for inst in instruction_decoders %}
typedef struct {
	{% for field in inst.field_decoders -%}
		uint{{ field.type_bit_size }}_t {{ field.name }};	/* {% for sf in field.subfield_decoders %}{{ sf.start_bit_in_instruction }}-{{ sf.end_bit_in_instruction }}{% if not loop.last %}, {% endif %}{% endfor %} */
	{% endfor %}
} {{ ns }}InstructionDecodeResult_{{ inst.name }};
{% endfor %}

typedef struct {
	{{ ns }}InstructionId instruction_id;
    union {
		{% for inst in instruction_decoders -%}
        	{{ ns }}InstructionDecodeResult_{{ inst.name }} {{ inst.name }};
		{% endfor %}
    } instruction;
} {{ ns }}DecodeResult;


/*
 * Functions
 */

extern bool {{ ns }}decode_instruction(const {{ ns }}DecodeRequest *request, {{ ns }}DecodeResult *result);


#endif /* !_{{ ns }}MC_DECODER_H_ */
