typedef unsigned char uint8;
typedef unsigned short uint16;
typedef unsigned long uint32;

#define OP_CODE_FORMAT_NUM	OP_CODE_FORMAT_UNKNOWN

typedef enum {
	{% for op in op_parsers %}
		OP_CODE_FORMAT_{{ op.name }},
	{% endfor %}
	OP_CODE_FORMAT_UNKNOWN,
} OpCodeFormatId;

typedef enum {
	{% for op in op_parsers %}
		OpCodeId_{{ op.name }},
	{% endfor %}
	OpCodeId_Num,
} OpCodeId;

typedef struct {
	OpCodeFormatId	format_id;
	OpCodeId		code_id;
} OperationCodeType;


{% for op in op_parsers %}
typedef struct {
	{% for arg in op.arg_parsers %}
	uint{{ arg.bit_size }} {{ arg.name }};	/* {{ arg.start_bit }}-{{ arg.end_bit }} */
	{% endfor %}
} OpCodeFormatType_{{ op.name }};
{% endfor %}

typedef struct {
	OpCodeFormatId type_id;
    union {
		{% for op in op_parsers %}
        	OpCodeFormatType_{{ op.name }} {{ op.name }};
		{% endfor %}
    } code;
} OpDecodedCodeType;

#define OP_DECODE_MAX	(3)

extern int op_parse(uint16 code[OP_DECODE_MAX], OpDecodedCodeType *decoded_code, OperationCodeType *optype);
