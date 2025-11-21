# dataset-creation
wakeword dataset creation scripts

Suggested benchmark model
https://github.com/Qualcomm-AI-research/bcresnet  
[Opensource Licence
](https://github.com/Qualcomm-AI-research/bcresnet#BSD-3-Clause-Clear-1-ov-file)

 [The repo folder](https://github.com/rolyantrauts/dataset-creation/tree/main/bcresnet) has hacked out the Google command so that any class collection can be used if provided in a data/train data/valid /data/test folder structure  
 Make edits if CUDA, current is MPS (Apple)  

 Example dataset here 

https://drive.google.com/file/d/1Uhe4Xjtas-ytIZgtGEXfK5qDo8CFcfXw/view?usp=sharing

# Install TTS from
https://github.com/idiap/coqui-ai-TTS
```
pip install coqui-tts[languages]
```
https://github.com/netease-youdao/EmotiVoice

[sherpa onnx
](https://github.com/k2-fsa/sherpa-onnx)
```
pip install sherpa-onnx sherpa-onnx-bin
```

Create SQLite views to represent your wakeword dataset, open `words.db` with SQLite Browser create your own and just export as a .CSV table.  
`create-word-lists.py` will create the number required likely the largest view and split the list to 3 TTS so you maximise prosody and variation. `create-word-lists.py` will create a apportioned piper list based on total voices   
Say for piper onnx clone the repo, do the `pip install` and then run `piper-word-list.py` after downloading the model as described in https://k2-fsa.github.io/sherpa/onnx/tts/pretrained_models/vits.html#vits-piper-en-us-libritts-r-medium-english-904-speakers  
I am not sure why this seems to provide better quality with more variation than the models the actual piper repo's provide and prob does exist in the piper repo's somewhere...  

Coqui is just a `pip install`, as the module on 1st use will grab the correct model it uses the voice clone function with voices downloaded from https://accent.gmu.edu/howto.php  
To save time you can use this download of over 1000 male/female voices from accent.gmu.edu https://drive.google.com/file/d/1gPiz--326JJSO_1CspNt97VPW1G95jlW/view?usp=drive_link  
`coqui-list.py` on the coqui.list will create TTS output...  

Emotivoice you can just use the inbuilt tools of convert emot list to phonetics as directed in the readme https://github.com/netease-youdao/EmotiVoice/blob/main/README.md  
`python frontend.py word-list.txt > data/my_text.txt` to create 'phone.txt' and then `emot-word-list.py` will add voices to that list.  
```
TEXT=data/my_text_for_tts.txt
python inference_am_vocoder_joint.py \
--logdir prompt_tts_open_source_joint \
--config_folder config/joint \
--checkpoint g_00140000 \
--test_file $TEXT
```

After TTS creation use trim.py to remove silence as reject too long /halucinations.  
Hey example  
```
start_length=0.45
end_length=0.8
min_pass_len=0.2
silence_percentage=0.05
tries=6
increment=2
min_silence_duration=0.1
fade_len=0.05
```

If you want to create a noise class a curated list of 10sec noise files can be downloaded from here https://drive.google.com/file/d/1tY6qkLSTz3cdOnYRuBxwIM5vj-w4yTuH/view?usp=sharing

Something somewhere is not right as likely you will find after training and testing your own model its far more accurate than ones supplied.
Dataset and basic instructions have been supplied as a toy dataset with no augmentation purely as a test datum. 
