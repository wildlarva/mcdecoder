#include "gtest/gtest.h"

extern "C"
{
#include "out/arm_mcdecoder.h"
#include "out/riscv_mcdecoder.h"
#include "out/pc_mcdecoder.h"
}

TEST(op_parse, should_decode_32bit_instructions)
{
  // constants
  unsigned char machine_codes[] = {
      0x00, 0x48, 0x2D, 0xE9, /* push    {fp, lr} */
      0x04, 0xB0, 0x8D, 0xE2, /* add     fp, sp, #4 */
  };

  // actions
  arm_OpDecodedCodeType decoded_code_push;
  arm_OperationCodeType optype_push;
  int result_push;

  result_push = arm_op_parse((arm_uint16 *)&machine_codes[0], &decoded_code_push, &optype_push);

  arm_OpDecodedCodeType decoded_code_add;
  arm_OperationCodeType optype_add;
  int result_add;
  result_add = arm_op_parse((arm_uint16 *)&machine_codes[4], &decoded_code_add, &optype_add);

  // assertions
  // push
  EXPECT_EQ(result_push, 0);
  EXPECT_EQ(optype_push.code_id, arm_OpCodeId_push_1);
  EXPECT_EQ(optype_push.format_id, arm_OP_CODE_FORMAT_push_1);
  EXPECT_EQ(decoded_code_push.type_id, arm_OP_CODE_FORMAT_push_1);
  EXPECT_EQ(decoded_code_push.code.push_1.cond, 0x0E);            /* 31-28 bit */
  EXPECT_EQ(decoded_code_push.code.push_1.register_list, 0x4800); /* 15-0 bit */

  // add
  EXPECT_EQ(result_add, 0);
  EXPECT_EQ(optype_add.code_id, arm_OpCodeId_add_1);
  EXPECT_EQ(optype_add.format_id, arm_OP_CODE_FORMAT_add_1);
  EXPECT_EQ(decoded_code_add.type_id, arm_OP_CODE_FORMAT_add_1);
  EXPECT_EQ(decoded_code_add.code.add_1.cond, 0x0E);  /* 31-28 bit */
  EXPECT_EQ(decoded_code_add.code.add_1.S, 0x00);     /* 20 bit */
  EXPECT_EQ(decoded_code_add.code.add_1.Rn, 0x0D);    /* 19-16 bit */
  EXPECT_EQ(decoded_code_add.code.add_1.Rd, 0x0B);    /* 15-12 bit */
  EXPECT_EQ(decoded_code_add.code.add_1.imm12, 0x04); /* 11-0 bit */
}

TEST(op_decode, should_decode_16bit_instructions)
{
  // constants
  unsigned char machine_codes[] = {
      0x41, 0x11, /* addi    sp,sp,-16 */
      0x06, 0xE4, /* sd      ra,8(sp) */
      0x00, 0x00, /* dummy */
      0x00, 0x00, /* dummy */
  };

  // actions
  riscv_OpDecodedCodeType decoded_code_addi;
  riscv_OperationCodeType optype_addi;
  int result_addi;

  result_addi = riscv_op_parse((riscv_uint16 *)&machine_codes[0], &decoded_code_addi, &optype_addi);

  riscv_OpDecodedCodeType decoded_code_sd;
  riscv_OperationCodeType optype_sd;
  int result_sd;
  result_sd = riscv_op_parse((riscv_uint16 *)&machine_codes[2], &decoded_code_sd, &optype_sd);

  // assertions
  // addi
  EXPECT_EQ(result_addi, 0);
  EXPECT_EQ(optype_addi.code_id, riscv_OpCodeId_c_addi_1);
  EXPECT_EQ(optype_addi.format_id, riscv_OP_CODE_FORMAT_c_addi_1);
  EXPECT_EQ(decoded_code_addi.type_id, riscv_OP_CODE_FORMAT_c_addi_1);
  EXPECT_EQ(decoded_code_addi.code.c_addi_1.funct3, 0x00);           /* 15-13 bit */
  EXPECT_EQ(decoded_code_addi.code.c_addi_1.imm, (0x1 << 5) | 0x10); /* 12, 6-2 bit */
  EXPECT_EQ(decoded_code_addi.code.c_addi_1.dest, 0x02);             /* 11-7 bit */
  EXPECT_EQ(decoded_code_addi.code.c_addi_1.op, 0x01);               /* 1-0 bit */

  // sd
  EXPECT_EQ(result_sd, 0);
  EXPECT_EQ(optype_sd.code_id, riscv_OpCodeId_c_sd_1);
  EXPECT_EQ(optype_sd.format_id, riscv_OP_CODE_FORMAT_c_sd_1);
  EXPECT_EQ(decoded_code_sd.type_id, riscv_OP_CODE_FORMAT_c_sd_1);
  EXPECT_EQ(decoded_code_sd.code.c_sd_1.funct3, 0x07);                    /* 15-13 bit */
  EXPECT_EQ(decoded_code_sd.code.c_sd_1.offset, (0x1 << 3) | (0x0 << 6)); /* 12-10, 9-7 bit */
  EXPECT_EQ(decoded_code_sd.code.c_sd_1.src, 0x01);                       /* 6-2 bit */
  EXPECT_EQ(decoded_code_sd.code.c_sd_1.op, 0x02);                        /* 1-0 bit */
}

TEST(op_parse, should_not_decode_condition_unmatched_instructions)
{
  // constants
  unsigned char machine_codes[] = {
      0x00, 0x48, 0x2D, 0xF9, /* push    {fp, lr} */
      0x04, 0xB0, 0x8D, 0xF2, /* add     fp, sp, #4 */
  };

  // actions
  arm_OpDecodedCodeType decoded_code_push;
  arm_OperationCodeType optype_push;
  int result_push;

  result_push = arm_op_parse((arm_uint16 *)&machine_codes[0], &decoded_code_push, &optype_push);

  arm_OpDecodedCodeType decoded_code_add;
  arm_OperationCodeType optype_add;
  int result_add;
  result_add = arm_op_parse((arm_uint16 *)&machine_codes[4], &decoded_code_add, &optype_add);

  // assertions
  // push
  EXPECT_NE(result_push, 0);

  // add
  EXPECT_NE(result_add, 0);
}

TEST(op_parse, should_match_field_element_subject)
{
  // constants
  pc_uint8 machine_codes[] = {
      0x03, 0x00, 0x00, 0x10, /* instruction using a condition with a field element subject */
      0x03, 0x00, 0x00, 0x30, /* instruction using a condition with a field element subject */
  };

  // actions
  pc_OpDecodedCodeType decoded_code1, decoded_code2;
  pc_OperationCodeType optype1, optype2;
  int result1, result2;

  result1 = pc_op_parse((pc_uint16 *)&machine_codes[0], &decoded_code1, &optype1);
  result2 = pc_op_parse((pc_uint16 *)&machine_codes[4], &decoded_code2, &optype2);

  // assertions
  EXPECT_EQ(result1, 0);
  EXPECT_EQ(optype1.code_id, pc_OpCodeId_field_element_subject);

  EXPECT_EQ(result2, 0);
  EXPECT_EQ(optype2.code_id, pc_OpCodeId_field_element_subject);
}

TEST(op_parse, should_unmatch_field_element_subject)
{
  // constants
  pc_uint8 machine_codes[] = {
      0x03, 0x00, 0x00, 0x20, /* instruction using a condition with a field element subject */
  };

  // actions
  pc_OpDecodedCodeType decoded_code;
  pc_OperationCodeType optype;
  int result;

  result = pc_op_parse((pc_uint16 *)&machine_codes[0], &decoded_code, &optype);

  // assertions
  EXPECT_NE(result, 0);
}

TEST(op_parse, should_match_field_object)
{
  // constants
  pc_uint8 machine_codes[] = {
      0x04, 0x00, 0x00, 0x00, /* instruction using a condition with a field object */
      0x04, 0x00, 0x00, 0x11, /* instruction using a condition with a field object */
  };

  // actions
  pc_OpDecodedCodeType decoded_code1, decoded_code2;
  pc_OperationCodeType optype1, optype2;
  int result1, result2;

  result1 = pc_op_parse((pc_uint16 *)&machine_codes[0], &decoded_code1, &optype1);
  result2 = pc_op_parse((pc_uint16 *)&machine_codes[4], &decoded_code2, &optype2);

  // assertions
  EXPECT_EQ(result1, 0);
  EXPECT_EQ(optype1.code_id, pc_OpCodeId_field_object);

  EXPECT_EQ(result2, 0);
  EXPECT_EQ(optype2.code_id, pc_OpCodeId_field_object);
}

TEST(op_parse, should_unmatch_field_object)
{
  // constants
  pc_uint8 machine_codes[] = {
      0x04, 0x00, 0x00, 0x01, /* instruction using a condition with a field object */
      0x04, 0x00, 0x00, 0x10, /* instruction using a condition with a field object */
  };

  // actions
  pc_OpDecodedCodeType decoded_code1, decoded_code2;
  pc_OperationCodeType optype1, optype2;
  int result1, result2;

  result1 = pc_op_parse((pc_uint16 *)&machine_codes[0], &decoded_code1, &optype1);
  result2 = pc_op_parse((pc_uint16 *)&machine_codes[4], &decoded_code2, &optype2);

  // assertions
  EXPECT_NE(result1, 0);
  EXPECT_NE(result2, 0);
}

TEST(op_parse, should_match_function_subject)
{
  // constants
  pc_uint8 machine_codes[] = {
      0x05, 0x00, 0x00, 0x30, /* instruction using a condition with a function subject */
      0x05, 0x00, 0x00, 0xa0, /* instruction using a condition with a function subject */
  };

  // actions
  pc_OpDecodedCodeType decoded_code1, decoded_code2;
  pc_OperationCodeType optype1, optype2;
  int result1, result2;

  result1 = pc_op_parse((pc_uint16 *)&machine_codes[0], &decoded_code1, &optype1);
  result2 = pc_op_parse((pc_uint16 *)&machine_codes[4], &decoded_code2, &optype2);

  // assertions
  EXPECT_EQ(result1, 0);
  EXPECT_EQ(optype1.code_id, pc_OpCodeId_function_subject);

  EXPECT_EQ(result2, 0);
  EXPECT_EQ(optype2.code_id, pc_OpCodeId_function_subject);
}

TEST(op_parse, should_unmatch_function_subject)
{
  // constants
  pc_uint8 machine_codes[] = {
      0x05, 0x00, 0x00, 0x10, /* instruction using a condition with a function subject */
      0x05, 0x00, 0x00, 0xe0, /* instruction using a condition with a function subject */
  };

  // actions
  pc_OpDecodedCodeType decoded_code1, decoded_code2;
  pc_OperationCodeType optype1, optype2;
  int result1, result2;

  result1 = pc_op_parse((pc_uint16 *)&machine_codes[0], &decoded_code1, &optype1);
  result2 = pc_op_parse((pc_uint16 *)&machine_codes[4], &decoded_code2, &optype2);

  // assertions
  EXPECT_NE(result1, 0);
  EXPECT_NE(result2, 0);
}
