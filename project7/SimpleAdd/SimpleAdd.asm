

// push constant 7
// D = 7
@7
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


// add
@SP
M=M-1
A=M
D=M
A=A-1
M=D+M
