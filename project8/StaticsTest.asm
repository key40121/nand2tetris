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


// push constant 6
// D = 6
@6
D=A
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1


// push constant 8
// D = 8
@8
D=A
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1
// call
@Class1.set$ret.1
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
@7
D=D-A
@ARG
M=D

// Reposition LCL
@SP
D=M
@LCL
M=D

@Class1.set
0;JMP
(Class1.set$ret.1)



// pop temp 0
// SP--
@SP
AM=M-1
D=M
// RAM[5] = RAM[SP]
@5
M=D


// push constant 23
// D = 23
@23
D=A
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1


// push constant 15
// D = 15
@15
D=A
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1
// call
@Class2.set$ret.2
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
@7
D=D-A
@ARG
M=D

// Reposition LCL
@SP
D=M
@LCL
M=D

@Class2.set
0;JMP
(Class2.set$ret.2)



// pop temp 0
// SP--
@SP
AM=M-1
D=M
// RAM[5] = RAM[SP]
@5
M=D
// call
@Class1.get$ret.3
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

@Class1.get
0;JMP
(Class1.get$ret.3)

// call
@Class2.get$ret.4
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

@Class2.get
0;JMP
(Class2.get$ret.4)

// label
(END)

// goto
@END
0;JMP

// function Class1.set 0
(Class1.set)


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


// pop static 0
// SP--
@SP
AM=M-1
D=M
// RAM[16] = RAM[SP]
@16
M=D


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


// pop static 1
// SP--
@SP
AM=M-1
D=M
// RAM[17] = RAM[SP]
@17
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
// function Class1.get 0
(Class1.get)


// push static 0
// D = RAM[16]
@16
D=M
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1


// push static 1
// D = RAM[17]
@17
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
// function Class2.set 0
(Class2.set)


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


// pop static 0
// SP--
@SP
AM=M-1
D=M
// RAM[18] = RAM[SP]
@18
M=D


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


// pop static 1
// SP--
@SP
AM=M-1
D=M
// RAM[19] = RAM[SP]
@19
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
// function Class2.get 0
(Class2.get)


// push static 0
// D = RAM[18]
@18
D=M
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1


// push static 1
// D = RAM[19]
@19
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
