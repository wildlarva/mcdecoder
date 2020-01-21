#include "arm_mcdecoder.h"
#include "ab_mcdecoder.h"
#include "at_mcdecoder.h"
#include "atb_mcdecoder.h"
#include "riscv_mcdecoder.h"
#include "pc_mcdecoder.h"
#include "cc_mcdecoder.h"
#include "dt16x2_mcdecoder.h"
#include "dt32x1_mcdecoder.h"

int arm_op_exec_add_1(struct TargetCore *cpu) { return 0; }
int arm_op_exec_push_1(struct TargetCore *cpu) { return 0; }

int ab_op_exec_add_1(struct TargetCore *cpu) { return 0; }
int ab_op_exec_push_1(struct TargetCore *cpu) { return 0; }

int at_op_exec_add_1(struct TargetCore *cpu) { return 0; }
int at_op_exec_push_1(struct TargetCore *cpu) { return 0; }

int atb_op_exec_add_1(struct TargetCore *cpu) { return 0; }
int atb_op_exec_push_1(struct TargetCore *cpu) { return 0; }

int riscv_op_exec_c_addi_1(struct TargetCore *cpu) { return 0; }
int riscv_op_exec_c_sd_1(struct TargetCore *cpu) { return 0; }

int pc_op_exec_equality_condition(struct TargetCore *core) { return 0; }
int pc_op_exec_in_condition(struct TargetCore *core) { return 0; }
int pc_op_exec_in_range_condition(struct TargetCore *core) { return 0; }
int pc_op_exec_field_element_subject(struct TargetCore *core) { return 0; }
int pc_op_exec_field_object(struct TargetCore *core) { return 0; }
int pc_op_exec_function_subject(struct TargetCore *core) { return 0; }

int cc_op_exec_and_condition(struct TargetCore *core) { return 0; }
int cc_op_exec_or_condition(struct TargetCore *core) { return 0; }
int cc_op_exec_and_or_condition1(struct TargetCore *core) { return 0; }
int cc_op_exec_and_or_condition2(struct TargetCore *core) { return 0; }

int dt16x2_op_exec_instruction0000_0001(struct TargetCore *core) { return 0; }
int dt16x2_op_exec_instruction0000_0010(struct TargetCore *core) { return 0; }
int dt16x2_op_exec_instruction0000_1000(struct TargetCore *core) { return 0; }
int dt16x2_op_exec_instruction0001_0001(struct TargetCore *core) { return 0; }
int dt16x2_op_exec_instruction0001_0010(struct TargetCore *core) { return 0; }
int dt16x2_op_exec_instruction0001_1000(struct TargetCore *core) { return 0; }
int dt16x2_op_exec_instruction0100_0001(struct TargetCore *core) { return 0; }
int dt16x2_op_exec_instruction0100_0010(struct TargetCore *core) { return 0; }
int dt16x2_op_exec_instruction0100_1000(struct TargetCore *core) { return 0; }
int dt16x2_op_exec_instruction0101_0001(struct TargetCore *core) { return 0; }
int dt16x2_op_exec_instruction0101_0010(struct TargetCore *core) { return 0; }
int dt16x2_op_exec_instruction0101_ab(struct TargetCore *core) { return 0; }
int dt16x2_op_exec_instruction1000(struct TargetCore *core) { return 0; }

int dt32x1_op_exec_instruction0000_0001(struct TargetCore *core) { return 0; }
int dt32x1_op_exec_instruction0000_0010(struct TargetCore *core) { return 0; }
int dt32x1_op_exec_instruction0000_1000(struct TargetCore *core) { return 0; }
int dt32x1_op_exec_instruction0001_0001(struct TargetCore *core) { return 0; }
int dt32x1_op_exec_instruction0001_0010(struct TargetCore *core) { return 0; }
int dt32x1_op_exec_instruction0001_1000(struct TargetCore *core) { return 0; }
int dt32x1_op_exec_instruction0100_0001(struct TargetCore *core) { return 0; }
int dt32x1_op_exec_instruction0100_0010(struct TargetCore *core) { return 0; }
int dt32x1_op_exec_instruction0100_1000(struct TargetCore *core) { return 0; }
int dt32x1_op_exec_instruction0101_0001(struct TargetCore *core) { return 0; }
int dt32x1_op_exec_instruction0101_0010(struct TargetCore *core) { return 0; }
int dt32x1_op_exec_instruction0101_ab(struct TargetCore *core) { return 0; }
int dt32x1_op_exec_instruction1000(struct TargetCore *core) { return 0; }
