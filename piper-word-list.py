#!/usr/bin/env python3
#
# Copyright (c)  2023-2025  Xiaomi Corporation

import sherpa_onnx
import soundfile as sf
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--txt', default='./word-list.txt', help='Word list without extention')
args = parser.parse_args()

words = open(args.txt + '.txt', 'r')
if os.path.exists(args.txt) == False:
    os.mkdir(args.txt)

def main():
    text='Hey jarvis'
    sid=0
    
    tts_config = sherpa_onnx.OfflineTtsConfig(
        model=sherpa_onnx.OfflineTtsModelConfig(
            vits=sherpa_onnx.OfflineTtsVitsModelConfig(
                model='./vits-piper-en_US-libritts_r-medium/en_US-libritts_r-medium.onnx',
                data_dir='./vits-piper-en_US-libritts_r-medium/espeak-ng-data',
                tokens='./vits-piper-en_US-libritts_r-medium/tokens.txt',
            ),
            provider='cpu',
            debug=False,
            num_threads=4,
        ),
        max_num_sentences=1,
    )
    if not tts_config.validate():
        raise ValueError("Please check your config")

    tts = sherpa_onnx.OfflineTts(tts_config)
    count = 0
    while True:
        count += 1
        for sid in range(903):
            text = words.readline().strip()
            if not text:
                print('Not Text Voices')
                quit()            
            audio = tts.generate(text, sid, speed=0.9)

            if len(audio.samples) == 0:
                print("Error in generating audios. Please read previous error messages.")
                return

            audio_duration = len(audio.samples) / audio.sample_rate

            output_filename=args.txt + '/' + str(count) + '-' + text + '-9-' + str(sid) + '.wav'
            sf.write(
                output_filename,
                audio.samples,
                samplerate=audio.sample_rate,
                subtype="PCM_16",
            )
            print(f"Saved to {output_filename}")

            text = words.readline().strip()
            if not text:
                print('Not Text Voices')
                quit()            
            audio = tts.generate(text, sid, speed=1.0)

            if len(audio.samples) == 0:
                print("Error in generating audios. Please read previous error messages.")
                return

            audio_duration = len(audio.samples) / audio.sample_rate

            output_filename=args.txt + '/' + str(count) + '-' + text + '-1-' + str(sid) + '.wav'
            sf.write(
                output_filename,
                audio.samples,
                samplerate=audio.sample_rate,
                subtype="PCM_16",
            )        
            print(f"Saved to {output_filename}")


if __name__ == "__main__":
    main()
