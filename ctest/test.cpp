#include "gtest/gtest.h"

extern "C"
{
#include "out/mcparser.h"
}

TEST(op_parse, should_parse_32bit_instructions)
{
  // constants
  unsigned char machine_codes[] = {
      0x00, 0x48, 0x2D, 0xE9, /* push    {fp, lr} */
      0x04, 0xB0, 0x8D, 0xE2, /* add     fp, sp, #4 */
  };

  // actions
  OpDecodedCodeType decoded_code_push;
  OperationCodeType optype_push;
  int result_push;

  result_push = op_parse((uint16 *)&machine_codes[0], &decoded_code_push, &optype_push);

  OpDecodedCodeType decoded_code_add;
  OperationCodeType optype_add;
  int result_add;
  result_add = op_parse((uint16 *)&machine_codes[4], &decoded_code_add, &optype_add);

  // assertions
  // push
  EXPECT_EQ(optype_push.code_id, OpCodeId_push_1);
  EXPECT_EQ(optype_push.format_id, OP_CODE_FORMAT_push_1);
  EXPECT_EQ(decoded_code_push.type_id, OP_CODE_FORMAT_push_1);
  EXPECT_EQ(decoded_code_push.code.push_1.cond, 0x0E);            /* 31-28 bit */
  EXPECT_EQ(decoded_code_push.code.push_1.register_list, 0x4800); /* 15-0 bit */

  // add
  EXPECT_EQ(optype_add.code_id, OpCodeId_add_1);
  EXPECT_EQ(optype_add.format_id, OP_CODE_FORMAT_add_1);
  EXPECT_EQ(decoded_code_add.type_id, OP_CODE_FORMAT_add_1);
  EXPECT_EQ(decoded_code_add.code.add_1.cond, 0x0E);  /* 31-28 bit */
  EXPECT_EQ(decoded_code_add.code.add_1.S, 0x00);     /* 20 bit */
  EXPECT_EQ(decoded_code_add.code.add_1.Rn, 0x0D);    /* 19-16 bit */
  EXPECT_EQ(decoded_code_add.code.add_1.Rd, 0x0B);    /* 15-12 bit */
  EXPECT_EQ(decoded_code_add.code.add_1.imm12, 0x04); /* 11-0 bit */
}
