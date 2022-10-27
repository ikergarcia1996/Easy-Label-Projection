# AWESOME: Aligning Word Embedding Spaces of Multilingual Encoders
This project contains python wrappers to easily generate word alignments using AWESoME. 

* Paper: https://arxiv.org/abs/2101.08231
* Official GitHub: https://github.com/neulab/awesome-align

## Batch size and hyperparameters
We use the default hyperparameters. We use a batch size of 2 with 4 gradient accumulation steps. It works well on a 24GB GPU. 
If you have a GPU with >32GB of memory, you can set a batch size of 8 with 1 gradient accumulation step for faster training.
If you get OOM errors, set batch size to 1 with 8 gradient accumulation steps. To do that, edit lines 11-12 in [model_utils.py](model_utils.py). You can also modify other hyperparameters in this file. 

## Installation
See the official repository for installation instructions: https://github.com/neulab/awesome-align#dependencies
> Note: Newest versions of Nvidia Apex library (for fp16 training) cause errors with AWESOME. As a quick workaround 
> you can download Apex from github [https://github.com/NVIDIA/apex](https://github.com/NVIDIA/apex) then go to 
> apex/amp/utils.py and and comment/remove lines 95-99. Then install Apex as usual (pip install -v --disable-pip-version-check --no-cache-dir --global-option="--cpp_ext" --global-option="--cuda_ext" ./). This workaround is not ideal,
> but I have successfully used it. The other option is uninstalling Apex and use native PyTorch AMP (you just need to have pytorch 1.6 or higher installed).

In short, you can install AWESOME using the following commands:
```commandline
git clone https://github.com/neulab/awesome-align.git
cd awesome-align
pip install -r requirements.txt
python setup.py install
```

You are ready to go when the following command produce the expected output:
````commandline
awesome-align -h
````
Expected output:
````commandline
usage: awesome-align [-h] --data_file DATA_FILE --output_file OUTPUT_FILE [--align_layer ALIGN_LAYER] [--extraction EXTRACTION] [--softmax_threshold SOFTMAX_THRESHOLD]
                     [--output_prob_file OUTPUT_PROB_FILE] [--output_word_file OUTPUT_WORD_FILE] [--model_name_or_path MODEL_NAME_OR_PATH] [--config_name CONFIG_NAME]
                     [--tokenizer_name TOKENIZER_NAME] [--seed SEED] [--batch_size BATCH_SIZE] [--cache_dir CACHE_DIR] [--no_cuda] [--num_workers NUM_WORKERS]

optional arguments:
  -h, --help            show this help message and exit
  --data_file DATA_FILE
                        The input data file (a text file).
  --output_file OUTPUT_FILE
                        The output file.
  --align_layer ALIGN_LAYER
                        layer for alignment extraction
  --extraction EXTRACTION
                        softmax or entmax15
  --softmax_threshold SOFTMAX_THRESHOLD
  --output_prob_file OUTPUT_PROB_FILE
                        The output probability file.
  --output_word_file OUTPUT_WORD_FILE
                        The output word file.
  --model_name_or_path MODEL_NAME_OR_PATH
                        The model checkpoint for weights initialization. Leave None if you want to train a model from scratch.
  --config_name CONFIG_NAME
                        Optional pretrained config name or path if not the same as model_name_or_path. If both are None, initialize a new config.
  --tokenizer_name TOKENIZER_NAME
                        Optional pretrained tokenizer name or path if not the same as model_name_or_path. If both are None, initialize a new tokenizer.
  --seed SEED           random seed for initialization
  --batch_size BATCH_SIZE
  --cache_dir CACHE_DIR
                        Optional directory to store the pre-trained models downloaded from s3 (instead of the default one)
  --no_cuda             Avoid using CUDA when available
  --num_workers NUM_WORKERS
                        Number of workers for data loading
````
