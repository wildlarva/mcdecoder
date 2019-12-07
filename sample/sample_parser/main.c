#include <stdio.h>
#include "sample_parser.h"

unsigned char machine_codes[] = {
    0x00, 0x48, 0x2D, 0xE9, /* push    {fp, lr} */
    0x04, 0xB0, 0x8D, 0xE2, /* add     fp, sp, #4 */
};

static void print_op(const OperationCodeType *optype, const OpDecodedCodeType *decoded_code) {
    switch (optype->code_id)
    {
    case OpCodeId_ADD_1:
        printf("optype: %d, cond = 0x%x, S = %d, Rn = %d, Rd = %d, imm12 = %d\n", 
        optype->code_id, decoded_code->code.add_1.cond, decoded_code->code.add_1.S, decoded_code->code.add_1.Rn, decoded_code->code.add_1.Rd, decoded_code->code.add_1.imm12);
        break;
    case OpCodeId_PUSH_1:
        printf("optype: %d, M = %d, register_list = 0x%x\n", 
        optype->code_id, decoded_code->code.push_1.M, decoded_code->code.push_1.register_list);
        break;
    default:
        break;
    }
}

int main(void) {
    OpDecodedCodeType decoded_code;
    OperationCodeType optype;
    int result;
    
    result = op_parse((uint16 *) &machine_codes[0], &decoded_code, &optype);
    print_op(&optype, &decoded_code);

    result = op_parse((uint16 *) &machine_codes[4], &decoded_code, &optype);
    print_op(&optype, &decoded_code);

    return 0;
}
