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

// Put your code here.
(INIT)
  // address が指すメモリにスクリーンの最初の address を保持する
  // Build-in Symbol の @SCREEN には、 16384 の値が設定されている
  @SCREEN
  D=A
  @address
  M=D

  // Build-in Symbol
  @KBD
  D=M

  @BLACK
  D;JGT

  @WHITE
  0;JMP

(BLACK)
  @color
  M=-1
  @ENDIF
  0;JMP
(WHITE)
  @color
  M=0
(ENDIF)

(LOOP)
  @color
  D=M
  // スクリーンの色の更新処理を実装
  @address
  A=M
  M=D
  // 操作する対象のアドレスをインクリメント
  @address
  M=M+1

  // for ループを回す回数を定義
  @SCREEN
  D=A
  // for ループを回す回数
  @8194
  D=D+A
  // 更新状況を表すパラメーターで for 文の真ん中の項に相当
  @address
  D=D-M

  // for 文の右の項 (終了条件) に相当
  @LOOP
  D;JGT

  @INIT
  0;JMP
