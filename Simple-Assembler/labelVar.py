
def isLabel(instn, labels, var, addr):
	opcode = ["add", "sub", "mov", "ld", "st", "mul", "div",
			  "rs", "ls", "xor", "or", "and", "not", "cmp", "jmp", "jlt", "jgt", "je"
		, "hlt"]
	reg = ["R0", "R1", "R2", "R3", "R4", "R5", "R6", "FLAGS"]
	if instn[0][:-1] in var:
		raise Exception("Label name used as a variable or vice-versa at line number ", addr[1])
	if instn[0][:-1] in reg or instn[0][:-1] in opcode or instn[0][:-1] in labels:
		return False
	for i in instn[0][:-1]:
		if i.lower() not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '_', 'a', 'b', 'c', 'd', 'e', 'f', 'g',
							 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
							 'z']:
			return False
	isd = instn[1].isdigit()
	if isd:
		return False
	return True

def label(instn, labels, var, addr):
	if isLabel(instn, labels, var, addr):
		addr[0] += 1
		a = bin(addr[0])[2:].zfill(8)
		labels[instn[0][:-1]] = a
	else:
		raise Exception("Label name incorrect at line number ", addr[1])

def isVar(instn, var):
	opcode = ["add", "sub", "mov", "ld", "st", "mul", "div",
			  "rs", "ls", "xor", "or", "and", "not", "cmp", "jmp", "jlt", "jgt", "je"
		, "hlt"]
	reg = ["R0", "R1", "R2", "R3", "R4", "R5", "R6", "FLAGS"]
	if instn[1] in var or instn[1] in reg or instn[1] in opcode:
		return False
	for i in instn[1]:
		if i.lower() not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '_', 'a', 'b', 'c', 'd', 'e', 'f', 'g',
							 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
							 'z']:
			return False
	isd = instn[1].isdigit()
	if isd:
		return False
	return True


def variable(instn, var, addr):
	if isVar(instn, var):
		var[instn[1]] = "00000000"
	else:
		raise Exception("Variable name incorrect at line number ", addr[1])
