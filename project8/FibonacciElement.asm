// Bootstrap code
@256
D=A
@SP
M=D
// call Sys.init
// call
@Sys.init$ret.0
D=A
@SP
A=M
M=D
@SP
M=M+1

// push LCL
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1

// push ARG
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1

// push THIS
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1

// push THAT
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1

// Reposition ARG
@SP
D=M
@5
D=D-A
@ARG
M=D

// Reposition LCL
@SP
D=M
@LCL
M=D

@Sys.init
0;JMP
(Sys.init$ret.0)

// function Sys.init 0
(Sys.init)


// push constant 4
// D = 4
@4
D=A
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1
// call
@Main.fibonacci$ret.1
D=A
@SP
A=M
M=D
@SP
M=M+1

// push LCL
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1

// push ARG
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1

// push THIS
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1

// push THAT
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1

// Reposition ARG
@SP
D=M
@6
D=D-A
@ARG
M=D

// Reposition LCL
@SP
D=M
@LCL
M=D

@Main.fibonacci
0;JMP
(Main.fibonacci$ret.1)

// label
(END)

// goto
@END
0;JMP

// function Main.fibonacci 0
(Main.fibonacci)


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


// lt
@SP
AM=M-1
D=M
A=A-1
D=M-D
@LT_TRUE2
D;JLT
@SP
A=M-1
M=0
@LT_END2
0;JMP
(LT_TRUE2)
@SP
A=M-1
M=-1
(LT_END2)
// if-goto
@SP
M=M-1
A=M
D=M
@N_LT_2
D;JNE

// goto
@N_GE_2
0;JMP

// label
(N_LT_2)



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
// label
(N_GE_2)



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
// call
@Main.fibonacci$ret.3
D=A
@SP
A=M
M=D
@SP
M=M+1

// push LCL
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1

// push ARG
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1

// push THIS
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1

// push THAT
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1

// Reposition ARG
@SP
D=M
@6
D=D-A
@ARG
M=D

// Reposition LCL
@SP
D=M
@LCL
M=D

@Main.fibonacci
0;JMP
(Main.fibonacci$ret.3)



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
// call
@Main.fibonacci$ret.4
D=A
@SP
A=M
M=D
@SP
M=M+1

// push LCL
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1

// push ARG
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1

// push THIS
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1

// push THAT
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1

// Reposition ARG
@SP
D=M
@6
D=D-A
@ARG
M=D

// Reposition LCL
@SP
D=M
@LCL
M=D

@Main.fibonacci
0;JMP
(Main.fibonacci$ret.4)



// add
@SP
M=M-1
A=M
D=M
A=A-1
M=D+M
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
