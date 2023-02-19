# !/usr/bin/env python3
# -*- coding : utf-8 -*-
import os
files = os.listdir("")

for fname in files:
    if (fname[-4] != 'v') or (fname[-3] != 'm') :
        print(fname)
        continue
    f = open(fname, mode='r', encoding='utf-8')
    oriname = fname.replace('.vmrk', '')
    # new_name = oriname+'_new.vmrk'
    #

    wordlist = []
    elselist = []
    j = 0
    for line in f:
        if j <= 10:
            elselist.append(line)
            j +=1
            continue
        else:
            a = line.split(',')
            #a[1] = a[1].replace(' ','')
            wordlist.append(a)
            #else:
        #	print(a)
        #/ Users / zhengchuhua / Documents / EXP_procedure / Analysis / marker_SD
    f.close()
    new_file = open(fname, "w")
    for t in elselist:
        new_file.write(t)
    for i in range(len(wordlist)):
        a = wordlist[i][1]
        if i < (len(wordlist)-1):
            if wordlist[i+1][1] == 'S  1' or wordlist[i+1][1] == 'S  2':
                     a = 'S1'+a[-2]+a[-1]
            elif wordlist[i+1][1] == 'S  3' or wordlist[i+1][1] == 'S  4':
                     a = 'S2'+a[-2]+a[-1]
            wordlist[i][1] = a
        k = 0

        for j in wordlist[i]:
            if k >= (len(wordlist[i])-1):
                new_file.write(j)
            else:
                k+=1
                new_file.write(j+',')
    new_file.close()

#	print(list)

