

// push constant 17
// D = 17
@17
D=A
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1


// push constant 17
// D = 17
@17
D=A
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1


// eq
@SP
AM=M-1
D=M
A=A-1
D=M-D
@EQ_TRUE0
D;JEQ
@SP
A=M-1
M=0
@EQ_END0
0;JMP
(EQ_TRUE0)
@SP
A=M-1
M=-1
(EQ_END0)


// push constant 17
// D = 17
@17
D=A
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1


// push constant 16
// D = 16
@16
D=A
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1


// eq
@SP
AM=M-1
D=M
A=A-1
D=M-D
@EQ_TRUE1
D;JEQ
@SP
A=M-1
M=0
@EQ_END1
0;JMP
(EQ_TRUE1)
@SP
A=M-1
M=-1
(EQ_END1)


// push constant 16
// D = 16
@16
D=A
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1


// push constant 17
// D = 17
@17
D=A
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1


// eq
@SP
AM=M-1
D=M
A=A-1
D=M-D
@EQ_TRUE2
D;JEQ
@SP
A=M-1
M=0
@EQ_END2
0;JMP
(EQ_TRUE2)
@SP
A=M-1
M=-1
(EQ_END2)


// push constant 892
// D = 892
@892
D=A
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1


// push constant 891
// D = 891
@891
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
@LT_TRUE3
D;JLT
@SP
A=M-1
M=0
@LT_END3
0;JMP
(LT_TRUE3)
@SP
A=M-1
M=-1
(LT_END3)


// push constant 891
// D = 891
@891
D=A
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1


// push constant 892
// D = 892
@892
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
@LT_TRUE4
D;JLT
@SP
A=M-1
M=0
@LT_END4
0;JMP
(LT_TRUE4)
@SP
A=M-1
M=-1
(LT_END4)


// push constant 891
// D = 891
@891
D=A
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1


// push constant 891
// D = 891
@891
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
@LT_TRUE5
D;JLT
@SP
A=M-1
M=0
@LT_END5
0;JMP
(LT_TRUE5)
@SP
A=M-1
M=-1
(LT_END5)


// push constant 32767
// D = 32767
@32767
D=A
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1


// push constant 32766
// D = 32766
@32766
D=A
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1


// gt
@SP
AM=M-1
D=M
A=A-1
D=M-D
@GT_TRUE6
D;JGT
@SP
A=M-1
M=0
@GT_END6
0;JMP
(GT_TRUE6)
@SP
A=M-1
M=-1
(GT_END6)


// push constant 32766
// D = 32766
@32766
D=A
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1


// push constant 32767
// D = 32767
@32767
D=A
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1


// gt
@SP
AM=M-1
D=M
A=A-1
D=M-D
@GT_TRUE7
D;JGT
@SP
A=M-1
M=0
@GT_END7
0;JMP
(GT_TRUE7)
@SP
A=M-1
M=-1
(GT_END7)


// push constant 32766
// D = 32766
@32766
D=A
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1


// push constant 32766
// D = 32766
@32766
D=A
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1


// gt
@SP
AM=M-1
D=M
A=A-1
D=M-D
@GT_TRUE8
D;JGT
@SP
A=M-1
M=0
@GT_END8
0;JMP
(GT_TRUE8)
@SP
A=M-1
M=-1
(GT_END8)


// push constant 57
// D = 57
@57
D=A
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1


// push constant 31
// D = 31
@31
D=A
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1


// push constant 53
// D = 53
@53
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


// push constant 112
// D = 112
@112
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


// neg
@SP
A=M-1
M=-M
// and
@SP
AM=M-1
D=M
A=A-1
M=D&M


// push constant 82
// D = 82
@82
D=A
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1
//or
@SP
AM=M-1
D=M
A=A-1
M=D|M


// not
@SP
A=M-1
M=!M
