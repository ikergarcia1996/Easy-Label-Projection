import os
from fast_align.generate_alignments import generate_word_alignments_fast_align
from mgiza.generate_alignments import generate_word_alignments_mgiza
from SimAlign.generate_alignments import generate_word_alignments_simalign
from awesome.generate_alignments import generate_word_alignments_awesome
from typing import Optional, List
from tokenization.conll2text import conll2text
from tokenization.utils import count_lines
from projection.annotation_proyection import dataset_projection
import argparse


def generate_alignments(
    source_train: Optional[str],
    source_dev: Optional[str],
    source_test: Optional[str],
    target_train: Optional[str],
    target_dev: Optional[str],
    target_test: Optional[str],
    source_augmentation: Optional[str],
    target_augmentation: Optional[str],
    output_dir: str,
    output_name: str,
    do_fastalign: bool = False,
    do_mgiza: bool = False,
    do_simalign: bool = True,
    do_awesome: bool = False,
    remove_awesome_model: bool = True,
    model_name_or_path: str = "bert-base-multilingual-cased",
):

    """
    Generate word alignments for the given datasets.
    :param str source_train: Path to the source language training dataset. A txt file, one sentence per line.
    :param str source_dev: Path to the source language development dataset. A txt file, one sentence per line.
    :param str source_test: Path to the source language test dataset. A txt file, one sentence per line.
    :param str target_train: Path to the target language training dataset. A txt file, one sentence per line.
    :param str target_dev: Path to the target language development dataset. A txt file, one sentence per line.
    :param str target_test: Path to the target language test dataset. A txt file, one sentence per line.
    :param str source_augmentation: Path to the source language augmentation dataset. A txt file, one sentence per line.
    :param str target_augmentation: Path to the target language augmentation dataset. A txt file, one sentence per line.
    :param str output_dir: Path to the output directory.
    :param str output_name: Name of the output files
    :param bool do_fastalign: Whether to generate word alignments with fastalign.
    :param bool do_mgiza: Whether to generate word alignments with mgiza.
    :param bool do_simalign: Whether to generate word alignments with simalign.
    :param bool do_awesome: Whether to generate word alignments with awesome.
    :param bool remove_awesome_model: Whether to remove the trained awesome model after the alignment generation.
    :param str model_name_or_path: Hugginface Hub model name or path to a local model. Used for simalign and awesome.
    """

    # 1) Sanity checks

    assert source_train or source_dev or source_test, f"Nothing to do"

    assert target_train or target_dev or target_test, f"Nothing to do"

    assert (source_train is not None and target_train is not None) or (
        source_train is None and target_train is None
    ), f"Source train: {source_train}. Target train: {target_train}"

    assert (source_dev is not None and target_dev is not None) or (
        source_dev is None and target_dev is None
    ), f"Source dev: {source_dev}. Target dev: {target_dev}"

    assert (source_test is not None and target_test is not None) or (
        source_test is None and target_test is None
    ), f"Source test: {source_test}. Target test: {target_test}"

    assert (source_augmentation is not None and target_augmentation is not None) or (
        source_augmentation is None and target_augmentation is None
    )

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Projection

    source_paths: List[str] = []
    target_paths: List[str] = []

    if source_train:
        source_paths.append(source_train)
        target_paths.append(target_train)
    if source_dev:
        source_paths.append(source_dev)
        target_paths.append(target_dev)
    if source_test:
        source_paths.append(source_test)
        target_paths.append(target_test)

    if do_mgiza:

        output_names = []
        if source_train:
            output_names.append(output_name + ".mgiza.train")
        if source_dev:
            output_names.append(output_name + ".mgiza.dev")
        if source_test:
            output_names.append(output_name + ".mgiza.test")

        print(
            f"Generate word alignments Mgiza.\n"
            f"Source paths: {source_paths}.\n"
            f"Target paths: {target_paths}.\n"
            f"source_parallel_corpus: {source_augmentation}.\n"
            f"target_parallel_corpus: {target_augmentation}.\n"
            f"Output names: {output_names}.\n"
            f"Output_dir: {output_dir}.\n"
        )

        generate_word_alignments_mgiza(
            source_paths=source_paths,
            target_paths=target_paths,
            source_parallel_corpus=[source_augmentation]
            if source_augmentation
            else None,
            target_parallel_corpus=[target_augmentation]
            if target_augmentation
            else None,
            output_names=output_names,
            output_dir=output_dir,
        )

    if do_fastalign:
        output_names = []
        if source_train:
            output_names.append(output_name + ".fast_align.train")
        if source_dev:
            output_names.append(output_name + ".fast_align.dev")
        if source_test:
            output_names.append(output_name + ".fast_align.test")

        print(
            f"Generate word alignments Fast Align.\n"
            f"Source paths: {source_paths}.\n"
            f"Target paths: {target_paths}.\n"
            f"source_parallel_corpus: {source_augmentation}.\n"
            f"target_parallel_corpus: {target_augmentation}.\n"
            f"Output names: {output_names}.\n"
            f"Output_dir: {output_dir}.\n"
        )

        generate_word_alignments_fast_align(
            source_paths=source_paths,
            target_paths=target_paths,
            source_parallel_corpus=[source_augmentation]
            if source_augmentation
            else None,
            target_parallel_corpus=[target_augmentation]
            if target_augmentation
            else None,
            output_names=output_names,
            output_dir=output_dir,
        )

    if do_simalign:
        if source_train and target_train:
            print(
                f"Generate word alignments SimAlign. "
                f"source_file: {source_train}. "
                f"target_file: {target_train}. "
                f"output: {os.path.join(output_dir, f'{output_name}.simalign.train')}"
            )

            generate_word_alignments_simalign(
                source_file=source_train,
                target_file=target_train,
                output=os.path.join(output_dir, f"{output_name}.simalign.train"),
                model=model_name_or_path,
            )

        if source_dev and target_dev:
            print(
                f"Generate word alignments SimAlign. "
                f"source_file: {source_dev}. "
                f"target_file: {target_dev}. "
                f"output: {os.path.join(output_dir, f'{output_name}.simalign.dev')}"
            )

            generate_word_alignments_simalign(
                source_file=source_dev,
                target_file=target_dev,
                output=os.path.join(output_dir, f"{output_name}.simalign.dev"),
                model=model_name_or_path,
            )

        if source_test and target_test:
            print(
                f"Generate word alignments SimAlign. "
                f"source_file: {source_test}. "
                f"target_file: {target_test}. "
                f"output: {os.path.join(output_dir, f'{output_name}.simalign.test')}"
            )

            generate_word_alignments_simalign(
                source_file=source_test,
                target_file=target_test,
                output=os.path.join(output_dir, f"{output_name}.simalign.test"),
                model=model_name_or_path,
            )

    if do_awesome:

        output_names = []
        if source_train:
            output_names.append(output_name + ".awesome.train.talp")
        if source_dev:
            output_names.append(output_name + ".awesome.dev.talp")
        if source_test:
            output_names.append(output_name + ".awesome.test.talp")

        print(
            f"Generate word alignments awesome.\n"
            f"Source paths: {source_paths}.\n"
            f"Target paths: {target_paths}.\n"
            f"source_parallel_corpus: {source_augmentation}.\n"
            f"target_parallel_corpus: {target_augmentation}.\n"
            f"Output names: {output_names}.\n"
            f"Output_dir: {output_dir}.\n"
        )

        generate_word_alignments_awesome(
            source_paths=source_paths,
            target_paths=target_paths,
            source_parallel_corpus=[source_augmentation]
            if source_augmentation
            else None,
            target_parallel_corpus=[target_augmentation]
            if target_augmentation
            else None,
            output_names=output_names,
            output_dir=output_dir,
            remove_tmp_dir=remove_awesome_model,
            model_name_or_path=model_name_or_path,
        )


def run_projection(
    source_train: Optional[str],
    source_dev: Optional[str],
    source_test: Optional[str],
    target_train: Optional[str],
    target_dev: Optional[str],
    target_test: Optional[str],
    source_augmentation: Optional[str],
    target_augmentation: Optional[str],
    output_dir: str,
    output_name: str,
    do_fastalign: bool = False,
    do_mgiza: bool = False,
    do_simalign: bool = True,
    do_awesome: bool = False,
    remove_awesome_model: bool = True,
    model_name_or_path: str = "bert-base-multilingual-cased",
    remove_puncs: bool = True,
    fill_gap_size: int = 1,
    use_existing_alignments: bool = False,
):
    """
    Perform annotation projection for the given datasets.
    :param str source_train: Path to the source language training dataset. A tsv file.
    :param str source_dev: Path to the source language development dataset. A tsv file.
    :param str source_test: Path to the source language test dataset. A tsv file.
    :param str target_train: Path to the target language training dataset. A txt file, one sentence per line.
    :param str target_dev: Path to the target language development dataset. A txt file, one sentence per line.
    :param str target_test: Path to the target language test dataset. A txt file, one sentence per line.
    :param str source_augmentation: Path to the source language augmentation dataset. A txt file, one sentence per line.
    :param str target_augmentation: Path to the target language augmentation dataset. A txt file, one sentence per line.
    :param str output_dir: Path to the output directory.
    :param str output_name: Name of the output files
    :param bool do_fastalign: Whether to generate word alignments with fastalign.
    :param bool do_mgiza: Whether to generate word alignments with mgiza.
    :param bool do_simalign: Whether to generate word alignments with simalign.
    :param bool do_awesome: Whether to generate word alignments with awesome.
    :param bool remove_awesome_model: Whether to remove the trained awesome model after the alignment generation.
    :param str model_name_or_path: Hugginface Hub model name or path to a local model. Used for simalign and awesome.
    :param bool remove_puncs: If a source word is aligned to a punctuation mark, we remove the alignment.
    Use True if you are projection named entities or labels with a small number of words.
    Use false for argumentation datasets and datasets in which the labels are long sentences.
    :param int fill_gap_size: If the projected label is split in two or more parts, we fill the gap if the gap size is
    less or equal than fill_gap_size. Else we will choose the largest label and remove the other part.
    Use True 1 if you are projection named entities or labels with a small number of words.
    Use a larger value for argumentation datasets and datasets in which the labels are long sentences.
    :param bool use_existing_alignments: Whether to use existing word alignments instead of generating new ones. You
    must use the same --output_dir and --output_name as the one used to generate the word alignments. You must
    also use the same train, dev and test files.
    """

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    assert source_train or source_dev or source_test, f"Nothing to do"

    assert target_train or target_dev or target_test, f"Nothing to do"

    assert (source_train is not None and target_train is not None) or (
        source_train is None and target_train is None
    ), f"Source train: {source_train}. Target train: {target_train}"

    assert (source_dev is not None and target_dev is not None) or (
        source_dev is None and target_dev is None
    ), f"Source dev: {source_dev}. Target dev: {target_dev}"

    assert (source_test is not None and target_test is not None) or (
        source_test is None and target_test is None
    ), f"Source test: {source_test}. Target test: {target_test}"

    assert (source_augmentation is not None and target_augmentation is not None) or (
        source_augmentation is None and target_augmentation is None
    )

    if source_train:
        source_train_txt = os.path.join(
            output_dir, os.path.basename(os.path.splitext(source_train)[0]) + ".txt"
        )
        conll2text(input_path=source_train, sentences_output_path=source_train_txt)
        lines_source = count_lines(input_path=source_train_txt)
        lines_target = count_lines(input_path=target_train)
        assert lines_source == lines_target, (
            f"The number of lines in the source and target files are different.\n"
            f"Source ({source_train_txt}): {lines_source}\n"
            f"Target ({target_train}): {lines_target}"
        )
    else:
        source_train_txt = None

    if source_dev:
        source_dev_txt = os.path.join(
            output_dir, os.path.basename(os.path.splitext(source_dev)[0]) + ".txt"
        )
        conll2text(input_path=source_dev, sentences_output_path=source_dev_txt)
        lines_source = count_lines(input_path=source_dev_txt)
        lines_target = count_lines(input_path=target_dev)
        assert lines_source == lines_target, (
            f"The number of lines in the source and target files are different.\n"
            f"Source ({source_dev_txt}): {lines_source}\n"
            f"Target ({target_dev}): {lines_target}"
        )
    else:
        source_dev_txt = None

    if source_test:
        source_test_txt = os.path.join(
            output_dir, os.path.basename(os.path.splitext(source_test)[0]) + ".txt"
        )
        conll2text(input_path=source_test, sentences_output_path=source_test_txt)
        lines_source = count_lines(input_path=source_test_txt)
        lines_target = count_lines(input_path=target_test)
        assert lines_source == lines_target, (
            f"The number of lines in the source and target files are different.\n"
            f"Source ({source_test_txt}): {lines_source}\n"
            f"Target ({target_test}): {lines_target}"
        )
    else:
        source_test_txt = None

    if source_augmentation:
        lines_source = count_lines(input_path=source_augmentation)
        lines_target = count_lines(input_path=target_augmentation)
        assert lines_source == lines_target, (
            f"The number of lines in the source and target files are different.\n"
            f"Source ({source_augmentation}): {lines_source}\n"
            f"Target ({target_augmentation}): {lines_target}"
        )

    if not use_existing_alignments:
        generate_alignments(
            source_train=source_train_txt,
            target_train=target_train,
            source_dev=source_dev_txt,
            target_dev=target_dev,
            source_test=source_test_txt,
            target_test=target_test,
            source_augmentation=source_augmentation,
            target_augmentation=target_augmentation,
            output_dir=output_dir,
            output_name=output_name,
            do_fastalign=do_fastalign,
            do_mgiza=do_mgiza,
            do_simalign=do_simalign,
            do_awesome=do_awesome,
            remove_awesome_model=remove_awesome_model,
            model_name_or_path=model_name_or_path,
        )
    else:
        print(
            f"--use_existing_alignments is set to True. We will attempt to use the existing word alignments."
        )

    alignment_list = []
    if do_mgiza:
        alignment_list.append("mgiza")
    if do_fastalign:
        alignment_list.append("fast_align")
    if do_simalign:
        alignment_list.append("simalign")
    if do_awesome:
        alignment_list.append("awesome")

    dataset_list = []
    if source_train:
        dataset_list.append("train")
    if source_dev:
        dataset_list.append("dev")
    if source_test:
        dataset_list.append("test")

    output_files: List[str] = []

    for alignment_method in alignment_list:
        for dataset_split in dataset_list:
            if alignment_method == "mgiza" or alignment_method == "fast_align":
                alignments_path = os.path.join(
                    output_dir,
                    f"{output_name}.{alignment_method}.{dataset_split}.grow_diag_final-and.talp",
                )

            elif alignment_method == "simalign":
                alignments_path = os.path.join(
                    output_dir,
                    f"{output_name}.{alignment_method}.{dataset_split}.itermax.talp",
                )

            elif alignment_method == "awesome":
                alignments_path = os.path.join(
                    output_dir,
                    f"{output_name}.{alignment_method}.{dataset_split}.talp",
                )
            else:
                raise ValueError(f"{alignment_method} not supported")

            if dataset_split == "train":
                source_dataset = source_train
                target_dataset = target_train
            elif dataset_split == "dev":
                source_dataset = source_dev
                target_dataset = target_dev
            elif dataset_split == "test":
                source_dataset = source_test
                target_dataset = target_test
            else:
                raise ValueError(f"{dataset_split} dataset split not supported")

            dataset_projection(
                source_dataset=source_dataset,
                target_sentences=target_dataset,
                alignments_path=alignments_path,
                batch_size=10000,
                output_path=os.path.join(
                    output_dir, f"{output_name}.{alignment_method}.{dataset_split}.tsv"
                ),
                remove_puncs=remove_puncs,
                fill_gap_size=fill_gap_size,
            )

            output_files.append(
                os.path.join(
                    output_dir, f"{output_name}.{alignment_method}.{dataset_split}.tsv"
                )
            )

    if source_train_txt:
        os.remove(source_train_txt)
    if source_dev_txt:
        os.remove(source_dev_txt)
    if source_test_txt:
        os.remove(source_test_txt)

    print("Done!")
    print("Output files:")
    print("\n".join(output_files))
    print("\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Perform annotation projection for a given dataset."
    )
    parser.add_argument(
        "--source_train",
        default=None,
        type=str,
        help="Path to the source training file. TSV format",
    )
    parser.add_argument(
        "--target_train",
        default=None,
        type=str,
        help="Path to the target training file. A txt file with one sentence per line",
    )
    parser.add_argument(
        "--source_dev",
        default=None,
        type=str,
        help="Path to the source development file. TSV format",
    )
    parser.add_argument(
        "--target_dev",
        default=None,
        type=str,
        help="Path to the target development file. A txt file with one sentence per line",
    )
    parser.add_argument(
        "--source_test",
        default=None,
        type=str,
        help="Path to the source test file. TSV format",
    )
    parser.add_argument(
        "--target_test",
        default=None,
        type=str,
        help="Path to the target test file. A txt file with one sentence per line",
    )
    parser.add_argument(
        "--source_augmentation",
        default=None,
        type=str,
        help="Path to the source augmentation file. A txt file with one sentence per line",
    )
    parser.add_argument(
        "--target_augmentation",
        default=None,
        type=str,
        help="Path to the target augmentation file. A txt file with one sentence per line",
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        help="Path to the output directory",
    )
    parser.add_argument(
        "--output_name",
        type=str,
        help="Name of the output file",
    )
    parser.add_argument(
        "--do_mgiza",
        action="store_true",
        help="Whether to generate alignments using mgiza",
    )
    parser.add_argument(
        "--do_fastalign",
        action="store_true",
        help="Whether to generate alignments using fast_align",
    )
    parser.add_argument(
        "--do_simalign",
        action="store_true",
        help="Whether to generate alignments using simalign",
    )
    parser.add_argument(
        "--do_awesome",
        action="store_true",
        help="Whether to generate alignments using awesome",
    )
    parser.add_argument(
        "--remove_awesome_model",
        action="store_true",
        help="Whether to remove the trained awesome model after the alignment is generated",
    )
    parser.add_argument(
        "--model_name_or_path",
        default="bert-base-multilingual-cased",
        type=str,
        help="Huggingface Hub model name or path to a local model",
    )

    parser.add_argument(
        "--do_not_remove_puncs",
        action="store_false",
        help="If a source word is aligned to a punctuation mark, we remove the alignment. "
        "Do not set this flag if you are projection named entities or labels with a small number of words. "
        "Use false for argumentation datasets and datasets in which the labels are long sentences.",
    )

    parser.add_argument(
        "--fill_gap_size",
        default=1,
        type=int,
        help="If the projected label is split in two or more parts, we fill the gap if the gap size is less or equal "
        "than fill_gap_size. Else shouldwe will choose the largest label and remove the other part. "
        "Use True 1 if you are projection named entities or labels with a small number of words. "
        "Use a larger value for argumentation datasets and datasets in which the labels are long sentences.",
    )

    parser.add_argument(
        "--use_existing_alignments",
        action="store_true",
        help="If set, the script will use the existing alignments in the output directory instead of generating "
        "new ones. You must use the same --output_dir and --output_name as the previous run and the same "
        "train, dev and test files.",
    )

    args = parser.parse_args()

    run_projection(
        source_train=args.source_train,
        target_train=args.target_train,
        source_dev=args.source_dev,
        target_dev=args.target_dev,
        source_test=args.source_test,
        target_test=args.target_test,
        source_augmentation=args.source_augmentation,
        target_augmentation=args.target_augmentation,
        output_dir=args.output_dir,
        output_name=args.output_name,
        do_mgiza=args.do_mgiza,
        do_fastalign=args.do_fastalign,
        do_simalign=args.do_simalign,
        do_awesome=args.do_awesome,
        remove_awesome_model=args.remove_awesome_model,
        model_name_or_path=args.model_name_or_path,
        remove_puncs=args.do_not_remove_puncs,
        fill_gap_size=args.fill_gap_size,
        use_existing_alignments=args.use_existing_alignments,
    )
