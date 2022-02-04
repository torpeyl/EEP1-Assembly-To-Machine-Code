import re
import sys

program = []
machineCode = []
counter = 1

tmp = ""
outputMode = ""
outputMode = input("Type 'h' to have the output written in hex, or 'b' to have the output in binary: ")
if outputMode != 'h' and outputMode != 'b':
    print("Unrecognised output mode")
    sys.exit()

while tmp != "exit":
    tmp = input(str(counter) + ": ")
    if tmp != "exit":
        program.append(tmp)
    counter += 1

inputMap = {"R0": "000", "R1": "001", "R2": "010", "R3": "011", "R4": "100", "R5": "101", "R6": "110", "R7": "111",
            "MOV": "000", "ADD": "001", "SUB": "010", "ADC": "011",
            "LDR": "100", "STR": "101", "JMP": "1100", "JNE": "1101", "JCS": "1110", "JMI": "1111"}

for i in range(len(program)):
    tmp_li = re.split(" ", program[i])
    if tmp_li[0] == "":
        tmp_li = tmp_li[1:]
    for j, item in enumerate(tmp_li):
        tmp_li[j] = item.upper()
    instruction = ""
    if tmp_li[0] == "MOV" or tmp_li[0] == "ADD" or tmp_li[0] == "SUB" or tmp_li[0] == "ADC":
        if len(tmp_li) == 3:
            instruction += "0"
            instruction += inputMap.get(tmp_li[0])
            instruction += inputMap.get(tmp_li[1])
            try:
                if int(tmp_li[2], 16) <= 0xFF:
                    instruction += "1"
                    instruction += "{0:08b}".format(int(tmp_li[2], 16))
                else:
                    print("ERROR: Number is greater than 8 bits on line " + str(i + 1))
                    sys.exit()
            except ValueError:
                instruction += "0"
                instruction += inputMap.get(tmp_li[2])
                instruction += "{0:05b}".format(0, 16)

        elif len(tmp_li) == 4:
            instruction += "0"
            instruction += inputMap.get(tmp_li[0])
            instruction += inputMap.get(tmp_li[1])
            instruction += "0"
            instruction += inputMap.get(tmp_li[2])
            if int(tmp_li[3], 16) <= 0x1F:
                instruction += "{0:08b}".format(int(tmp_li[3], 16))
            else:
                print("ERROR: Number is greater than 5 bits on line " + str(i+1))
                sys.exit()
        else:
            print("ERROR: Invalid number of elements on line " + str(i+1))
            sys.exit()


    elif tmp_li[0] == "LDR" or tmp_li[0] == "STR":
        instruction += "10"
        if tmp_li[0] == "LDR":
            instruction += "0"
        else:
            instruction += "1"
        instruction += "0"
        instruction += inputMap.get(tmp_li[1])
        if len(tmp_li == 3):
            instruction += "1"
            if int(tmp_li[2], 16) <= 0xFF:
                instruction += "{0:08b}".format(int(tmp_li[2], 16))
            else:
                print("ERROR: Number is greater than 8 bits on line " + str(i+1))
                sys.exit()
        elif len(tmp_li) == 4:
            instruction += "0"
            instruction += inputMap.get(tmp_li[2])
            if int(tmp_li[3], 16) <= 0x1F:
                instruction += "{0:08b}".format(int(tmp_li[3], 16))
            else:
                print("ERROR: Number is greater than 5 bits on line " + str(i + 1))
                sys.exit()
        else:
            print("ERROR: Invalid number of elements on line " + str(i + 1))
            sys.exit()

    elif tmp_li[0] == "JMP" or tmp_li[0] == "JNE" or tmp_li[0] == "JCS" or tmp_li[0] == "JMI":
        instruction += "1100"
        instruction += inputMap.get(tmp_li[0])
        instruction += "0"
        if int(tmp_li[1], 16) <= 0xFF:
            instruction += "{0:08b}".format(int(tmp_li[1], 16))
        else:
            print("ERROR: Number is greater than 8 bits on line " + str(i + 1))
            sys.exit()
    else:
        print("Error on line " + str(i+1) + ", invalid operation")
        sys.exit()
    machineCode.append(instruction)

for i in range(len(program)):
    if outputMode == "b":
        print("0b" + machineCode[i])
    else:
        tmp = int(machineCode[i], 2)
        print("0x" + format(tmp, 'x'))
