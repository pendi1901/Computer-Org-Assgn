import labelVar
import instruction
from sys import stdin

def isInstruction(instn):
	opcode = ["add", "sub", "mov","ld", "st", "mul", "div",
	"rs","ls","xor" ,"or" ,"and", "not","cmp", "jmp", "jlt", "jgt", "je"
	, "hlt"]
	return instn in opcode

def isBlankLine(line):

	return len(line) == 1

def main():
	prog_cnter = 1
	mem_addr = -1
	hlt_count= 0
	addr_and_pc = [ mem_addr, prog_cnter, hlt_count]
	storeLabel = {}
	storeVar = {}
	input_list = []
	machine_code = []

	for each in stdin:
		line = each.strip().split()

		if isBlankLine(line):
			addr_and_pc[1] = addr_and_pc[1] + 1
			continue

		input_list.append(line)
		if addr_and_pc[2] == 1:
			raise Exception(addr_and_pc[1] - 1, "Halt not the last instruction at line number ", addr_and_pc[1])

		elif line[0][-1] == ":":
			labelVar.label(line, storeLabel, storeVar, addr_and_pc)
			if len(line) == 1:
				raise Exception("Syntax Error at line number ", addr_and_pc[1])
			if line[1] == 'hlt':
				if len(line) == 2:
					addr_and_pc[2] = 1
				else:
					raise Exception("Syntax Error at line number", addr_and_pc[1])

		elif line[0] == "var":
			if len(line) != 2:
				raise Exception("Syntax Error at line number ", addr_and_pc[1])
			if addr_and_pc[0] != -1:
				raise Exception("Variable not declared at the beginning", addr_and_pc[1])
			labelVar.variable(line, storeVar, addr_and_pc)
		
		elif line[0] == "hlt":
			if len(line) == 1:
				addr_and_pc[2] = 1
				addr_and_pc[0] += 1
			else:
				raise Exception("Syntax Error at line number", addr_and_pc[1])
		
		else:
			addr_and_pc[0] += 1
		addr_and_pc[1] += 1
	if addr_and_pc[2] == 0:
		raise Exception("Halt statement missing at line number", addr_and_pc[1])

	for v in storeVar.keys():
		addr_and_pc[0] += 1
		memad = bin(addr_and_pc[0])[2:].zfill(8)
		storeVar[v] = memad
	addr_and_pc[1] = 1
	addr_and_pc[0] = -1

	# SECOND ITERATION
	for line in input_list:

		if line[0][-1] == ":":
			if len(line) == 1:
				raise Exception("Syntax Error at line number ", addr_and_pc[1])
			if isInstruction(line[1]):
				instruction.itr(line[1:], machine_code, addr_and_pc, storeLabel, storeVar)
			else:
				raise Exception("Wrong instruction at line number ", addr_and_pc[1])

		elif line[0] == "var":
			addr_and_pc[1] += 1
			continue

		elif isInstruction(line[0]):
			instruction.itr(line, machine_code, addr_and_pc, storeLabel, storeVar)

		else:
			if len(line[0]) <= 3:
				raise Exception("Instruction Typo at line number", addr_and_pc[1])
			else:
				raise Exception("General Error at line number", addr_and_pc[1])
		addr_and_pc[1] += 1

	for result in machine_code:
		print(result)

if __name__ == '__main__':
	main()