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


// push constant 4000
// D = 4000
@4000
D=A
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1


// pop pointer 0
// SP--
@SP
AM=M-1
D=M
// RAM[THIS] = RAM[SP]
@THIS
M=D


// push constant 5000
// D = 5000
@5000
D=A
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
// call
@Sys.main$ret.1
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

@Sys.main
0;JMP
(Sys.main$ret.1)



// pop temp 1
// SP--
@SP
AM=M-1
D=M
// RAM[6] = RAM[SP]
@6
M=D
// label
(LOOP)

// goto
@LOOP
0;JMP

// function Sys.main 5
(Sys.main)
@SP
A=M
M=0
@SP
M=M+1
@SP
A=M
M=0
@SP
M=M+1
@SP
A=M
M=0
@SP
M=M+1
@SP
A=M
M=0
@SP
M=M+1
@SP
A=M
M=0
@SP
M=M+1


// push constant 4001
// D = 4001
@4001
D=A
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1


// pop pointer 0
// SP--
@SP
AM=M-1
D=M
// RAM[THIS] = RAM[SP]
@THIS
M=D


// push constant 5001
// D = 5001
@5001
D=A
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


// push constant 200
// D = 200
@200
D=A
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1


// pop local 1
// Compute address RAM[LCL] + 1 and store in R13
@LCL
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


// push constant 40
// D = 40
@40
D=A
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1


// pop local 2
// Compute address RAM[LCL] + 2 and store in R13
@LCL
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


// pop local 3
// Compute address RAM[LCL] + 3 and store in R13
@LCL
D=M
@3
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


// push constant 123
// D = 123
@123
D=A
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1
// call
@Sys.add12$ret.2
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

@Sys.add12
0;JMP
(Sys.add12$ret.2)



// pop temp 0
// SP--
@SP
AM=M-1
D=M
// RAM[5] = RAM[SP]
@5
M=D


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


// push local 2
// D = RAM[LCL]
@LCL
D=M
// A = D + 2
@2
A=D+A
// D = RAM[LCL] + 2
D=M
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1


// push local 3
// D = RAM[LCL]
@LCL
D=M
// A = D + 3
@3
A=D+A
// D = RAM[LCL] + 3
D=M
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1


// push local 4
// D = RAM[LCL]
@LCL
D=M
// A = D + 4
@4
A=D+A
// D = RAM[LCL] + 4
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


// add
@SP
M=M-1
A=M
D=M
A=A-1
M=D+M


// add
@SP
M=M-1
A=M
D=M
A=A-1
M=D+M


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
// function Sys.add12 0
(Sys.add12)


// push constant 4002
// D = 4002
@4002
D=A
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1


// pop pointer 0
// SP--
@SP
AM=M-1
D=M
// RAM[THIS] = RAM[SP]
@THIS
M=D


// push constant 5002
// D = 5002
@5002
D=A
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


// push constant 12
// D = 12
@12
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
