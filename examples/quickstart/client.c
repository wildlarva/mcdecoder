#include "out/mcdecoder.h"
#include <stdio.h>

int main(void)
{
  /* Machine codes to be decoded */
  unsigned char machine_codes[] = {
      0x04, 0xB0, 0x8D, 0xE2, /* add     fp, sp, #4 */
  };

  /* Arguments for the decode API */
  OpDecodedCodeType decoded_code;
  OperationCodeType optype;
  int result;

  /* Decode */
  result = op_parse((uint16 *)&machine_codes[0], &decoded_code, &optype);
  if (result != 0)
  {
    printf("Decode failed.\n");
  }
  else
  {
    printf("Decode succeeded.\n");
    switch (optype.code_id)
    {
    case OpCodeId_add_immediate_a1:
      printf("Instruction: add_immediate_a1\n");
      printf("Rn = %d, Rd = %d, imm12 = %d\n", decoded_code.code.add_immediate_a1.Rn, decoded_code.code.add_immediate_a1.Rd, decoded_code.code.add_immediate_a1.imm12);
      break;
    case OpCodeId_push_a1:
      /* nop */
      break;
    default:
      break;
    }
  }

  return 0;
}

/* Stubs for instruction execution callbacks */
int op_exec_add_immediate_a1(struct TargetCore *cpu)
{
  return 0;
}

int op_exec_push_a1(struct TargetCore *cpu)
{
  return 0;
}