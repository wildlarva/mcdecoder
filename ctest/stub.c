#include "out/arm_mcdecoder.h"
#include "out/riscv_mcdecoder.h"
#include "out/pc_mcdecoder.h"

int arm_op_exec_add_1(struct TargetCore *cpu) { return 0; }
int arm_op_exec_push_1(struct TargetCore *cpu) { return 0; }

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
