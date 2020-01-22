#ifndef _MC_DECODER_H_
#define _MC_DECODER_H_

#include <stdint.h>
#include <stdbool.h>


/*
 * Types
 */

/** Decoding request */
typedef struct {
	const uint8_t *codes;	/** Codes to be input */
} DecodeRequest;

/** Instruction id to identify a decoded instruction */
typedef enum {
	InstructionId_k_add_immediate_a1,	/** add_immediate_a1 */
	InstructionId_k_push_a1,	/** push_a1 */
	
	InstructionId_kUnknown, /** Unknown instruction */
} InstructionId;

/** Number of instruction ids */
#define INSTRUCTION_ID_MAX InstructionId_kUnknown


	/** Decoding result for add_immediate_a1 */
	typedef struct {
		uint8_t cond;	/** Bit 31-28: Decoding result for cond */
		uint8_t S;	/** Bit 20-20: Decoding result for S */
		uint8_t Rn;	/** Bit 19-16: Decoding result for Rn */
		uint8_t Rd;	/** Bit 15-12: Decoding result for Rd */
		uint16_t imm12;	/** Bit 11-0: Decoding result for imm12 */
		
	} InstructionDecodeResult_add_immediate_a1;

	/** Decoding result for push_a1 */
	typedef struct {
		uint8_t cond;	/** Bit 31-28: Decoding result for cond */
		uint16_t register_list;	/** Bit 15-0: Decoding result for register_list */
		
	} InstructionDecodeResult_push_a1;


/** Decoding result */
typedef struct {
	InstructionId instruction_id;	/** Decoded instruction id */
    union {
		InstructionDecodeResult_add_immediate_a1 add_immediate_a1;	/** Decoding result for add_immediate_a1 */
		InstructionDecodeResult_push_a1 push_a1;	/** Decoding result for push_a1 */
		
    } instruction;	/** Decoding result for an instruction */
} DecodeResult;


/*
 * Functions
 */

/**
 * Decode an instruction
 *
 * @param request Decoding request
 * @param result Decoding result
 * @return True if decoding succeeded. False otherwise
 */
extern bool DecodeInstruction(const DecodeRequest *request, DecodeResult *result);


#endif /* !_MC_DECODER_H_ */