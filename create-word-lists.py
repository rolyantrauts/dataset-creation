import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--csv', default='./word-list.csv', help='Word list without extention')
parser.add_argument('--qty', type=int, help='Total qty needed')
args = parser.parse_args()
  
words = open(args.csv + '.csv', 'r')
cc = open(args.csv + '-cc.txt', 'w')
emot = open(args.csv + '-emot.txt', 'w')
pi = open(args.csv + '-pi.txt', 'w')

emot_count = 4.1666
pi_count = 8.9218


emot_last = 0
pi_last = 0

count = 0
while True:
  word = words.readline()
  if count == args.qty:
      break
  if not word:
    words = open(args.csv + '.csv', 'r')
    word = words.readline()
  word = word.replace(',', ' ').strip()      
  if int(count / emot_count) > emot_last:
      emot_last = count / emot_count
      emot.write(word + '\n')
      print("emot")
  elif  int(count / pi_count) > pi_last:
      pi_last = count / pi_count
      pi.write(word + '\n')
      print("pi")
  else:
      cc.write(word + '\n')         
      print("cc")
  count += 1          
