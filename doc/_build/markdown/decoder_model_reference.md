# MC decoder model refernece


### class mcdecoder.core.McDecoder(namespace_prefix: str, machine_decoder: mcdecoder.core.MachineDecoder, instruction_decoders: List[mcdecoder.core.InstructionDecoder], extras: Optional[Any])
Bases: `object`

Decoder itself. The root model element of MC decoder model


#### extras( = None)
User-defined data not related to a machine, an instruction and a field


#### instruction_decoders( = None)
Instruction decoders


#### machine_decoder( = None)
Machine decoder


#### namespace_prefix( = None)
Namespace prefix of generated codes


### class mcdecoder.core.MachineDecoder(extras: Optional[Any])
Bases: `object`

Decoder for a machine


#### extras( = None)
User-defined data for a machine


### class mcdecoder.core.InstructionDecoder(name: str, fixed_bits_mask: int, fixed_bits: int, type_bit_size: int, conditions: List[mcdecoder.core.InstructionDecodeCondition], field_decoders: List[mcdecoder.core.InstructionFieldDecoder], extras: Optional[Any])
Bases: `object`

Decoder for an instruction


#### conditions( = None)
Conditions an instruction must be satisfy


#### extras( = None)
User-defined data for an instruction


#### field_decoders( = None)
Field decoders


#### fixed_bits( = None)
Fixed bits of an instruction


#### fixed_bits_mask( = None)
Mask of fixed bit positions of an instruction


#### name( = None)
Name of an instruction


#### type_bit_size( = None)
Bit size of a data type used for an instruction


### class mcdecoder.core.InRangeInstructionDecodeCondition(field: str, value_start: int, value_end: int, type: str = 'in_range')
Bases: `mcdecoder.core.InstructionDecodeCondition`

An in-range condition subclass for InstructionDecodeCondition to express an instruction field is in a value range(inclusive)


#### field( = None)
Name of a field to be tested


#### type( = 'in_range')
Type of InstructionDecodeCondition


#### value_end( = None)
End of a value range a field must be in


#### value_start( = None)
Start of a value range a field must be in


### class mcdecoder.core.EqualityInstructionDecodeCondition(field: str, operator: str, value: int, type: str = 'equality')
Bases: `mcdecoder.core.InstructionDecodeCondition`

An equality condition subclass for InstructionDecodeCondition to express a field value’s equality to a value like !=, >, >=, <, <=, etc.


#### field( = None)
Name of a field to be tested


#### operator( = None)
Operator to test


#### type( = 'equality')
Type of InstructionDecodeCondition


#### value( = None)
Value to be tested with


### class mcdecoder.core.InstructionDecodeCondition()
Bases: `object`

A condition of instruction encoding when an instruction applys.
Each subclass must have a string attribute ‘type’ to express the type of a subclass.


### class mcdecoder.core.InstructionFieldDecoder(name: str, start_bit: int, type_bit_size: int, subfield_decoders: List[mcdecoder.core.InstructionSubfieldDecoder], extras: Optional[Any])
Bases: `object`

Decoder for an instruction field


#### extras( = None)
User-defined data for a field


#### name( = None)
Name of a field


#### start_bit( = None)
MSB of a field


#### subfield_decoders( = None)
Subfield decoders


#### type_bit_size( = None)
Bit size of data type used for a field


### class mcdecoder.core.InstructionSubfieldDecoder(index: int, mask: int, start_bit_in_instruction: int, end_bit_in_instruction: int, end_bit_in_field: int)
Bases: `object`

Decoder for a instruction subfield


#### end_bit_in_field( = None)
LSB of a subfield in a field


#### end_bit_in_instruction( = None)
LSB of a subfield in an instruction


#### index( = None)
Index number of a subfield in a field: 0th to (n-1)th


#### mask( = None)
Mask of a subfield in an instruction


#### start_bit_in_instruction( = None)
MSB of a subfield in an instruction
