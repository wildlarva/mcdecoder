#include "mcparser.h"

/* op constants */

    /* add_1 */
    #define OP_FB_MASK_add_1 (0xfe00000l) /* fixed bits mask */
    #define OP_FB_add_1 (0x2800000l) /* fixed bits */
    
        #define OP_ARG_MASK_add_1_cond (0xf0000000l) /* arg mask: cond */
        #define OP_ARG_END_BIT_add_1_cond (28) /* arg end bit: cond */
    
        #define OP_ARG_MASK_add_1_S (0x100000l) /* arg mask: S */
        #define OP_ARG_END_BIT_add_1_S (20) /* arg end bit: S */
    

    /* push_1 */
    #define OP_FB_MASK_push_1 (0xfe00000l) /* fixed bits mask */
    #define OP_FB_push_1 (0x2800000l) /* fixed bits */
    
        #define OP_ARG_MASK_push_1_cond (0xf0000000l) /* arg mask: cond */
        #define OP_ARG_END_BIT_push_1_cond (28) /* arg end bit: cond */
    
        #define OP_ARG_MASK_push_1_register_list (0xffffl) /* arg mask: register_list */
        #define OP_ARG_END_BIT_push_1_register_list (0) /* arg end bit: register_list */
    


/* individual op parse functions */

    /* add_1 */
    static int op_parse_add_1(uint16 code[OP_DECODE_MAX], OpDecodedCodeType *decoded_code, OperationCodeType *optype) {
        uint32 code32 = *(uint32 *) &code[0];
        if ((code32 & OP_FB_MASK_add_1) != OP_FB_add_1) {
            return 1;
        }

        optype->code_id = OpCodeId_add_1;
        optype->format_id = OP_CODE_FORMAT_add_1;
        decoded_code->type_id = OP_CODE_FORMAT_add_1;
        
            decoded_code->code.add_1.cond = (code32 & OP_ARG_MASK_add_1_cond) >> OP_ARG_END_BIT_add_1_cond;
        
            decoded_code->code.add_1.S = (code32 & OP_ARG_MASK_add_1_S) >> OP_ARG_END_BIT_add_1_S;
        
        return 0;
    }


    /* push_1 */
    static int op_parse_push_1(uint16 code[OP_DECODE_MAX], OpDecodedCodeType *decoded_code, OperationCodeType *optype) {
        uint32 code32 = *(uint32 *) &code[0];
        if ((code32 & OP_FB_MASK_push_1) != OP_FB_push_1) {
            return 1;
        }

        optype->code_id = OpCodeId_push_1;
        optype->format_id = OP_CODE_FORMAT_push_1;
        decoded_code->type_id = OP_CODE_FORMAT_push_1;
        
            decoded_code->code.push_1.cond = (code32 & OP_ARG_MASK_push_1_cond) >> OP_ARG_END_BIT_push_1_cond;
        
            decoded_code->code.push_1.register_list = (code32 & OP_ARG_MASK_push_1_register_list) >> OP_ARG_END_BIT_push_1_register_list;
        
        return 0;
    }


/* op parse function */
int op_parse(uint16 code[OP_DECODE_MAX], OpDecodedCodeType *decoded_code, OperationCodeType *optype) {
    
        if (op_parse_add_1(code, decoded_code, optype) == 0) {
            return 0;
        }
    
        if (op_parse_push_1(code, decoded_code, optype) == 0) {
            return 0;
        }
    

    return 1;
}