# EEP1-Assembly-To-Machine-Code
Convert Assembly code to machine code for the EEP1 cpu

The compiler is not case-sensitive, however the standard is to write assembly in uppercase. 
This compiler will accept values written in any of the following formats:
  
• 0x01            &nbsp;  &nbsp; (hex)  
• -0x01           &nbsp;  &nbsp; (hex)  
• #-0x01          &nbsp;  &nbsp; (hex)  
• #0x01           &nbsp;  &nbsp; (hex)  
• #-1              &nbsp; &nbsp; (decimal)  
• #1              &nbsp; &nbsp; (decimal)  
• 1               &nbsp; &nbsp; (decimal)  
• -1             &nbsp; &nbsp; (decimal)  
• 0b1            &nbsp; &nbsp; (binary)  
• #0b01          &nbsp; &nbsp; (binary)  
• #-0b01         &nbsp; &nbsp; (binary)  
• -0b1           &nbsp; &nbsp; (binary)  

Example input file code:

MOV R0, #94
LSR R6, R0, 12
JMP 0x45
add R6 0b010110

• As you can see the compiler is flexible when it comes to comma usage and hashtag usage, however '0x' and '0b' must be included when using binary and hex values
• The inital input and output file names are "AssemblyCode.txt" and "machineCode.ram" respectively, however these can be changed at the top of the python script.
