// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

(INF_LOOP)
    @KBD
    D=M
    @key
    M=D // key = KBD
    @BLACK
    D;JNE //if RAM[KBD]!=0 then black screen
    @INF_LOOP
    0;JMP

    (BLACK)
        @i
        M=0 // i=0
        @SCREEN
        D=A
        @cur
        M=D //cur == first base address of screen
        (BLACK_LOOP)
            @i
            D=M //D=i
            @8192
            D=D-A
            @END_BLACK_LOOP
            D;JGE //if (i-8106) >= 0 go to end of loop
            @cur
            A=M
            M=-1

            //black this register
            @i
            D=M //D=i
            @i
            M=M+1
            @BLACK_LOOP
            0;JMP
        (END_BLACK_LOOP)
        @KBD
        D=M
        @key
        M=D // key = KBD
        @WHITE
        D;JEQ //if RAM[KBD]==0 then white screen
        @BLACK
        0;JMP //else: check again

    (WHITE)
        (WHITE_LOOP)
            @BLACK_LOOP
            0;JMP
        (END_WHITE_LOOP)
        @KBD
        D=M
        @key
        M=D // key = KBD
        @BLACK
        D;JNE //if RAM[KBD]!=0 then black screen
        @WHITE
        0;JMP //else: check again



    @INF_LOOP
    0;JMP