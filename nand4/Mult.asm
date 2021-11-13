// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.
@R0
D=M
@i
M=D
@0
D=A
@R2
M=D
(WHILE_LOOP)
	@i
	D=M
	@END_WHILE_LOOP
	D;JEQ
	@R1
	D=M
	@R2
	M=M+D
	@i
	M=M-1
	@WHILE_LOOP
	0;JMP
(END_WHILE_LOOP)
@END_WHILE_LOOP
0;JMP