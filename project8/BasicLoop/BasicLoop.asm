

// push constant 0
// D = 0
@0
D=A
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1


// pop local 0
// Compute address RAM[LCL] + 0 and store in R13
@LCL
D=M
@0
D=D+A
@R13
M=D
// SP--
@SP
AM=M-1
D=M
// RAM[add] = RAM[SP]
@R13
A=M
M=D
// label
(LOOP)



// push argument 0
// D = RAM[ARG]
@ARG
D=M
// A = D + 0
@0
A=D+A
// D = RAM[ARG] + 0
D=M
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1


// push local 0
// D = RAM[LCL]
@LCL
D=M
// A = D + 0
@0
A=D+A
// D = RAM[LCL] + 0
D=M
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1


// add
@SP
M=M-1
A=M
D=M
A=A-1
M=D+M


// pop local 0
// Compute address RAM[LCL] + 0 and store in R13
@LCL
D=M
@0
D=D+A
@R13
M=D
// SP--
@SP
AM=M-1
D=M
// RAM[add] = RAM[SP]
@R13
A=M
M=D


// push argument 0
// D = RAM[ARG]
@ARG
D=M
// A = D + 0
@0
A=D+A
// D = RAM[ARG] + 0
D=M
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1


// push constant 1
// D = 1
@1
D=A
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1


// sub
@SP
M=M-1
A=M
D=M
A=A-1
M=M-D


// pop argument 0
// Compute address RAM[ARG] + 0 and store in R13
@ARG
D=M
@0
D=D+A
@R13
M=D
// SP--
@SP
AM=M-1
D=M
// RAM[add] = RAM[SP]
@R13
A=M
M=D


// push argument 0
// D = RAM[ARG]
@ARG
D=M
// A = D + 0
@0
A=D+A
// D = RAM[ARG] + 0
D=M
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1
// if-goto
@SP
M=M-1
A=M
D=M
@LOOP
D;JNE



// push local 0
// D = RAM[LCL]
@LCL
D=M
// A = D + 0
@0
A=D+A
// D = RAM[LCL] + 0
D=M
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1
