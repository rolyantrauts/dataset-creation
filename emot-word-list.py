import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--txt', default='./word-list.txt', help='Word list without extention')
args = parser.parse_args()

words = open(args.txt + '.txt', 'r')
#if os.path.exists(args.txt) == False:
#    os.mkdir(args.txt)

Males = open('Voices-Male.csv', 'r')
Females = open('Voices-Female.csv', 'r')
TTS = open('data/my_text_for_tts.txt', 'w')
Emot=['|Happy|','|Sad|','|Surprised|','|Angry']

Count = 0
while True:
  text = words.readline().strip() 
  if not text:
    print('Not Text Voices')
    quit()
  text = text + '|word\n'
  MaleVoice = Males.readline()
  FemaleVoice = Females.readline()
  if not MaleVoice:
    Males = open('Voices-Male.csv', 'r')
    MaleVoice = Males.readline()
  if not FemaleVoice:
    Females = open('Voices-Female.csv', 'r')
    FemaleVoice = Females.readline()
  Count += 1          
  print(MaleVoice.split(",")[0], FemaleVoice.split(",")[0])
  TTS.write(MaleVoice.split(",")[0] + Emot[0] + text)
  text = words.readline().strip() 
  if not text:
    print('Not Text Voices')
    quit()
  text = text + '|word\n'  
  TTS.write(FemaleVoice.split(",")[0] + Emot[0] + text)
  text = words.readline().strip() 
  if not text:
    print('Not Text Voices')
    quit()
  text = text + '|word\n'
  TTS.write(MaleVoice.split(",")[0] + Emot[1] + text) 
  text = words.readline().strip() 
  if not text:
    print('Not Text Voices')
    quit()
  text = text + '|word\n' 
  TTS.write(FemaleVoice.split(",")[0] + Emot[1] + text)       

print(Count)