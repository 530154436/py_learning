# !/usr/bin/env python3
# -*- coding : utf-8 -*-
import os
import xlrd
import xlwt
BASE_DIR = '/Users/zhengchubin/Desktop'

p2Path = os.path.join(BASE_DIR, 'p2.xlsx')
frnPath = os.path.join(BASE_DIR, 'frn.xlsx')

def fileload(filename1, filename2):
    workbook1 = xlrd.open_workbook(filename1)
    workbook2 = xlrd.open_workbook(filename2)
    p2 = workbook1.sheets()[0]
    frn = workbook2.sheets()[0]
    newbook = xlwt.Workbook()
    sheet = newbook.add_sheet('frn-p2')
    books = []
    print(frn.nrows)
    print(frn.ncols)
    for row in range(p2.nrows):
        newcol = 0
        l1 = p2.row_values(row)
        l2 = frn.row_values(row)
        newRow = []
        for i in range(len(l1)):
            if (row==0 and i%2==0) or i==0:
                newRow.append(l1[i])
                sheet.write(row,newcol, l1[i])
                newcol +=1
            else:
                if i%2==0:
                    newRow.append(float(l2[i]) - float(l1[i]))
                    sheet.write(row, newcol, float(l2[i]) - float(l1[i]))
                    newcol+=1
        print('frn', l2)
        print('p2', l1)
        print(newRow, '\n')
        books.append(newRow)
    newbook.save(os.path.join(BASE_DIR, 'frn_p2.xls'))

def finalProcess(filename, mod=4, firsCols=1):
    workbook = xlrd.open_workbook(filename)
    sheet = workbook.sheets()[0]
    print(sheet.nrows)
    print(sheet.ncols)
    newbook = xlwt.Workbook()
    p1 = newbook.add_sheet('YY')
    p2 = newbook.add_sheet('YN')
    p3 = newbook.add_sheet('NY')
    p4 = newbook.add_sheet('NN')
    for row in range(sheet.nrows):
        newcol = 0
        rowVals = sheet.row_values(row)
        for i in range(len(rowVals)):
            if i < firsCols:
                p1.write(row, newcol, rowVals[i])
                p2.write(row, newcol, rowVals[i])
                p3.write(row, newcol, rowVals[i])
                p4.write(row, newcol, rowVals[i])
                newcol+=1
                continue
            if((i-firsCols)%mod==0):
                p1.write(row, newcol, rowVals[i])
            elif((i-firsCols)%mod==1):
                p2.write(row, newcol, rowVals[i])
            elif((i-firsCols)%mod==2):
                p3.write(row, newcol, rowVals[i])
            else:
                p4.write(row, newcol, rowVals[i])
                newcol += 1
    newbook.save(os.path.join(BASE_DIR, 'p3_4.xls'))

# fileload(p2Path, frnPath)
finalProcess(os.path.join(BASE_DIR, 'p3.xlsx'), firsCols=2, mod=4)

