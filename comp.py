#!/usr/bin/env python3
import sys

# Compile to qbe

DEBUG = False

chartypes = [
    list("0123456789"),
    list("!|&^+-*/%=<>[]{}$:_;.,"),
    list("@#"),
]

whitespace = " \n"

def tokenize(txt):
    tokens = []
    buf = ""
    tokenType = -1
    for char in txt:
        if tokenType == -1:
            if char in chartypes[0]:
                tokenType = 0
                buf += char
            elif char in chartypes[1]:
                tokenType = 1
                buf += char
            elif char in chartypes[2]:
                tokenType = 2
                buf += char
            continue
        if tokenType == 0:
            if char in chartypes[0]:
                buf += char
            elif char in whitespace:
                tokens.append({"typ": 0, "val": buf})
                buf = ""
                tokenType = -1
                continue
            else:
                print("Nonnumeric char found in numeric token")
                exit(127)
            continue
        if tokenType == 1:
            if char in chartypes[1]:
                buf += char
            elif char in whitespace:
                tokens.append({"typ": 1, "val": buf})
                buf = ""
                tokenType = -1
                continue
            else:
                print("Invalid symbolic token found")
                exit(254)
            continue
        if tokenType == 2:
            if char in chartypes[1] or char in chartypes[2]:
                print("Invalid identifier")
                exit(125)
            elif char in whitespace:
                tokens.append({"typ": 2, "val": buf})
                buf = ""
                tokenType = -1
                continue
            else:
                buf += char
            continue
    return tokens

src = ""
with open(sys.argv[1], "r") as f:
    src = f.read()

bracketstack = []
def bracketpush(i):
    bracketstack.append(i)
    return i

def bracketpop():
    return bracketstack.pop()

tokens = tokenize(src)

print("data $stack = { z 8192 }")
print("data $sp = { l 0 }")

print("export function w $push(l %val) {")
print("@start")
print("  %sp_ptr =l add $sp, 0")
print("  %sp_val =l loadl %sp_ptr")

print("  %base =l add $stack, 0")
print("  %off =l shl %sp_val, 3")
print("  %cond =l csgel %off, 8192")
print("  jnz %cond, @overflow, @ok") # underflow is your problem
                                     # overflow is mb
print("@ok")
print("  %addr =l add %base, %off")
print("  storel %val, %addr")

print("  %new_sp =l add %sp_val, 1")
print("  storel %new_sp, $sp")

print("  ret 0")
print("@overflow")
print("  call $puts(l $overflowmsg)")
print("  call $exit(w 1)")
print("  ret 1")
print("}")

print("export function l $pop() {")
print("@start")
print("  %sp_ptr =l add $sp, 0")
print("  %sp_val =l loadl %sp_ptr")

print("  %new_sp =l sub %sp_val, 1")
print("  storel %new_sp, $sp")

print("  %base =l add $stack, 0")
print("  %off =l shl %new_sp, 3")

print("  %addr =l add %base, %off")
print("  %val =l loadl %addr")
print("  ret %val")
print("}")

print("export function w $pushint(l %x) {")
print("@start")
print("  %imm_ptr =l call $malloc(w 16)")
print("  %imm_ptr_val =l add %imm_ptr, 8")
print("  storel 1, %imm_ptr")
print("  storel %x, %imm_ptr_val")
print("  call $push(l %imm_ptr)")
print("  ret 0")
print("}")

print("export function w $add() {")
print("@start")
print("  %imm_ptr_1 =l call $pop()")
print("  %imm_ptr_2 =l call $pop()")
print("  %imm_ptr_3 =l call $malloc(w 16)")
print("  %imm_ptr_3_vp =l add %imm_ptr_3, 8")
print("  %imm_ptr_1_vp =l add %imm_ptr_1, 8")
print("  %imm_ptr_1_v =l loadl %imm_ptr_1_vp")
print("  %imm_ptr_2_vp =l add %imm_ptr_2, 8")
print("  %imm_ptr_2_v =l loadl %imm_ptr_2_vp")
print("  %imm_ptr_sum =l add %imm_ptr_1_v, %imm_ptr_2_v")
print("  storel 1, %imm_ptr_3")
print("  storel %imm_ptr_sum, %imm_ptr_3_vp")
print("  call $push(l %imm_ptr_3)")
print("  ret 0")
print("}")

print("export function w $sub() {")
print("@start")
print("  %imm_ptr_1 =l call $pop()")
print("  %imm_ptr_2 =l call $pop()")
print("  %imm_ptr_3 =l call $malloc(w 16)")
print("  %imm_ptr_3_vp =l add %imm_ptr_3, 8")
print("  %imm_ptr_1_vp =l add %imm_ptr_1, 8")
print("  %imm_ptr_1_v =l loadl %imm_ptr_1_vp")
print("  %imm_ptr_2_vp =l add %imm_ptr_2, 8")
print("  %imm_ptr_2_v =l loadl %imm_ptr_2_vp")
print("  %imm_ptr_diff =l sub %imm_ptr_1_v, %imm_ptr_2_v")
print("  storel 1, %imm_ptr_3")
print("  storel %imm_ptr_diff, %imm_ptr_3_vp")
print("  call $push(l %imm_ptr_3)")
print("  ret 0")
print("}")

print("export function w $main() {")
print("@start")

if DEBUG:
    with open("/dev/tty", "w") as console:
        print(tokens, file=console)

for i, token in enumerate(tokens):
    if DEBUG:
        with open("/dev/tty", "w") as console:
            print(f"{i} {token["typ"]} {token["val"]}", file=console)
    tVal = token["val"]
    if token["typ"] == 0:
        print(f"  call $pushint(l {tVal})")
    elif token["typ"] == 1:
        if token["val"] == "+":
            print("  call $add()")
        if token["val"] == "-":
            print("  call $sub()")
        if token["val"] == ".":
            print(f"  %imm_ptr_{i} =l call $pop()")
            print(f"  %imm_ptr_{i}_vp =l add %imm_ptr_{i}, 8")
            print(f"  %imm_ptr_{i}_v =w loadw %imm_ptr_{i}_vp")
            print(f"  %dummy_{i} =l call $putchar(w %imm_ptr_{i}_v)")
        if token["val"] == "{":
            print(f"@loopstart{bracketpush(i)}")
        if token["val"] == "}":
            bidx = bracketpop()
            print(f"  %imm_ptr_{i} =l call $pop()")
            print(f"  %imm_ptr_{i}_vp =l add %imm_ptr_{i}, 8")
            print(f"  %imm_ptr_{i}_v =l loadl %imm_ptr_{i}_vp")
            print(f"  jnz %imm_ptr_{i}_v, @loopstart{bidx}, @loopend{bidx}")
            print(f"@loopend{bidx}")
        if token["val"] == ":":
            print(f"  %imm_ptr_{i} =l call $pop()")
            print(f"  call $push(l %imm_ptr_{i})")
            print(f"  call $push(l %imm_ptr_{i})")
        if token["val"] == "$":
            print(f"  %imm_ptr_{i}_a =l call $pop()")
            print(f"  %imm_ptr_{i}_b =l call $pop()")
            print(f"  call $push(l %imm_ptr_{i}_a)")
            print(f"  call $push(l %imm_ptr_{i}_b)")
        if token["val"] == "<":
            print(f"  %imm_ptr_{i}_a =l call $pop()")
            print(f"  %imm_ptr_{i}_b =l call $pop()")
            print(f"  %imm_ptr_{i}_avp =l add %imm_ptr_{i}_a, 1")
            print(f"  %imm_ptr_{i}_bvp =l add %imm_ptr_{i}_b, 1")
            print(f"  %imm_ptr_{i}_av =l loadl %imm_ptr_{i}_avp")
            print(f"  %imm_ptr_{i}_bv =l loadl %imm_ptr_{i}_bvp")
            print(f"  %imm_ptr_{i}_c =l csgtl %imm_ptr_{i}_av, %imm_ptr_{i}_bv")
            print(f"  %imm_ptr_{i}_v =l call $malloc(w 16)")
            print(f"  %imm_ptr_{i}_vv =l add %imm_ptr_{i}_v, 8")
            print(f"  storel 1, %imm_ptr_{i}_v")
            print(f"  storel %imm_ptr_{i}_c, %imm_ptr_{i}_vv")
            print(f"  call $push(l %imm_ptr_{i}_v)")
        if token["val"] == "<":
            print(f"  %imm_ptr_{i}_a =l call $pop()")
            print(f"  %imm_ptr_{i}_b =l call $pop()")
            print(f"  %imm_ptr_{i}_avp =l add %imm_ptr_{i}_a, 1")
            print(f"  %imm_ptr_{i}_bvp =l add %imm_ptr_{i}_b, 1")
            print(f"  %imm_ptr_{i}_av =l loadl %imm_ptr_{i}_avp")
            print(f"  %imm_ptr_{i}_bv =l loadl %imm_ptr_{i}_bvp")
            print(f"  %imm_ptr_{i}_c =l csltl %imm_ptr_{i}_av, %imm_ptr_{i}_bv")
            print(f"  %imm_ptr_{i}_v =l call $malloc(w 16)")
            print(f"  %imm_ptr_{i}_vv =l add %imm_ptr_{i}_v, 8")
            print(f"  storel 1, %imm_ptr_{i}_v")
            print(f"  storel %imm_ptr_{i}_c, %imm_ptr_{i}_vv")
            print(f"  call $push(l %imm_ptr_{i}_v)")
    elif token["typ"] == 2:
        print(f"\n# Token: {token["val"]} of type 2")
        if token["val"][0] == "#":
            print(f"  call $push(l %{token["val"][1:]})")
        if token["val"][0] == "@":
            print(f"  %stacktop_{i} =l call $pop()")
            print(f"  storel %{token["val"][1:]}, %stacktop_{i}")
        if token["val"][0] == "$":
            print(f"  %stacktop_{i} =l call $pop()")
            print(f"  %{token["val"][1:]} =l loadl %stacktop_{i}")



print("  ret 0")
print("}")
print("data $overflowmsg = { b \"Stack overflow!\" }")
