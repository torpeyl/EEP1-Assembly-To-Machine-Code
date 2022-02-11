import re
import sys

program = []
counter = 1
tmp = ""
outputMode = ""


def val_to_bin(n_bits, val):
    bit_format = "{0:0" + str(n_bits) + "b}"
    if val[0] == "#":
        val = val[1:]
    if "0x" in val.lower():
        if "-" in val:
            tmp = int(val, 16) + 2 ** n_bits
            if tmp < (2 ** (n_bits - 1)) or tmp > (2 ** n_bits - 1):
                return None
        else:
            tmp = int(val, 16)
            if tmp < 0 or tmp > (2 ** n_bits) - 1:
                return None
        return bit_format.format(tmp)
    elif "0b" in val.lower():
        tmp = int(val, 2)
        if tmp > (2 ** n_bits - 1):
            return None
        return bit_format.format(int(val, 2))
    else:
        tmp = int(val)
        if tmp < 0:
            tmp += (2 ** n_bits)
            if tmp < (2 ** (n_bits - 1)) or tmp > (2 ** n_bits - 1):
                return None
        if tmp > (2 ** n_bits - 1):
            return None
        return bit_format.format(tmp)


outputMode = input("Type 'h' to have the output written in hex, or 'b' to have the output in binary: ")
if outputMode != 'h' and outputMode != 'b':
    print("Unrecognised output mode")
    sys.exit()

while tmp.lower() != "end":
    tmp = input(str(counter) + " >>> ")
    if tmp.lower() != "end":
        program.append(tmp)
    else:
        print("\n")
    counter += 1

inputMap = {"R0": "000", "R1": "001", "R2": "010", "R3": "011", "R4": "100", "R5": "101", "R6": "110", "R7": "111",
            "MOV": "000", "ADD": "001", "SUB": "010", "ADC": "011",
            "LDR": "100", "STR": "101", "JMP": "0000", "JNE": "0010", "JCS": "0100", "JMI": "0110", "JGE": "1000",
            "JGT": "1010", "JHI": "1100", "JSR": "1110", "JEQ": "0011", "JCC": "0101", "JPL": "0111", "JLT": "1001",
            "JLE": "1011", "JLS": "1101", "RET": "1111"}

for i in range(len(program)):
    tmp_li = re.split(" ", program[i])
    if tmp_li[0] == "":
        tmp_li = tmp_li[1:]
    for j, item in enumerate(tmp_li):
        tmp_li[j] = item.upper()
    instruction = ""
    if tmp_li[0] == "MOV" or tmp_li[0] == "ADD" or tmp_li[0] == "SUB" or tmp_li[0] == "ADC":
        if len(tmp_li) == 3:
            instruction = "0"
            instruction += inputMap.get(tmp_li[0])
            instruction += inputMap.get(tmp_li[1])
            try:
                tmp = val_to_bin(8, tmp_li[2])
                if tmp is not None:
                    instruction += tmp
                else:
                    print("ERROR: Number is not appropriate for 8 bit representation on line " + str(i + 1))
                    continue
            except ValueError:
                instruction += "0"
                instruction += inputMap.get(tmp_li[2])
                instruction += "{0:05b}".format(0, 16)

        elif len(tmp_li) == 4:
            instruction = "0"
            instruction += inputMap.get(tmp_li[0])
            instruction += inputMap.get(tmp_li[1])
            instruction += "0"
            instruction += inputMap.get(tmp_li[2])
            tmp = val_to_bin(5, tmp_li[3])
            if tmp is not None:
                instruction += tmp
            else:
                print("ERROR: Number is not appropriate for 5 bit representation on line " + str(i + 1))
                continue
        else:
            print("ERROR: Invalid number of elements on line " + str(i+1))
            continue

    elif tmp_li[0] == "LDR" or tmp_li[0] == "STR":
        instruction = "10"
        if tmp_li[0] == "LDR":
            instruction += "0"
        else:
            instruction += "1"
        instruction += "0"
        instruction += inputMap.get(tmp_li[1])
        if len(tmp_li) == 3:
            instruction += "1"
            tmp = val_to_bin(8, tmp_li[2])
            if tmp is not None:
                instruction += tmp
            else:
                print("ERROR: Number is not appropriate for 8 bit representation on line " + str(i + 1))
                continue
        elif len(tmp_li) == 4:
            instruction += "0"
            instruction += inputMap.get(tmp_li[2])
            tmp = val_to_bin(5, tmp_li[3])
            if tmp is not None:
                instruction += tmp
            else:
                print("ERROR: Number is not appropriate for 5 bit representation on line " + str(i + 1))
                continue
        else:
            print("ERROR: Invalid number of elements on line " + str(i + 1))
            continue

    else:
        try:
            instruction = "1100"
            instruction += inputMap.get(tmp_li[0])
            try:
                tmp = val_to_bin(8, tmp_li[1])
            except IndexError:
                print("ERROR: Invalid number of elements on line " + str(i + 1))
                continue
            if tmp is not None:
                instruction += tmp
            else:
                print("ERROR: Number is not appropriate for 8 bit representation on line " + str(i + 1))
                continue
        except TypeError:
            print("Error on line " + str(i + 1) + ", invalid operation")
            continue

    if outputMode == "b":
        print(str(i+1) + ": 0b" + instruction)
    else:
        tmp = int(instruction, 2)
        print(str(i+1) + ": 0x" + format(tmp, 'x'))

