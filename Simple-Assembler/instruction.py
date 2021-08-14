
def isImm(instn):
	return int(instn) < 256

def isHalt(instn):
	return len(instn) == 1

def get_opcode(command):
	opcode = {"add": "00000", "sub" : "00001" , "movI" : "00010" , "movR" : "00011",
	"ld" : "00100" , "st" : "00101" , "mul": "00110" , "div" : "00111" ,
	"rs" : "01000" , "ls" : "01001" , "xor":"01010" ,"or" : "01011" ,
	"and" : "01100", "not" : "01101" ,"cmp" : "01110", "jmp":"01111" , 
	"jlt" : "10000" , "jgt": "10001" , "je" : "10010" , "hlt" : "10011"}
	return str(opcode[command])

def get_regAddr(reg1, line_no):
	regdict = {"R0" : "000" , "R1" : "001" , "R2" : "010" , "R3" : "011" ,
	 			"R4" : "100", "R5" : "101" , "R6" : "110"}
	if reg1 == "FLAGS":
		raise Exception("Illegal use of FLAGS at line number", line_no)
	if(reg1 in regdict):
		return str(regdict[reg1])
	else : 
		raise Exception("Error : Register Not Found at Line number: ", line_no)

def get_regAddrfl(reg1, line_no):
	regdict = {"R0" : "000" , "R1" : "001" , "R2" : "010" , "R3" : "011" ,
	 			"R4" : "100", "R5" : "101" , "R6" : "110" , "FLAGS" : "111"}
	if(reg1 in regdict):
		return str(regdict[reg1])
	else :
		raise Exception("Error : Register Not Found at Line number: ", line_no)

def typeA(instn, machine_code, addr_and_pc):

	if(len(instn) == 4):
		rd = get_regAddr(instn[1], addr_and_pc[1])
		rs1 = get_regAddr(instn[2], addr_and_pc[1])
		rs2 = get_regAddr(instn[3], addr_and_pc[1])
		opcode = get_opcode(instn[0])
		unused = "00"
		machine_code.append(opcode + unused + rd + rs1 + rs2 )
		addr_and_pc[0] += 1
	else:
		raise Exception("Syntax Error at line number ", addr_and_pc[1])
		

		

def typeB(instn, machine_code, addr_and_pc):
	if(len(instn) == 3):
		if(isImm(instn[2][1:])):
			rd = get_regAddr(instn[1], addr_and_pc[1])
			opcode = get_opcode(instn[0])
			i = int(instn[2][1:])
			binary = bin(i)[2:]
			imm = binary.zfill(8)
			machine_code.append(opcode + rd + imm)
			addr_and_pc[0] += 1
			
		else:
			raise Exception("Error  : Illegal Immediate value at line number", addr_and_pc[1])
	else:
		raise Exception("Syntax Error at line number ", addr_and_pc[1])



def typeC(instn, machine_code, addr_and_pc):
	if(len(instn) == 3):
		if instn[0] == "movR":
			rd = get_regAddr(instn[1], addr_and_pc[1])
			rs = get_regAddrfl(instn[2], addr_and_pc[1])
		else:
			rd = get_regAddr(instn[1], addr_and_pc[1])
			rs = get_regAddr(instn[2], addr_and_pc[1])
		opcode = get_opcode(instn[0])
		unused = "00000"
		machine_code.append(opcode + unused + rd + rs)
		addr_and_pc[0] += 1
	else:
		raise Exception("Syntax Error at line number ", addr_and_pc[1])


def typeD(instn, machine_code, addr_and_pc, vars):
	if (len(instn) ==3):
		a = get_regAddr(instn[1], addr_and_pc[1])
		op = get_opcode(instn[0])
		try:
			memad = vars[instn[2]]
		except:
			raise Exception("Variable not declared at line number ", addr_and_pc[1])
		machine_code.append(op + a + memad)
		addr_and_pc[0] += 1
	else:
		raise Exception("Syntax Error at line number ", addr_and_pc[1])


def typeE(instn, machine_code, addr_and_pc, labels):
	if(len(instn)==2):
		op = get_opcode(instn[0])
		redundant = "000"
		try:
			memad = labels[instn[1]]
		except:
			raise Exception("Invalid label at line number ", addr_and_pc[1])
		machine_code.append(op + redundant + memad)
		addr_and_pc[0] += 1
	else:
		raise Exception("Syntax Error at line number ", addr_and_pc[1])



def typeF(instn, machine_code, addr_and_pc):
	if(isHalt(instn)):
		opcode =get_opcode(instn[0])
		unused = "00000000000"
		machine_code.append(opcode + unused)
		addr_and_pc[0] += 1
		addr_and_pc[2] = 1
	else:	
		raise Exception("Syntax Error at line number ", addr_and_pc[1])



def itr(instn, machine_code, addr_and_pc, labels, vars):
	if instn[0] == "mov":
		try:
			index = instn[2].find('$')
		except:
			raise Exception("Syntax")
		if(index == 0):
			instn[0] = "movI"
		else:
			instn[0] = "movR"

	instn_type = { "A": ["add" , "sub" , "mul" , "xor" , "or" , "and" ],
				   "B" : ["movI" , "rs","ls"], 
				   "C" : ["movR", "div" ,"not" , "cmp"] , 
				   "D" : ["ld" , "st"],
				   "E" : ["jmp" , "jlp" , "jgt" , "je"] ,
				   "F" :["hlt"]
				 }
	if instn[0] in instn_type["A"]:
		typeA(instn, machine_code, addr_and_pc)
	elif instn[0] in instn_type["B"]:
		typeB(instn, machine_code, addr_and_pc)
	elif instn[0] in instn_type["C"]:
		typeC(instn, machine_code, addr_and_pc)
	elif instn[0] in instn_type["D"]:
		typeD(instn, machine_code, addr_and_pc, vars)
	elif instn[0] in instn_type["E"]:
		typeE(instn, machine_code, addr_and_pc, labels)
	else:
		typeF(instn, machine_code, addr_and_pc)
		