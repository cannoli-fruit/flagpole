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

var = {}

stack = []
ptr = -1
while True:
    ptr += 1
    if ptr >= len(tokens): break
    token = tokens[ptr]
    if DEBUG: print("Exec token: ", token)
    if DEBUG: print("Vars: ", var)
    if DEBUG: print("Stack: ", stack)
    if token.isnumeric():
        stack.append(int(token))
    # Instrinsic command, because golfing all are 1 char
    if len(token) == 1:
        # print
        if token == "~":
            print(stack.pop())
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
            if not cond: continue
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
            if cond: continue
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
            stack.append(lhs + rhs)
            continue
        if token == "*":
            rhs = stack.pop()
            lhs = stack.pop()
            stack.append(lhs * rhs)
            continue
        if token == "-":
            rhs = stack.pop()
            lhs = stack.pop()
            stack.append(lhs - rhs)
            continue
        if token == "%":
            rhs = stack.pop()
            lhs = stack.pop()
            stack.append(lhs % rhs)
            continue
        if token == "/":
            rhs = stack.pop()
            lhs = stack.pop()
            stack.append(lhs // rhs)
            continue
        if token == "|":
            rhs = stack.pop()
            lhs = stack.pop()
            stack.append(lhs | rhs)
            continue
        if token == "&":
            rhs = stack.pop()
            lhs = stack.pop()
            stack.append(lhs & rhs)
            continue
        if token == "^":
            rhs = stack.pop()
            lhs = stack.pop()
            stack.append(lhs ^ rhs)
            continue
        if token == "!":
            stack[-1] = not stack[-1]
            continue
        if token == "<":
            rhs = stack.pop()
            lhs = stack.pop()
            stack.append(int(lhs < rhs))
            continue
        if token == ">":
            rhs = stack.pop()
            lhs = stack.pop()
            stack.append(int(lhs > rhs))
            continue
        if token == "=":
            rhs = stack.pop()
            lhs = stack.pop()
            stack.append(int(lhs == rhs))
            continue
        # store
        if token == "@":
            var[tokens[ptr+1]] = stack.pop()
            ptr += 1
            continue
        # load
        if token == "#":
            stack.append(var[tokens[ptr+1]])
            ptr += 1
            continue
