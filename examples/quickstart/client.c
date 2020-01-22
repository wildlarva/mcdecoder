#include <stdio.h>
#include "out/mcdecoder.h"

int main(void) {
  /* Machine codes to be decoded */
  const uint8_t kMachineCodes[] = {
      0x04, 0xB0, 0x8D, 0xE2, /* add FP, SP, #4 */
  };

  /* Decode an instruction */
  DecodeRequest request;
  DecodeResult result;
  bool succeeded;

  request.codes = &kMachineCodes[0];
  succeeded = DecodeInstruction(&request, &result);

  /* Decoding succeeded? */
  if (!succeeded) {
    printf("Decoding failed.\n");

  } else {
    printf("Decoding succeeded.\n");

    /* Which instruction is decoded? */
    switch (result.instruction_id) {
      case InstructionId_k_add_immediate_a1:
        /* Get the decoded result of add_immediate_a1 */
        printf("Instruction: add_immediate_a1\n");
        printf("Rn: %d\nRd: %d\nimm12: %d\n", result.instruction.add_immediate_a1.Rn, result.instruction.add_immediate_a1.Rd,
               result.instruction.add_immediate_a1.imm12);
        break;
      case InstructionId_k_push_a1:
        /* Handle push_a1 */
        break;
      case InstructionId_kUnknown:
        /* Handle an unknown instruction */
        break;
      default:
        break;
    }
  }

  return 0;
}
