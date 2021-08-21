import Execution_Engine
from sys import stdin
import matplotlib.pyplot as plt

def initialization(memory):
    for inst in stdin:
        memory.append(inst.strip())

def display(pc, reg):
    pc = bin(pc)[2:]
    pc = pc.zfill(8)
    print(pc, end = " ")
    regs = reg.keys()
    regs = list(regs)
    for i in regs[:-1]:
        val = bin(reg[i])[2:]
        val = val.zfill(16)
        print(val, end=" ")
    flgs = reg["111"].zfill(16)
    print(flgs)

def main():

    memory = []
    pc = 0
    hlt = 1
    pc_and_halt = [pc, hlt]
    cc = 0
    var = {}
    cc_x = []
    pc_y = []
    register_file = {"000": 0, "001": 0, "010": 0, "011": 0, "100": 0, "101": 0, "110": 0, "111": "0000"}

    initialization(memory)
   
    while pc_and_halt[1]:
        instn = memory[pc]
        Execution_Engine.exec(instn, pc_and_halt, register_file, var)
        display(pc, register_file)
        cc_x.append(cc)
        if instn[:5] == "00101" or instn[:5] == "00100":
            a = (int(instn[-8:], 2))
            pc_y.append(a)
            cc_x.append(cc)
        pc_y.append(pc)
        pc = pc_and_halt[0]
        cc += 1
    vkeys = var.keys()
    vkeys = list(vkeys)
    vkeys.sort()
    i = len(memory) + len(vkeys)

    for v in vkeys:
        memory.append(bin(var[v])[2:].zfill(16))
    while i != 256:
        memory.append("0000000000000000")
        i = i + 1
    for line in memory:
        print(line)

    plt.scatter(cc_x,pc_y)
    plt.xlabel("Cycle Number")
    plt.ylabel("Memory Address")
    plt.show()

if __name__ == '__main__':
    main()


