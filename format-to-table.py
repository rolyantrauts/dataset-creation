#!/usr/bin/env python3
# -*- coding: utf-8 -*-

Orig = open('cmudict.rep', 'r')
Syllable = open('syllable.csv', 'w')
Syllable.write('scount,word,s1,s2,s3,s4,s5,s6,s7\n')
while True:
  Line = Orig.readline()
  if not Line:
    break
  Dup = 0
  X = Line.find("(2)")
  if X != -1:
    Dup += 1
  X = Line.find("(3)")
  if X != -1:
    Dup += 1
  X = Line.find("(4)")
  if X != -1:
    Dup += 1
  X = Line.find("(5)")
  if X != -1:
    Dup += 1
  X = Line.find("(6)")  
  if X != -1:
    Dup += 1
  X = Line.find("(7)")
  if X != -1:
    Dup += 1
  X = Line.find("(8)")
  if X != -1:
    Dup += 1
  X = Line.find("(9)")
  if X != -1:
    Dup += 1
  X = Line.find("'S")
  if X != -1:
    Dup += 1
  if Dup == 0:
    Line = Line.replace('  ', ' ')
    Word = []
    Lines = Line.split(' ')
    count = 0
    Sylls = ''
    SyllCount = 0
    for Syll in Lines:
      if count == 0:
        Word.append(Syll.strip())
      else:
        if Syll != '-':
          Sylls = Sylls + Syll.strip() + ' '
        else:
          Word.append(Sylls.strip())
          Sylls = ''
          SyllCount += 1     
      count += 1
      if count == len(Lines):
         Word.append(Sylls.strip())
         Sylls = ' '
         SyllCount += 1
         
    
    print(Word)
    Sylls = '' 
    for Syll in Word:
      Sylls = Sylls + Syll + ","
    Sylls = str(SyllCount) + ',' + Sylls
    Syllable.write(Sylls + '\n')