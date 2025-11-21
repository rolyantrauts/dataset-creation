#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import argparse
import glob
import os
import random
import soundfile as sf
import uuid
#import shortuuid
import sox

def trim(source_dir='./in', dest_dir='./out', start_length=1.0, end_length=1.0, min_pass_len=0.2, silence_percentage=0.05, tries=4, increment=2, min_silence_duration=0.05, fade_len=0.2):

  if not os.path.exists(dest_dir):
    os.makedirs(dest_dir)
  if not os.path.exists(source_dir):
    print("Source_dir = " + source_dir + " does not exist!")
    exit()

  logging.getLogger('sox').setLevel(logging.ERROR)
  faults = open(dest_dir + '/faults.txt', 'w')
  faults.write("start_length=" + str(start_length) + "\n")
  faults.write("end_length=" + str(end_length) + "\n")
  faults.write("min_pass_len=" + str(min_pass_len) + "\n")
  faults.write("silence_percentage=" + str(silence_percentage) + "\n")
  faults.write("tries=" + str(tries) + "\n")
  faults.write("increment=" + str(increment) + "\n")
  faults.write("min_silence_duration=" + str(min_silence_duration) + "\n")
  faults.write("fade_len=" + str(fade_len) + "\n")
  sample_rate = 48000
  source = glob.glob(source_dir + '/**/*.wav', recursive=True)
  tfm = sox.Transformer()
  count = 0
  fail = 0
  target_length = start_length
  len_source = len(source)
  for wav in source:
    sp = silence_percentage
    t = 0
    #try t times
    while t < tries:
      tfm.clear_effects()
      tfm.rate(samplerate=sample_rate)
      tfm.norm(-0.1)
      tfm.silence(location=1, silence_threshold=sp, min_silence_duration=min_silence_duration)
      tfm.silence(location=-1, silence_threshold=sp, min_silence_duration=min_silence_duration)
      tfm.fade(fade_in_len=fade_len, fade_out_len=fade_len)
      array_out = tfm.build_array(input_filepath=wav, sample_rate_in=sample_rate)
      #Silence increments in steps so that trim is done in 1 pass
      #Incrementing over multiple passes tends to create more errors
      if len(array_out) <= sample_rate * min_pass_len:
        print(wav + " Failed! length = " + str(len(array_out) / sample_rate) + 's')
        faults.write('Len< ' + wav + " Failed! length = " + str(len(array_out) / sample_rate) + 's\n')
        fail += 1
        count += 1
        os.remove(wav)
        source.remove(wav)
        break
      if len(array_out) <= sample_rate * target_length:
        tfm.build_file(input_array=array_out, sample_rate_in=sample_rate, output_filepath=dest_dir + '/' + os.path.basename(wav))
        print(dest_dir + '/' + os.path.basename(wav) + ' Sucess! length = ' + str(len(array_out) / sample_rate) + 's')
        count += 1
        os.remove(wav)
        source.remove(wav)
        break
      else:
      #increment silence_percentage by increment factor
        sp = sp * increment
        print(sp)
        t += 1
    if t >= tries:
      print(wav + " Failed! length = " + str(len(array_out) / sample_rate) + 's')
      faults.write('Start len ' + wav + " Failed! length = " + str(len(array_out) / sample_rate) + 's\n')
      


  target_length = end_length
  for wav in source:
    sp = silence_percentage
    t = 0
    #try t times
    while t < tries:
      tfm.clear_effects()
      tfm.rate(samplerate=sample_rate)
      tfm.norm(-0.1)
      tfm.silence(location=1, silence_threshold=sp, min_silence_duration=min_silence_duration)
      tfm.silence(location=-1, silence_threshold=sp, min_silence_duration=min_silence_duration)
      tfm.fade(fade_in_len=fade_len, fade_out_len=fade_len)
      array_out = tfm.build_array(input_filepath=wav, sample_rate_in=sample_rate)
      #Silence increments in steps so that trim is done in 1 pass
      #Incrementing over multiple passes tends to create more errors
      print(sp)
      if len(array_out) <= sample_rate * target_length:
        tfm.build_file(input_array=array_out, sample_rate_in=sample_rate, output_filepath=dest_dir + '/' + os.path.basename(wav))
        print(dest_dir + '/' + os.path.basename(wav) + ' Sucess! length = ' + str(len(array_out) / sample_rate) + 's')
        os.remove(wav)
        count += 1
        break
      else:
      #increment silence_percentage by increment factor
        sp = sp * increment
        t += 1
    if t >= tries:
      print(wav + " Failed! length = " + str(len(array_out) / sample_rate) + 's')
      faults.write('End len ' + wav + " Failed! length = " + str(len(array_out) / sample_rate) + 's\n')
      count += 1
      fail += 1
          
  if count == 0:
    print("Source_dir " + source_dir + " is empty no .wav files found or are larger than target size")
  else:
    print(str(fail) + " failed out of " + str(len_source))


    
    
def main_body():
  parser = argparse.ArgumentParser()
  parser.add_argument('--source_dir', default='./in', help='source dir location default=./in')
  parser.add_argument('--dest_dir', type=str, default='./out', help='dest dir location default=./out')
  parser.add_argument('--start_length', type=float, default=1.0, help='Minimum trimmed length default=1.0s')
  parser.add_argument('--end_length', type=float, default=1.0, help='Max trimmed length default=1.0s')
  parser.add_argument('--silence_percentage', type=float, default=0.05, help='Start trim level silence percentage default=0.05')
  parser.add_argument('--tries', type=int, default=4, help='The number of tries to trim incrementing silence_percentage by the increment factor')
  parser.add_argument('--increment', type=int, default=2, help='The increment factor for each try default=2')
  parser.add_argument('--min_silence_duration', type=float, default=0.1, help='min silence duration default=0.1s')
  parser.add_argument('--fade_len', type=float, default=0.05, help='fade in & out length default=0.05s')
  parser.add_argument('--min_pass_len', type=float, default=0.2, help='min length before fail default=0.2s')
  args = parser.parse_args()

  if args.dest_dir == None:
    args.dest_dir = "./out"
  
  trim(args.source_dir, args.dest_dir, args.start_length, args.end_length, args.min_pass_len, args.silence_percentage, args.tries, args.increment, args.min_silence_duration, args.fade_len)

    
if __name__ == '__main__':
  main_body()







