# AWESOME: Aligning Word Embedding Spaces of Multilingual Encoders
This project contains python wrappers to easily generate word alignments using AWESoME. 

* Paper: https://arxiv.org/abs/2101.08231
* Official GitHub: https://github.com/neulab/awesome-align

## Installation
See the official repository for installation instructions: https://github.com/neulab/awesome-align#dependencies

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