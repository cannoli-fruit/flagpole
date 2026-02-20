# Flagpole
Custom golfing language interpreted in python

## TODO:
 - strings?
 - self host
 - compile

Currently doing project euler calculations as test programs.

## Reference:
 {}: Do while loop, condition is top of the stack when } is reached
 []: If statement, condition is top of the stack when [ is reached
 +: add top two numbers on the stack
 -: subtract top two numbers on the stack
 */%=<>|&^: etc (|&^ are bitwise operators)
 ~: print top value of the stack
 :: duplicate top value of the stack
 _: duplicate second value of the stack
 $: swap top two stack values
 @: treat next token as variable name, pop top value of stack and set variable.
 #: treat next token as variable name, push value to stack


