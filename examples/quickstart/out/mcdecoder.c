#include "mcdecoder.h"


/*
 * Types
 */

typedef struct {
    const DecodeRequest *request;
    DecodeResult *result;
    uint16_t code16x1;
    uint32_t code16x2;
    uint32_t code32x1;
} DecodeContext;

typedef uint32_t (*SetBitCountFunction)(uint32_t value);


/*
 * Internal function declarations
 */

static bool DecisionNode_code32x1_0(DecodeContext *context, uint32_t code);
    static bool DecisionNode_code32x1_1(DecodeContext *context, uint32_t code);
    static bool DecisionNode_code32x1_2(DecodeContext *context, uint32_t code);
    

static bool DecodeInstruction_add_immediate_a1(DecodeContext *context);
static bool DecodeInstruction_push_a1(DecodeContext *context);

static uint32_t SetBitCount(uint32_t value);
static uint8_t BitElement(uint32_t value, uint8_t element_index);


/*
 * Internal global variables
 */

static const SetBitCountFunction setbit_count = SetBitCount;


/*
 * External function definitions
 */

/* decode function */
bool DecodeInstruction(const DecodeRequest *request, DecodeResult *result) {
    const uint8_t *raw_code = request->codes;
    uint16_t word1_16bit = *((uint16_t *) &raw_code[0]);
        uint16_t word2_16bit = *((uint16_t *) &raw_code[2]);
    

    DecodeContext context;
    context.request = request;
    context.result = result;
    context.code16x1 = word1_16bit;
    context.code16x2 = (((uint32_t) word1_16bit) << 16) | ((uint32_t) word2_16bit);
    context.code32x1 = *((uint32_t *) &raw_code[0]);
    
    if (DecisionNode_code32x1_0(&context, context.code32x1)) {
            return true;
        }
    
    return false;
}


/*
 * Internal function definitions
 */

/* decision node functions */
static bool DecisionNode_code32x1_0(DecodeContext *context, uint32_t code) {
            
            switch (code & 0x0fe00000) {
                    case 0x02800000:
                            if (DecisionNode_code32x1_1(context, code)) {
                                return true;
                            }
                            break;
                    case 0x09200000:
                            if (DecisionNode_code32x1_2(context, code)) {
                                return true;
                            }
                            break;
                    
                default:
                    break;
                }
            
            
            return false;
        }
    static bool DecisionNode_code32x1_1(DecodeContext *context, uint32_t code) {
            if (DecodeInstruction_add_immediate_a1(context)) {
                    return true;
                }
            
            
            
            return false;
        }
    static bool DecisionNode_code32x1_2(DecodeContext *context, uint32_t code) {
            if (DecodeInstruction_push_a1(context)) {
                    return true;
                }
            
            
            
            return false;
        }
    


/* individual decode functions */

    static bool DecodeInstruction_add_immediate_a1(DecodeContext *context) {
        if ((context->code32x1 & (0x0fe00000l)) != (0x02800000l)) {
            return false;
        }

        context->result->instruction_id = InstructionId_k_add_immediate_a1;
        context->result->instruction.add_immediate_a1.cond =
            (((context->code32x1 & (0xf0000000l)) >> (28)) << (0));
            
        context->result->instruction.add_immediate_a1.S =
            (((context->code32x1 & (0x00100000l)) >> (20)) << (0));
            
        context->result->instruction.add_immediate_a1.Rn =
            (((context->code32x1 & (0x000f0000l)) >> (16)) << (0));
            
        context->result->instruction.add_immediate_a1.Rd =
            (((context->code32x1 & (0x0000f000l)) >> (12)) << (0));
            
        context->result->instruction.add_immediate_a1.imm12 =
            (((context->code32x1 & (0x00000fffl)) >> (0)) << (0));
            
        
        
        
        return true;
    }

    static bool DecodeInstruction_push_a1(DecodeContext *context) {
        if ((context->code32x1 & (0x0fff0000l)) != (0x092d0000l)) {
            return false;
        }

        context->result->instruction_id = InstructionId_k_push_a1;
        context->result->instruction.push_a1.cond =
            (((context->code32x1 & (0xf0000000l)) >> (28)) << (0));
            
        context->result->instruction.push_a1.register_list =
            (((context->code32x1 & (0x0000ffffl)) >> (0)) << (0));
            
        
        
        
        return true;
    }


/* functions for conditions */
static uint32_t SetBitCount(uint32_t value) {
    uint32_t count = 0;
    while (value) {
        count += value & 1;
        value >>= 1;
    }
    return count;
}

static uint8_t BitElement(uint32_t value, uint8_t element_index) {
    return (value & (1u << element_index)) >> element_index;
}