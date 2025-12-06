// push constant 10
// D = 10
@10
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
// push constant 21
// D = 21
@21
D=A
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1
// push constant 22
// D = 22
@22
D=A
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1
// pop argument 2
// Compute address RAM[ARG] + 2 and store in R13
@ARG
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
// pop argument 1
// Compute address RAM[ARG] + 1 and store in R13
@ARG
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
// push constant 36
// D = 36
@36
D=A
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1
// pop this 6
// Compute address RAM[THIS] + 6 and store in R13
@THIS
D=M
@6
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
// push constant 42
// D = 42
@42
D=A
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1
// push constant 45
// D = 45
@45
D=A
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1
// pop that 5
// Compute address RAM[THAT] + 5 and store in R13
@THAT
D=M
@5
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
// push constant 510
// D = 510
@510
D=A
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1
// pop temp 6
// SP--
@SP
AM=M-1
D=M
// RAM[11] = RAM[SP]
@11
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
// push that 5
// D = RAM[THAT]
@THAT
D=M
// A = D + 5
@5
A=D+A
// D = RAM[THAT] + 5
D=M
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1
// add
// SP--
@SP
M=M-1
A=M
D=M
// R13 = *SP - 1
 @R13
M=D
// SP--
@SP
M=M-1
A=M
// D = *SP + R13
D=M+D
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1
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
// SP--
@SP
M=M-1
A=M
D=M
// R13 = *SP - 1
 @R13
M=D
// SP--
@SP
M=M-1
A=M
// D = *SP - R13
D=M-D
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1
// push this 6
// D = RAM[THIS]
@THIS
D=M
// A = D + 6
@6
A=D+A
// D = RAM[THIS] + 6
D=M
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1
// push this 6
// D = RAM[THIS]
@THIS
D=M
// A = D + 6
@6
A=D+A
// D = RAM[THIS] + 6
D=M
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1
// add
// SP--
@SP
M=M-1
A=M
D=M
// R13 = *SP - 1
 @R13
M=D
// SP--
@SP
M=M-1
A=M
// D = *SP + R13
D=M+D
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1
// sub
// SP--
@SP
M=M-1
A=M
D=M
// R13 = *SP - 1
 @R13
M=D
// SP--
@SP
M=M-1
A=M
// D = *SP - R13
D=M-D
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1
// push temp 6
// D = RAM[11]
@11
D=M
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1
// add
// SP--
@SP
M=M-1
A=M
D=M
// R13 = *SP - 1
 @R13
M=D
// SP--
@SP
M=M-1
A=M
// D = *SP + R13
D=M+D
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1
