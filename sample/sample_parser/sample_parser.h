typedef unsigned char uint8;
typedef unsigned short uint16;
typedef unsigned long uint32;

#define OP_CODE_FORMAT_NUM	OP_CODE_FORMAT_UNKNOWN

typedef enum {
	OP_CODE_FORMAT_ADD_1 = 0,
	OP_CODE_FORMAT_PUSH_1,
	OP_CODE_FORMAT_UNKNOWN,
} OpCodeFormatId;

typedef enum {
	OpCodeId_ADD_1 = 0,
    OpCodeId_PUSH_1,
	OpCodeId_Num,
} OpCodeId;

typedef struct {
	OpCodeFormatId	format_id;
	OpCodeId		code_id;
} OperationCodeType;

typedef struct {
	uint8 cond;	/* 31-28 */
	uint8 S;	/* 20 */
    uint8 Rn;   /* 19-16 */
    uint8 Rd;   /* 15-12 */
	uint16 imm12;	/* 11-0 */
} OpCodeFormatType_add_1;

typedef struct {
	uint8 M;	/* 14 */
	uint16 register_list;	/* 12-0 */
} OpCodeFormatType_push_1;

typedef struct {
	OpCodeFormatId type_id;
    union {
        OpCodeFormatType_add_1 add_1;
        OpCodeFormatType_push_1 push_1;
    } code;
} OpDecodedCodeType;

#define OP_DECODE_MAX	(3)

extern int op_parse(uint16 code[OP_DECODE_MAX], OpDecodedCodeType *decoded_code, OperationCodeType *optype);
