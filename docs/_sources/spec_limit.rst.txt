############################
Limitations
############################

Generated decoders have the limitations below:

* The decoder codes are in C language(C11 standard).

  * However, you can define decoder codes in other programming languages with user templates.

* The host computer which runs the decoders must be of little endian.
* The bit length of instruction encodings must be 16 bit or 32 bit.

  * The decoder does not support others, such as 8 bit, 24 bit, 64 bit, etc.

* Multiple instructions must not match a certain bit pattern.

  * The decoder finds only one matching instruction in this case.
