
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
