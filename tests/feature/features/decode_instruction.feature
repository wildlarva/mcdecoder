Feature: Decode an instruction

  Scenario Outline: Decode an instruction successfully
    Given decoding instructions with the decoder "<decoder>"
    When I decode "<code>"
    Then the decoding should be succeeded
     And the instruction should be "<instruction>"
     And the fields "<fields>" should be "<values>"

  Examples:
    # code: Raw bytes in hex string
    # values: Numbers in hex string. They're split by comma symbol.
    | decoder | code      | instruction   | fields                | values      | description                       |
    | arm     | 00482de9  | push_1        | cond,register_list    | e,4800      | 32-bit little endian              |
    | arm     | 04b08de2  | add_1         | cond,S,Rn,Rd,imm12    | e,0,d,b,4   | 32-bit little endian              |
    | ab      | e92d4800  | push_1        | cond,register_list    | e,4800      | 32-bit big endian                 |
    | ab      | e28db004  | add_1         | cond,S,Rn,Rd,imm12    | e,0,d,b,4   | 32-bit big endian                 |
    | riscv   | 4111      | c_addi_1      | funct3,imm,dest,op    | 0,30,2,1    | 16-bit little endian              |
    | riscv   | 06e4      | c_sd_1        | funct3,offset,src,op  | 7,8,1,2     | 16-bit little endian              |
    | at      | 2de90140  | push_1        | M,register_list       | 1,1         | 2 words of 16-bit, little endian  |
    | at      | 11f50111  | add_1         | i,S,Rn,imm3,Rd,imm8   | 1,1,1,1,1,1 | 2 words of 16-bit, little endian  |
    | atb     | e92d4001  | push_1        | M,register_list       | 1,1         | 2 words of 16-bit, big endian     |
    | atb     | f5111101  | add_1         | i,S,Rn,imm3,Rd,imm8   | 1,1,1,1,1,1 | 2 words of 16-bit, big endian     |

  Scenario Outline: Code matches an instruction
    Given decoding instructions with the decoder "<decoder>"
    When I decode "<code>"
    Then the decoding should be succeeded
     And the instruction should be "<instruction>"

  Examples:
    # code: Raw bytes in hex string
    | decoder | code     | instruction            | description                                       |
    | dt16x2  | 0000f100 | instruction0000_0001   | Decision tree for 2 words of 16-bit               |
    | dt16x2  | 0000f200 | instruction0000_0010   | Decision tree for 2 words of 16-bit               |
    | dt16x2  | 0000f800 | instruction0000_1000   | Decision tree for 2 words of 16-bit               |
    | dt16x2  | 001f1000 | instruction0001_0001   | Decision tree for 2 words of 16-bit               |
    | dt16x2  | f05000ff | instruction0101_ab     | Decision tree for 2 words of 16-bit               |
    | dt16x2  | f08fffff | instruction1000        | Decision tree for 2 words of 16-bit               |
    | dt32x1  | f1000000 | instruction0000_0001   | Decision tree for 1 word of 32-bit                |
    | dt32x1  | f2000000 | instruction0000_0010   | Decision tree for 1 word of 32-bit                |
    | dt32x1  | f8000000 | instruction0000_1000   | Decision tree for 1 word of 32-bit                |
    | dt32x1  | 1000001f | instruction0001_0001   | Decision tree for 1 word of 32-bit                |
    | dt32x1  | 00fff050 | instruction0101_ab     | Decision tree for 1 word of 32-bit                |
    | dt32x1  | fffff08f | instruction1000        | Decision tree for 1 word of 32-bit                |
    | pc      | 00000010 | equality_condition     | Equality condition                                |
    | pc      | 01000010 | in_condition           | In-a-set condition                                |
    | pc      | 01000030 | in_condition           | In-a-set condition                                |
    | pc      | 02000000 | in_range_condition     | In-a-range condition                              |
    | pc      | 020000b0 | in_range_condition     | In-a-range condition                              |
    | pc      | 03000010 | field_element_subject  | Field-element subject                             |
    | pc      | 03000030 | field_element_subject  | Field-element subject                             |
    | pc      | 04000000 | field_object           | Field object                                      |
    | pc      | 04000011 | field_object           | Field object                                      |
    | pc      | 05000030 | function_subject       | Function subject                                  |
    | pc      | 050000a0 | function_subject       | Function subject                                  |
    | cc      | 00000012 | and_condition          | Logical 'and' condition                           |
    | cc      | 01000021 | or_condition           | Logical 'or' condition                            |
    | cc      | 02000012 | and_or_condition1      | Combination of logical 'and' and 'or' conditions  |
    | cc      | 02000030 | and_or_condition1      | Combination of logical 'and' and 'or' conditions  |
    | cc      | 03000011 | and_or_condition2      | Combination of logical 'and' and 'or' conditions  |
    | cc      | 03000022 | and_or_condition2      | Combination of logical 'and' and 'or' conditions  |

  Scenario Outline: Code does not match any instructions
    Given decoding instructions with the decoder "<decoder>"
    When I decode "<code>"
    Then the decoding should be failed

  Examples:
    # code: Raw bytes in hex string
    | decoder | code      | description                                       |
    | arm     | 00482df9  | Like push but not matched                         |
    | arm     | 04b08df2  | Like add but not matched                          |
    | pc      | 00000000  | Equality condition                                |
    | pc      | 00000020  | Equality condition                                |
    | pc      | 01000000  | In-a-set condition                                |
    | pc      | 01000020  | In-a-set condition                                |
    | pc      | 02000010  | In-a-range condition                              |
    | pc      | 020000a0  | In-a-range condition                              |
    | pc      | 03000020  | Field-element subject                             |
    | pc      | 04000001  | Field object                                      |
    | pc      | 04000010  | Field object                                      |
    | pc      | 05000010  | Function subject                                  |
    | pc      | 050000e0  | Function subject                                  |
    | cc      | 00000011  | Logical 'and' condition                           |
    | cc      | 00000022  | Logical 'and' condition                           |
    | cc      | 01000002  | Logical 'or' condition                            |
    | cc      | 01000010  | Logical 'or' condition                            |
    | cc      | 02000011  | Combination of logical 'and' and 'or' conditions  |
    | cc      | 02000022  | Combination of logical 'and' and 'or' conditions  |
    | cc      | 03000012  | Combination of logical 'and' and 'or' conditions  |
    | cc      | 03000030  | Combination of logical 'and' and 'or' conditions  |
