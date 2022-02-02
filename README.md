Cross-lingual Annotation Projection 

# Parameters

### Source datasets:
Source datasets in TSV format (see sample/en.absa.test.tsv for an example). 
The three splits are optional, but you must provide at least one.
````commandline
--source_train
--source_dev
--source_test
````

### Target datasets:
Target sentences in txt formar, one per line (see sample/en2es.absa.test.txt for an example).
The splits should be parallel (translations) to the corresponding one in the source split and in the same order. 
The splits should contain the same number of sentences that the corresponding source split. 
The splits are optional, but if you provide a source dataset, you must provide a corresponding target dataset.
````commandline
--target_train
--target_dev
--target_test
````

### Output directory:
The output directory where the alignments (talp file) and projections (tsv file) will be saved.
The name of the files that will be created. 
The output files will have the path: {output_dir}/{output_name}.{alignment_method}.{data_split}.[talp|tsv]
````commandline
--output_dir
--output_name
````

### Alignment method:
The alignment methods to use. The alignment method should be correctly installed/compiled to be used. 
See the README.md file inside the alignment method directory for more info about installation.
If the flag is provided, we will generate the alignments and projections for the corresponding alignment method.
You can provide multiple alignment methods, at least one of them must be provided.
If you want to modify the parameters of the alignment method, you should modify the
"model_utils.py" file inside each alignment method directory.
````commandline
--do_mgiza
--do_fastalign
--do_simalign
--do_awesome
````
If you use AWESoME you can provide to additional flags. "remove_awesome_model" will delete the trained 
AWESoME model from the output directory after the alignments are generated. You can also provide the "awesome_model_path"
flag to specify the path to a pretrained AWESoME model, we will use this models instead of training a new one.
````commandline
--remove_awesome_model
--awesome_model_path
````

### Data Augmentation:
Your dataset may be too small to be used for training the alignment method. You can 
provide an extra parallel corpus as data augmentation for training the alignment method. We will
use both, the provided tain/dev/test splits together with the augmented corpus to train the alignments.
The augmentation corpus consist of two txt files (a sentence per line), the source data augmentation dataset
should be in the same language of the source dataset. The target data augmentation dataset should be in the same
language of the target dataset. Both datasets should have the same number of sentences. Se sample/en.txt and 
sample/es.txt for an example.

````commandline
--source_augmentation
--target_augmentation
````



# Sample Projection
This is a sample projection run to test the system.
````commandline
python3 annotation_projection.py \
--source_test sample/en.absa.test.tsv \
--target_test sample/en2es.absa.test.txt \
--source_augmentation sample/en.txt \
--target_augmentation sample/es.txt \
--output_dir sample/output/ \
--output_name en2es_absa_test \
--do_simalign 
````
