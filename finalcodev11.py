import re
import sys
from deeplator import Translator

# Usage - python finalcodev10.py -i inputsrtfile.txt -o outputsrtfile.txt -lf EN -lt DE
inpfile = outpfile = lf = lt = ''

for i in sys.argv:
    if i == '-i':
        iindex = sys.argv.index(i)
        inpfile = sys.argv[iindex+1]
    if i == '-o':
        oindex = sys.argv.index(i)
        outpfile = sys.argv[oindex+1]
    if i == '-lf':
        lfindex = sys.argv.index(i)
        lf = sys.argv[lfindex+1]
    if i == '-lt':
        ltindex = sys.argv.index(i)
        lt = sys.argv[ltindex+1]

allparams = 1
if inpfile == '' or outpfile == '' or lf == '' or lt == '':
    allparams = 0
    print ('  ')
    print ('Error - Missing parameter(s)')
    print ('Usage - python finalcodev10.py -i inputsrtfile.txt -o outputsrtfile.txt -lf EN -lt DE')
    print ('Supported languages - DE  German, EN  English, FR  French, ES  Spanish, IT  Italian, NL  Dutch, PL  Polish')
    print ('  ')


def getindexofpartialfromarray(arraytosearchin, texttosearch):
    i = 0;
    for line in arraytosearchin:
        if bool(texttosearch in line):
            return i
        else:
            i+=1
    return -1

def find_str(s, char):
    index = 0

    if char in s:
        c = char[0]
        for ch in s:
            if ch == c:
                if s[index:index+len(char)] == char:
                    return index

            index += 1

    return -1


if allparams:
    print ('  ')
    print ('  ')
    print ("File: "+inpfile+" will be translated from "+lf+" to "+lt+" and the output will be saved in the file: "+outpfile)
    print ('  ')
    print ('  ')
    
    t = Translator(lf, lt)

    data = []
    data.append([])
    data.append([])

    with open (inpfile, 'rt') as in_file:
        for line in in_file:
            data[0].append(line.rstrip('\n'))
            data[1].append('')




    textonly = []
    textonly.append([])
    textonly.append([])
    textonly.append([])

    for line in data[0]:
        if line.isdigit() or bool(re.search('([0-9][0-9]:[0-9][0-9]:[0-9][0-9],[0-9][0-9][0-9])', line)) or line == '':
            currindex = data[0].index(line)
            data[1][currindex] = line
        else:
            textonly[0].append(line)
            textonly[1].append('')
            textindex = data[0].index(line)
            textonly[2].append(textindex)
    #print (data)
    #print (textonly)

    lines2trans = []
    lines2trans.append([])
    lines2trans.append([])
    lines2trans.append([])

    for line in textonly[0]:
        if bool(re.search('(\.)', line)):
            splitline = line.split('.')
            for sents in splitline:
                if sents != '':
                    # print (len(splitline))
                    # print (splitline.index(sents) + 1)
                    if len(splitline) != splitline.index(sents) + 1:    
                        lines2trans[0].append(sents+'.')
                    else:
                        lines2trans[0].append(sents)
                    lines2trans[1].append(getindexofpartialfromarray(textonly[0], sents))
                    lines2trans[2].append(len(sents.split()))
        else:
            lines2trans[0].append(line)
            lines2trans[1].append(getindexofpartialfromarray(textonly[0], line))
            lines2trans[2].append(len(line.split()))

    #print (lines2trans)

    currsent = ''
    startindex = ''
    endindex = ''

    for line in lines2trans[0]:
        if startindex == '':
            startindex = lines2trans[0].index(line)
        if bool(re.search('(\.)', line)):
            currsent = currsent + line + ' '
            currtrans = t.translate_sentences(currsent)
            endindex = lines2trans[0].index(line)

            lencurrtrans = len(currtrans[0])
            lencurrsent  = len(currsent)

            transsplit = []
            transstart = 0
            for sn in range(startindex, endindex+1):
                print ("Progress: " + str(sn) + " of "+str(endindex+1))

                lensncurr  = len(lines2trans[0][sn])
                lensntrans = int(round(lensncurr / lencurrsent * lencurrtrans))

                snstart = find_str(currsent, lines2trans[0][sn])
                snend = 0

                if sn == endindex:
                    sntrans = currtrans[0][snstart:]
                else:
                    snend = snstart+lensncurr+1
                    # for i in range(0, lencurrsent):
                    #     if currsent[snend] == ' ':
                    #         break
                    #     snend+=1
                    # sntrans = currtrans[0][snstart:snstart+lensncurr]
                    sntrans = currtrans[0][snstart:snend]
                textonly[1][lines2trans[1][sn]] += sntrans

            currsent = ''
            startindex = ''
        else:
            currsent = currsent + line + ' '

    for line in textonly[1]:
        tbrow = textonly[2][getindexofpartialfromarray(textonly[1], line)]
        data[1][tbrow] = line

    fh = open(outpfile,"w") 
    for lines in data[1]:
        fh.write(lines+'\n') 
    fh.close()

    print ("Now you can open the output file " + outpfile + " and see the results. Thank you for using this program.") 

