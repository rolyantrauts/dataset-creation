
```
mkdir gkws
cd gkws
git clone https://github.com/google-research/google-research.git
cd google-research
git checkout fa08dcc009c73c516400dc32e13147b14196becc
cd ..
mv google-research/kws_streaming .
KWS_PATH=$PWD
mkdir data2
DATA_PATH=$KWS_PATH/data2
mkdir $KWS_PATH/models2
MODELS_PATH=$KWS_PATH/models2
CMD_TRAIN="python -m kws_streaming.train.model_train_eval"
brew install graphviz
```

```
python3 -m venv --system-site-packages ./venv
source ./venv/bin/activate
pip3 install --upgrade pip
pip install tensorflow-macos==2.11.0 numpy==1.26.4 tensorflow_addons tensorflow_model_optimization pydot graphviz absl-py sounddevice scipy
```
### create crnn-state file  
modify `wanted-words` to dataset and place dataset in data2
```
$CMD_TRAIN \
--data_url '' \
--data_dir $DATA_PATH/ \
--train_dir $MODELS_PATH/crnn_state/ \
--split_data 0 \
--wanted_words kw,likekw,notkw,noise \
--mel_upper_edge_hertz 7600 \
--how_many_training_steps 20000,20000,20000,20000 \
--learning_rate 0.001,0.0005,0.0001,0.00002 \
--window_size_ms 40.0 \
--window_stride_ms 20.0 \
--mel_num_bins 40 \
--dct_num_features 20 \
--resample 0.0 \
--alsologtostderr \
--train 1 \
--lr_schedule 'exp' \
--use_spec_augment 1 \
--time_masks_number 2 \
--time_mask_max_size 10 \
--frequency_masks_number 2 \
--frequency_mask_max_size 5 \
--feature_type 'mfcc_op' \
--fft_magnitude_squared 1 \
--return_softmax 1 \
crnn \
--cnn_filters '16,16' \
--cnn_kernel_size '(3,3),(5,3)' \
--cnn_act "'relu','relu'" \
--cnn_dilation_rate '(1,1),(1,1)' \
--cnn_strides '(1,1),(1,1)' \
--gru_units 256 \
--return_sequences 0 \
--dropout1 0.1 \
--units1 '128,256' \
--act1 "'linear','relu'" \
--stateful 1
```
`nano crnn_state` paste the above with class label modifications and add a empty folder `_background_noise_` to data2  
`source crnn_state` or on macOS as source doesn't seem to work "python -m kws_streaming.train.model_train_eval --data_url "" --data_dir "$DATA_PATH/" --train_dir "$MODELS_PATH/crnn_state/" --split_data 0 --wanted_words "hey,hey-jarvis,jarvis,like-hey-jarvis,unk1,unk2,unk3,noise" --mel_upper_edge_hertz 7600 --how_many_training_steps 20000,20000,20000,20000 --learning_rate 0.001,0.0005,0.0001,0.00002 --window_size_ms 40.0 --window_stride_ms 20.0 --mel_num_bins 40 --dct_num_features 20 --resample 0.0 --alsologtostderr --train 1 --lr_schedule 'exp' --use_spec_augment 1 --time_masks_number 2 --time_mask_max_size 10 --frequency_masks_number 2 --frequency_mask_max_size 5 --feature_type 'mfcc_op' --fft_magnitude_squared 1 --return_softmax 1  crnn --cnn_filters '16,16' --cnn_kernel_size '(3,3),(5,3)' --cnn_act "'relu','relu'" --cnn_dilation_rate '(1,1),(1,1)' --cnn_strides '(1,1),(1,1)' --gru_units 256 --return_sequences 0 --dropout1 0.1 --units1 '128,256' --act1 "'linear','relu'" --stateful 1"
