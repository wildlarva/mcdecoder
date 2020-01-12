#ifndef _MC_DECODER_H_
#define _MC_DECODER_H_

#include <stdint.h>

typedef uint8_t uint8;
typedef uint16_t uint16;
typedef uint32_t uint32;

#define OP_CODE_FORMAT_NUM OP_CODE_FORMAT_UNKNOWN

typedef enum
{

	OP_CODE_FORMAT_add_immediate_a1,

	OP_CODE_FORMAT_push_a1,

	OP_CODE_FORMAT_UNKNOWN,
} OpCodeFormatId;

typedef enum
{

	OpCodeId_add_immediate_a1,

	OpCodeId_push_a1,

	OpCodeId_Num,
} OpCodeId;

typedef struct
{
	OpCodeFormatId format_id;
	OpCodeId code_id;
} OperationCodeType;

typedef struct
{

	uint8 cond; /* 31-28 */

	uint8 S; /* 20-20 */

	uint8 Rn; /* 19-16 */

	uint8 Rd; /* 15-12 */

	uint16 imm12; /* 11-0 */

} OpCodeFormatType_add_immediate_a1;

typedef struct
{

	uint8 cond; /* 31-28 */

	uint16 register_list; /* 15-0 */

} OpCodeFormatType_push_a1;

typedef struct
{
	OpCodeFormatId type_id;
	union {

		OpCodeFormatType_add_immediate_a1 add_immediate_a1;

		OpCodeFormatType_push_a1 push_a1;

	} code;
} OpDecodedCodeType;

#define OP_DECODE_MAX (3)

extern int op_parse(uint16 code[OP_DECODE_MAX], OpDecodedCodeType *decoded_code, OperationCodeType *optype);

struct TargetCore;
typedef struct
{
	int clocks;
	int (*exec)(struct TargetCore *cpu);
} OpExecType;
extern OpExecType op_exec_table[OpCodeId_Num];

extern int op_exec_add_immediate_a1(struct TargetCore *core);
extern int op_exec_push_a1(struct TargetCore *core);
#endif /* !_MC_DECODER_H_ */