#ifndef _{{ ns }}MC_PARSER_H_
#define _{{ ns }}MC_PARSER_H_

#include <stdint.h>

typedef uint8_t {{ ns }}uint8;
typedef uint16_t {{ ns }}uint16;
typedef uint32_t {{ ns }}uint32;

#define {{ ns }}OP_CODE_FORMAT_NUM	{{ ns }}OP_CODE_FORMAT_UNKNOWN

typedef enum {
	{% for op in op_parsers %}
		{{ ns }}OP_CODE_FORMAT_{{ op.name }},
	{% endfor %}
	{{ ns }}OP_CODE_FORMAT_UNKNOWN,
} {{ ns }}OpCodeFormatId;

typedef enum {
	{% for op in op_parsers %}
		{{ ns }}OpCodeId_{{ op.name }},
	{% endfor %}
	{{ ns }}OpCodeId_Num,
} {{ ns }}OpCodeId;

typedef struct {
	{{ ns }}OpCodeFormatId	format_id;
	{{ ns }}OpCodeId		code_id;
} {{ ns }}OperationCodeType;


{% for op in op_parsers %}
typedef struct {
	{% for arg in op.arg_parsers %}
		{{ ns }}uint{{ arg.type_bit_size }} {{ arg.name }};	/* {{ arg.start_bit }}-{{ arg.end_bit }} */
	{% endfor %}
} {{ ns }}OpCodeFormatType_{{ op.name }};
{% endfor %}

typedef struct {
	{{ ns }}OpCodeFormatId type_id;
    union {
		{% for op in op_parsers %}
        	{{ ns }}OpCodeFormatType_{{ op.name }} {{ op.name }};
		{% endfor %}
    } code;
} {{ ns }}OpDecodedCodeType;

#define {{ ns }}OP_DECODE_MAX	(3)

extern int {{ ns }}op_parse({{ ns }}uint16 code[{{ ns }}OP_DECODE_MAX], {{ ns }}OpDecodedCodeType *decoded_code, {{ ns }}OperationCodeType *optype);

#endif /* !_{{ ns }}MC_PARSER_H_ */
