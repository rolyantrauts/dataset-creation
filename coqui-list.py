import torch
import time
import os
from TTS.api import TTS
import argparse
import random

parser = argparse.ArgumentParser()
parser.add_argument('--txt', default='./word-list.txt', help='Word list without extention')
args = parser.parse_args()

words = open(args.txt + '.txt', 'r')
if os.path.exists(args.txt) == False:
    os.mkdir(args.txt)
    
# Get device
device = "mps" if torch.backends.mps.is_available() else "cpu"
#device ="cpu"

# Initialize TTS
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

path = os. getcwd() + "//voices"
dir_list = os.listdir(path)
random.shuffle(dir_list)
languages = tts.languages
random.shuffle(languages)
speakers = tts.speakers
random.shuffle(speakers)

count = 0
qty = 0
while True:
    count += 1

    for file in dir_list:
        for lang in languages:
            if lang != "ko" and lang != "hi":
                text = words.readline().strip()
                if not text:
                    print('Not Text Voices')
                    quit()
                qty += 1
                print(qty)
                file_path = args.txt + "/" + str(count) + '-' + text.replace(' ', '-') + '-' + os.path.basename(file).split('.')[0].replace(' ', '-') + "-" + lang + ".wav"
                tts.tts_to_file(
                    text=text,
                    speaker_wav=path + "//" + file,
                    language=lang,
                    file_path= file_path
                )
       
    for lang in languages:
        for speaker in speakers:
            if lang != "ko" and lang != "hi":
                text = words.readline().strip()
                if not text:
                    print('Not Text Speakers')
                    quit()
                qty += 1
                print(qty)
                tts.tts_to_file(
                    text=text,
                    speaker=speaker,
                    language=lang,
                    file_path= args.txt + "/" + str(count) + '-' + text.replace(' ', '-') + '-' + speaker.replace(' ', '-') + "-" + lang + ".wav"
                )