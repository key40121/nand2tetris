// function SimpleFunction.test 2
(SimpleFunction.test)


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


// push local 1
// D = RAM[LCL]
@LCL
D=M
// A = D + 1
@1
A=D+A
// D = RAM[LCL] + 1
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


// not
@SP
A=M-1
M=!M


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


// add
@SP
M=M-1
A=M
D=M
A=A-1
M=D+M


// push argument 1
// D = RAM[ARG]
@ARG
D=M
// A = D + 1
@1
A=D+A
// D = RAM[ARG] + 1
D=M
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
// return
// FRAME = LCL
@LCL
D=M
@R13
M=D
// RET = *(FRAME-5)
@5
A=D-A
D=M
@R14
M=D
@SP
AM=M-1
D=M
@ARG
A=M
M=D
@ARG
D=M+1
@SP
M=D
@R13
AM=M-1
D=M
@THAT
M=D
@R13
AM=M-1
D=M
@THIS
M=D
@R13
AM=M-1
D=M
@ARG
M=D
@R13
AM=M-1
D=M
@LCL
M=D
@R14
A=M
0;JMP
