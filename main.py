import re
import sys
import colorama

inputFileName = "AssemblyCode.txt"
outputFileName = "machineCode.ram"
program = []

ALUinputMap = {"R0": "000", "R1": "001", "R2": "010", "R3": "011", "R4": "100", "R5": "101", "R6": "110", "R7": "111",
            "MOV": "0000", "ADD": "0001", "SUB": "0010", "ADC": "0011", "SBC": "0100", "AND": "0101", "XOR": "0110",
            "LSR": "0111", "LDR": "1000", "STR": "1010"}

JUMPinputMap = {"JMP": "11000000", "JNE": "11000010", "JCS": "11000100", "JMI": "11000110", "JGE": "11001000",
            "JGT": "11001010", "JHI": "11001100", "JSR": "11001110", "JEQ": "11000011", "JCC": "11000101", "JPL": "11000111", "JLT": "11001001",
            "JLE": "11001011", "JLS": "11001101", "RET": "11001111"}

colorama.init()

RED = '\033[31m'   # mode 31 = red forground
RESET = '\033[0m'  # mode 0  = reset


def val_to_bin(val, n_bits):
    bit_format = "{0:0" + str(n_bits) + "b}"
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


outputType = input("Output mode h or b (hex or binary): ").lower()
if not (outputType == "h" or outputType == "b"):
    print(RED + "Error: Invalid input for output mode" + RESET)
    sys.exit()

lineNumbers = input("Do you want line numbers in output file y/n: ").lower()
if not(lineNumbers == "y" or lineNumbers == "n"):
    print(RED + "ERROR: Invalid response" + RESET)
    sys.exit()

try:
    f = open(inputFileName)
    fileLine = f.readline()
    lineCount = 0
    while fileLine:
        instruction = re.split(r", #| #|, | ", re.compile(r"\n").sub("", fileLine.upper()))
        machineCode = ""
        try:
            machineCode += ALUinputMap.get(instruction[0])
            try:
                machineCode += ALUinputMap.get(instruction[1])
                insLen = len(instruction)
                if insLen == 3:
                    try:
                        machineCode += ("1" + val_to_bin(instruction[2], 8))
                    except ValueError:
                        print(RED + "ERROR: Invalid number on line " + str(lineCount) + RESET)
                elif insLen == 4:
                    try:
                        machineCode += ("0" + ALUinputMap.get(instruction[2]))
                    except TypeError:
                        print(RED + "ERROR: Second register on line " + str(lineCount) + " is invalid" + RESET)
                    try:
                        machineCode +=  val_to_bin(instruction[3], 5)
                    except TypeError:
                        print(RED + "ERROR: Invalid number on line " + str(lineCount) + RESET)
                else:
                    print(RED + "ERROR: Invalid number of elements on line " + str(lineCount) + RESET)

            except TypeError:
                print(RED + "ERROR: First register on line " + str(lineCount) + " is invalid" + RESET)

        except TypeError:
            try:
                machineCode += (JUMPinputMap.get(instruction[0]) + val_to_bin(instruction[1], 8))
            except TypeError:
                print(RED + "ERROR: Invalid instruction on line " + str(lineCount) + RESET)
            except ValueError:
                print(RED + "ERROR: Invalid number on line " + str(lineCount) + RESET)

        program.append(machineCode)

        lineCount += 1
        fileLine = f.readline()

    f.close()
except FileNotFoundError:
    print(RED + "ERROR: " + RESET + "File " + RED + inputFileName + RESET + " not found")

f = open(outputFileName, "w")

if outputType == "b":
    for lineNum, line in enumerate(program):
        if (lineNumbers == "y"):
            f.write("0x" + format(lineNum, 'x') + "  ")
        f.write("0b" + line + "\n")
else:
    for lineNum, line in enumerate(program):
        if (lineNumbers == "y"):
            f.write("0x" + format(lineNum, 'x') + "  ")
        tmp = int(line, 2)
        f.write("0x" + format(tmp, 'x') + "\n")

f.close()
