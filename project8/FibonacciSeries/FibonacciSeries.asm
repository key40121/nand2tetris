

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


// pop pointer 1
// SP--
@SP
AM=M-1
D=M
// RAM[THAT] = RAM[SP]
@THAT
M=D


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


// pop that 0
// Compute address RAM[THAT] + 0 and store in R13
@THAT
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


// pop that 1
// Compute address RAM[THAT] + 1 and store in R13
@THAT
D=M
@1
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


// push constant 2
// D = 2
@2
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
// if-goto
@SP
M=M-1
A=M
D=M
@COMPUTE_ELEMENT
D;JNE

// goto
@END
0;JMP

// label
(COMPUTE_ELEMENT)



// push that 0
// D = RAM[THAT]
@THAT
D=M
// A = D + 0
@0
A=D+A
// D = RAM[THAT] + 0
D=M
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1


// push that 1
// D = RAM[THAT]
@THAT
D=M
// A = D + 1
@1
A=D+A
// D = RAM[THAT] + 1
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


// pop that 2
// Compute address RAM[THAT] + 2 and store in R13
@THAT
D=M
@2
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


// push pointer 1
// D = RAM[THAT]
@THAT
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


// add
@SP
M=M-1
A=M
D=M
A=A-1
M=D+M


// pop pointer 1
// SP--
@SP
AM=M-1
D=M
// RAM[THAT] = RAM[SP]
@THAT
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
// goto
@LOOP
0;JMP

// label
(END)

