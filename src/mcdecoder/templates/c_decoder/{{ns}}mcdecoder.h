#ifndef _{{ ns }}MC_DECODER_H_
#define _{{ ns }}MC_DECODER_H_

#include <stdint.h>
#include <stdbool.h>


/*
 * Types
 */

/** Decoding request */
typedef struct {
	const uint8_t *codes;	/** Codes to be input */
} {{ ns }}DecodeRequest;

/** Instruction id to identify a decoded instruction */
typedef enum {
	{% for inst in instruction_decoders -%}
		{{ ns }}InstructionId_k_{{ inst.name }},	/** {{ inst.name }} */
	{% endfor %}
	{{ ns }}InstructionId_kUnknown, /** Unknown instruction */
} {{ ns }}InstructionId;

/** Number of instruction ids */
#define {{ ns }}INSTRUCTION_ID_MAX {{ ns }}InstructionId_kUnknown

{% for inst in instruction_decoders %}
	/** Decoding result for {{ inst.name }} */
	typedef struct {
		{% for field in inst.fields -%}
			uint{{ field.type_bit_length }}_t {{ field.name }};	/** Bit {% for sf in field.subfields %}{{ sf.msb_in_instruction }}-{{ sf.lsb_in_instruction }}{% if not loop.last %}, {% endif %}{% endfor %}: Decoding result for {{ field.name }} */
		{% endfor %}
	} {{ ns }}InstructionDecodeResult_{{ inst.name }};
{% endfor %}

/** Decoding result */
typedef struct {
	{{ ns }}InstructionId instruction_id;	/** Decoded instruction id */
    union {
		{% for inst in instruction_decoders -%}
        	{{ ns }}InstructionDecodeResult_{{ inst.name }} {{ inst.name }};	/** Decoding result for {{ inst.name }} */
		{% endfor %}
    } instruction;	/** Decoding result for an instruction */
} {{ ns }}DecodeResult;


/*
 * Functions
 */

/**
 * Decode an instruction
 *
 * @param request Decoding request
 * @param result Decoding result
 * @return True if decoding succeeded. False otherwise
 */
extern bool {{ ns }}DecodeInstruction(const {{ ns }}DecodeRequest *request, {{ ns }}DecodeResult *result);


#endif /* !_{{ ns }}MC_DECODER_H_ */
