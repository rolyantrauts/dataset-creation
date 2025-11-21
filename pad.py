#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import argparse
import glob
import os, operator, sys
import random
import soundfile as sf
import uuid
import sox
import math
import shortuuid
import numpy as np

def augment(target_qty, target_length, min_vol, debug, source_dir, dest_dir, ):

  if debug == 0:  
    logging.getLogger('sox').setLevel(logging.ERROR)
  else:
    logging.getLogger('sox').setLevel(logging.DEBUG)
    
  if not os.path.exists(source_dir):
    print("Source_dir = " + source_dir + " does not exist!")
    exit()
      
  sample_rate = 16000
  #print(source_dir)
  source_samples = glob.glob(os.path.join(source_dir, '*.wav'))
  source_qty = len(source_samples)  
  sample_qty = math.ceil(target_qty / source_qty)
  print(sample_qty)
  #exit()
  if source_qty < 1:
    print("No noise files found *.wav")
    exit()
  if not os.path.exists(dest_dir):
    print("dest dir is missing")
    exit()
  
  qty = 0
  count = 0
  
  while qty < sample_qty:
    for source_wav in source_samples:
        augment_wav(dest_dir, sample_rate, target_length, qty + 1, source_wav, min_vol)
        count += 1
        if count == target_qty:
          quit()
    qty += 1
    
def augment_wav(dest_dir, sample_rate, target_length, version, source_wav, source_vol):
    
    wav_length = sox.file_info.duration(source_wav)
    source_lvl = 1.0 - ((1.0 - source_vol)  * random.random())
    
    tfm2 = sox.Transformer()
    tfm2.clear_effects()
    tfm2.rate(samplerate=sample_rate)
    tfm2.norm(-0.1)
    tfm2.vol(source_lvl)
    if wav_length < target_length:
      offset = target_length - wav_length
      if offset > 0.04:
        jog = 0.02 * random.random()
        #print(offset, jog)
        tfm2.pad((offset / 2) - jog, (offset / 2) + jog + 0.1)
      elif offset > 0.02:
        jog = 0.01 * random.random()
        #print(offset, jog)
        tfm2.pad((offset / 2) - jog, (offset / 2) + jog + 0.1)
      else:
        tfm2.pad(offset / 2, (offset / 2) + 0.1)   
        
    tfm2.trim(0, target_length)
    out = os.path.splitext(source_wav)[0].replace(" ", "") + '-v' + str(version) + '.wav'
    out = dest_dir + "/" + shortuuid.uuid() + "-" + os.path.basename(out)
    tfm2.build_file(source_wav, out)
    print(out)
      
    
def main_body():
  parser = argparse.ArgumentParser()
  parser.add_argument('--dest_dir', default='./dest', help='dest dir location')
  parser.add_argument('--target_qty', type=int, default=4000, help='Final qty of augmented audio files')
  parser.add_argument('--target_length', type=float, default=1.0, help='Target length of audio files to be trimmed to (s)')
  parser.add_argument('--debug', help='debug effect settings to cli', action="store_true")
  parser.add_argument('--source_dir', default='./noise', help='noise dir location')
  parser.add_argument('--min_vol', type=float, default=0.7, help='Min Vol of noise foreground (0.7)')
  args = parser.parse_args()
  
  augment(args.target_qty, args.target_length, args.min_vol, args.debug, args.source_dir, args.dest_dir,)
    
if __name__ == '__main__':
  main_body()

