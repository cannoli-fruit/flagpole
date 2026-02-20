#!/usr/bin/env python3
import sys

DEBUG = False

if len(sys.argv) == 1:
    print("No file given!")

filename = sys.argv[1]
src = ""
with open(filename, "r") as f:
    src = f.read()

# TODO: an actual tokenizer, maybe, this works though
tokens = src.split()
if DEBUG: print("TOKENS: ", tokens)

class Data:
    def __init__(self, typ, val):
        self.typ = typ
        if typ == 0:
            self.int = val
        if typ == 1:
            self.arr = val

var = {}

stack = []
ptr = -1
while True:
    ptr += 1
    if ptr >= len(tokens): break
    token = tokens[ptr]
    if DEBUG: print("Vars: ", var)
    if DEBUG: print("Stack: ", stack)
    if DEBUG: print("Exec token: ", token)
    if token.isnumeric():
        stack.append(Data(0, int(token)))
    # Instrinsic Command
    if len(token) == 1:
        # print
        if token == "~":
            elt = stack.pop()
            if elt.typ == 0:
                print(elt.int)
            elif elt.typ == 1:
                for c in elt.arr:
                    print(chr(c))
            else:
                exit(255)
            continue
        # duplicate
        if token == ":":
            x = stack.pop()
            stack.append(x)
            stack.append(x)
            continue
        # over
        if token == "_":
            stack.append(stack[-2])
            continue
        # swap
        if token == "$":
            v1 = stack.pop()
            v2 = stack.pop()
            stack.append(v1)
            stack.append(v2)
            continue
        # open while
        if token == "{":
            continue
        # close while
        if token == "}":
            cond = stack.pop()
            if cond.typ != 0:
                print("Trying to branch based on non-condition type")
                exit(2)
            if not cond.int: continue
            idx = ptr
            depth = 1
            while idx >= 0:
                idx -= 1
                if tokens[idx] == "{":
                    depth -= 1
                elif tokens[idx] == "}":
                    depth += 1
                if depth == 0: break
            if depth != 0:
                print("Unmatched } found")
                exit(1)
            ptr = idx
            continue
        if token == "[":
            cond = stack.pop()
            if cond.typ != 0:
                print("Trying to branch based on non-condition type")
                exit(2)
            if cond.int: continue
            depth = 1
            idx = ptr + 1
            while idx < len(tokens):
                if tokens[idx] == "]":
                    depth -= 1
                if tokens[idx] == "[":
                    depth += 1
                if depth == 0: break
                idx += 1
            if depth != 0:
                print ("Unmatched [ found")
                exit(1)
            ptr = idx
            continue
        if token == "]":
            continue
        if token == "+":
            rhs = stack.pop()
            lhs = stack.pop()
            if rhs.typ == 0 and lhs.typ == 0:
                stack.append(Data(0,rhs.int+lhs.int))
            elif lhs.typ == 1:
                lhs.arr.append(rhs)
                stack.append(lhs)
            elif rhs.typ == 1 and lhs.typ == 0:
                print("Cannot add int + arr")
                exit(3)
            continue
        if token == "*":
            rhs = stack.pop()
            lhs = stack.pop()
            if lhs.typ == 0 and rhs.typ == 0:
                stack.append(Data(0,lhs.int * rhs.int))
            if lhs.typ == 0 and rhs.typ == 1:
                print("Cannot multiply int * arr")
                exit(4)
            if lhs.typ == 1 and rhs.typ == 0:
                stack.append(Data(1,lhs.arr * rhs.int))
            if lhs.typ == 1 and rhs.typ == 1:
                print("Cannot multiply two arrays")
                exit(5)
            continue
        if token == "-":
            rhs = stack.pop()
            lhs = stack.pop()
            if lhs.typ == 0 and rhs.typ == 0:
                stack.append(Data(0,lhs.int - rhs.int))
            if lhs.typ == 0 and rhs.typ == 1:
                print("Cannot subtract int - arr")
                exit(6)
            if lhs.typ == 1 and rhs.typ == 0:
                print("Cannot subtract arr - int")
                exit(7)
            if lhs.typ == 1 and rhs.typ == 1:
                print("Cannot subtract arr - arr")
                exit(8)
            continue
        if token == "%":
            rhs = stack.pop()
            lhs = stack.pop()
            if lhs.typ == 0 and rhs.typ == 0:
                stack.append(Data(0,lhs.int % rhs.int))
            if lhs.typ == 0 and rhs.typ == 1:
                print("Cannot mod int % arr")
                exit(9)
            if lhs.typ == 1 and rhs.typ == 0:
                print("Cannot mod arr % int")
                exit(10)
            if lhs.typ == 1 and rhs.typ == 1:
                print("Cannot mod arr % arr")
                exit(11)
            continue
        if token == "/":
            rhs = stack.pop()
            lhs = stack.pop()
            if lhs.typ == 0 and rhs.typ == 0:
                stack.append(Data(0,lhs.int // rhs.int))
            if lhs.typ == 0 and rhs.typ == 1:
                print("Cannot div int / arr")
                exit(12)
            if lhs.typ == 1 and rhs.typ == 0:
                print("Cannot div arr / int")
                exit(13)
            if lhs.typ == 1 and rhs.typ == 1:
                print("Cannot div arr / arr")
                exit(14)
            continue
        if token == "|":
            rhs = stack.pop()
            lhs = stack.pop()
            if lhs.typ == 0 and rhs.typ == 0:
                stack.append(Data(0,lhs.int | rhs.int))
            if lhs.typ == 0 and rhs.typ == 1:
                print("Cannot or int | arr")
                exit(15)
            if lhs.typ == 1 and rhs.typ == 0:
                print("Cannot or arr | int")
                exit(16)
            if lhs.typ == 1 and rhs.typ == 1:
                print("Cannot or arr | arr")
                exit(17)
            continue
        if token == "&":
            rhs = stack.pop()
            lhs = stack.pop()
            if lhs.typ == 0 and rhs.typ == 0:
                stack.append(Data(0,lhs.int & rhs.int))
            if lhs.typ == 0 and rhs.typ == 1:
                print("Cannot and int & arr")
                exit(18)
            if lhs.typ == 1 and rhs.typ == 0:
                print("Cannot and arr & int")
                exit(19)
            if lhs.typ == 1 and rhs.typ == 1:
                print("Cannot and arr & arr")
                exit(20)
            continue
        if token == "^":
            rhs = stack.pop()
            lhs = stack.pop()
            if lhs.typ == 0 and rhs.typ == 0:
                stack.append(Data(0,lhs.int ^ rhs.int))
            if lhs.typ == 0 and rhs.typ == 1:
                print("Cannot xor int ^ arr")
                exit(21)
            if lhs.typ == 1 and rhs.typ == 0:
                print("Cannot xor arr ^ int")
                exit(22)
            if lhs.typ == 1 and rhs.typ == 1:
                print("Cannot xor arr ^ arr")
                exit(23)
            continue
        if token == "!":
            x = stack.pop()
            if x.typ == 0:
                stack.append(Data(0,not x.int))
            else:
                print("Cannot negate arr")
                exit(24)
            continue
        if token == "<":
            rhs = stack.pop()
            lhs = stack.pop()
            if lhs.typ == 0 and rhs.typ == 0:
                stack.append(Data(0,int(lhs.int < rhs.int)))
            if lhs.typ == 0 and rhs.typ == 1:
                print("Cannot compare int < arr")
                exit(25)
            if lhs.typ == 1 and rhs.typ == 0:
                print("Cannot compare arr < int")
                exit(26)
            if lhs.typ == 1 and rhs.typ == 1:
                print("Cannot compare arr < arr")
                exit(27)
            continue
        if token == ">":
            rhs = stack.pop()
            lhs = stack.pop()
            if lhs.typ == 0 and rhs.typ == 0:
                stack.append(Data(0,int(lhs.int > rhs.int)))
            if lhs.typ == 0 and rhs.typ == 1:
                print("Cannot compare int > arr")
                exit(28)
            if lhs.typ == 1 and rhs.typ == 0:
                print("Cannot compare arr > int")
                exit(29)
            if lhs.typ == 1 and rhs.typ == 1:
                print("Cannot compare arr > arr")
                exit(30)
            continue
        if token == "=":
            rhs = stack.pop()
            lhs = stack.pop()
            if lhs.typ == 0 and rhs.typ == 0:
                stack.append(Data(0,int(lhs.int == rhs.int)))
            if lhs.typ == 0 and rhs.typ == 1:
                print("Cannot compare int = arr")
                exit(28)
            if lhs.typ == 1 and rhs.typ == 0:
                print("Cannot compare arr = int")
                exit(29)
            if lhs.typ == 1 and rhs.typ == 1:
                stack.append(Data(0,int(lhs.arr == rhs.arr)))
                exit(30)
            continue
        # store int
        if token == "@":
            var[tokens[ptr+1]] = stack.pop()
            ptr += 1
            continue
        # load int
        if token == "#":
            stack.append(var[tokens[ptr+1]])
            ptr += 1
            continue
        # array load
        if token == "'":
            idx = stack.pop()
            arr = stack.pop()
            if idx.typ != 0:
                print("Index must be an integer")
                exit(31)
            if arr.typ != 1:
                print("Array not found")
                exit(32)
            stack.append(arr.arr[idx.int])
            continue
        # array store
        if token == ";":
            val = stack.pop()
            idx = stack.pop()
            arr = stack.pop()
            if idx.typ != 0:
                print("Index must be an integer")
                exit(33)
            if arr.typ != 1:
                print("Array not found")
                exit(34)
            while len(arr.arr) <= idx.int:
                if val.typ == 0: arr.arr.append(Data(0,0))
                if val.typ == 1: arr.arr.append(Data(1,[]))
            arr.arr[idx.int] = val
            stack.append(arr)
        # char print
        if token == ".":
            val = stack.pop()
            if val.typ != 0:
                print("Non-integer type print fail")
                exit(35)
            print(chr(val.int),end="")
        # new array
        if token == ",":
            stack.append(Data(1,[]))



