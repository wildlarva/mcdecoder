#include "sample_parser.h"

/* op constants */
/* add_1 */
#define OP_FB_MASK_ADD_1 (0x0fe00000l) /* fixed bits mask */
#define OP_FB_ADD_1 (0x02800000l) /* fixed bits */
#define OP_ARG_MASK_ADD_1_COND (0xf0000000l) /* arg mask: cond */
#define OP_ARG_MASK_ADD_1_S (0x00100000l) /* arg mask: S */
#define OP_ARG_MASK_ADD_1_RN (0x000f0000l) /* arg mask: Rn */
#define OP_ARG_MASK_ADD_1_RD (0x0000f000l) /* arg mask: Rd */
#define OP_ARG_MASK_ADD_1_IMM12 (0x00000fffl) /* arg mask: imm12 */

/* push_1 */
#define OP_FB_MASK_PUSH_1 (0xffffa000l) /* fixed bits mask */
#define OP_FB_PUSH_1 (0xe92d0000l) /* fixed bits */
#define OP_ARG_MASK_PUSH_1_M (0x00004000l) /* arg mask: M */
#define OP_ARG_MASK_PUSH_1_REGISTER_LIST (0x00001fffl) /* arg mask: register_list */

/* op parse functions */
static int op_parse_add_1(uint16 code[OP_DECODE_MAX], OpDecodedCodeType *decoded_code, OperationCodeType *optype) {
    uint32 code32 = *(uint32 *) &code[0];
    if ((code32 & OP_FB_MASK_ADD_1) != OP_FB_ADD_1) {
        return 1;
    }

    optype->code_id = OpCodeId_ADD_1;
    optype->format_id = OP_CODE_FORMAT_ADD_1;
    decoded_code->type_id = OP_CODE_FORMAT_ADD_1;
    decoded_code->code.add_1.cond = (code32 & OP_ARG_MASK_ADD_1_COND) >> 28;
    decoded_code->code.add_1.S = (code32 & OP_ARG_MASK_ADD_1_S) >> 20;
    decoded_code->code.add_1.Rn = (code32 & OP_ARG_MASK_ADD_1_RN) >> 16;
    decoded_code->code.add_1.Rd = (code32 & OP_ARG_MASK_ADD_1_RD) >> 12;
    decoded_code->code.add_1.imm12 = (code32 & OP_ARG_MASK_ADD_1_IMM12) >> 0;
    return 0;
}

static int op_parse_push_1(uint16 code[OP_DECODE_MAX], OpDecodedCodeType *decoded_code, OperationCodeType *optype) {
    uint32 code32 = *(uint32 *) &code[0];
    if ((code32 & OP_FB_MASK_PUSH_1) != OP_FB_PUSH_1) {
        return 1;
    }

    optype->code_id = OpCodeId_PUSH_1;
    optype->format_id = OP_CODE_FORMAT_PUSH_1;
    decoded_code->type_id = OP_CODE_FORMAT_PUSH_1;
    decoded_code->code.push_1.M = (code32 & OP_ARG_MASK_PUSH_1_M) >> 14;
    decoded_code->code.push_1.register_list = (code32 & OP_ARG_MASK_PUSH_1_REGISTER_LIST) >> 0;
    return 0;
}

int op_parse(uint16 code[OP_DECODE_MAX], OpDecodedCodeType *decoded_code, OperationCodeType *optype) {
    if (op_parse_add_1(code, decoded_code, optype) == 0) {
        return 0;
    }
    if (op_parse_push_1(code, decoded_code, optype) == 0) {
        return 0;
    }

    return 1;
}