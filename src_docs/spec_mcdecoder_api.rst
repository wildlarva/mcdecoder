###############################
MC decoder API specification
###############################

*********************************
Usage
*********************************

Here's an example of using :code:`DecodeInstruction` (without namespace).

.. code-block:: c

    #include "mcdecoder.h"

    /* Decode an instruction */
    const uint8_t kCodes[] = { 0x00, 0x48, 0x2d, 0xe9, };

    DecodeRequest request;
    DecodeResult result;
    bool succeeded;

    request.codes = &kCodes[0];
    succeeded = DecodeInstruction(&request, &result);

    /* Decoding succeeded? */
    if (succeeded) {
        /* Which instruction is decoded? */
        switch (result.instruction_id) {
        case InstructionId_k_push:
            /* Get the decoded result for push */
            printf("instruction: push\n");
            printf("cond: %d\n", result.instruction.push.cond);
            printf("register_list: %d\n", result.instruction.push.register_list);
            break;
        case InstructionId_kUnknown:
            /* Handle an unknown instruction */
            break;
        }
    }

*********************************
Types
*********************************

.. c:struct:: DecodeRequest

    Decoding request

    .. c:member:: const uint8_t *codes

        Codes to be input

.. c:struct:: DecodeResult

    Decoding result

    .. c:member:: InstructionId instruction_id

        Decoded instruction id

    .. c:union:: instruction

        Decoding result for an instruction

        .. c:member:: InstructionDecodeResult_<instruction> <instruction>

            Decoding result for <instruction>

            where

            * <instruction>: Instruction name

.. c:enum:: InstructionId

    Instruction id to identify a decoded instruction

    .. c:enumerator:: InstructionId_k_<instruction>

        Id for <instruction>

        where

        * <instruction>: Instruction name

    .. c:enumerator:: InstructionId_kUnknown

        Id for an unknown instruction

.. c:struct:: InstructionDecodeResult_<instruction>

    Decoding result for <instruction>

    where

    * <instruction>: Instruction name

    .. c:member:: <type> <field>

        Decoding result for <field>

        where

        * <type>: Appropriate unsigned integer type for the field: :code:`uint8_t`, :code:`uint16_t` or :code:`uint32_t`
        * <field>: Field name

*********************************
Macros
*********************************

.. c:var:: InstructionId INSTRUCTION_ID_MAX

    Number of instruction ids

*********************************
Functions
*********************************

.. c:function:: bool DecodeInstruction(const DecodeRequest *request, DecodeResult *result)

    Decode an instruction

    :param request: Decoding request
    :param result: Decoding result
    :return: :code:`true` if an instruction matches codes. :code:`false` otherwise
