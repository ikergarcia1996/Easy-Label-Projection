import os
from fast_align.generate_alignments import generate_word_alignments_fast_align
from mgiza.generate_alignments import generate_word_alignments_mgiza
from SimAlign.generate_alignments import generate_word_alignments_simalign
from awesome.generate_alignments import generate_word_alignments_awesome
from typing import Optional, List
from tokenization.utils import count_lines
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
    awesome_model_path: str = None,
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
    :param str awesome_model_path: Path to a pretrained awesome model.
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

    if source_train:
        lines_source = count_lines(input_path=source_train)
        lines_target = count_lines(input_path=target_train)
        assert lines_source == lines_target, (
            f"The number of lines in the source and target files are different.\n"
            f"Source ({source_train}): {lines_source}\n"
            f"Target ({target_train}): {lines_target}"
        )

    if source_dev:
        lines_source = count_lines(input_path=source_dev)
        lines_target = count_lines(input_path=target_dev)
        assert lines_source == lines_target, (
            f"The number of lines in the source and target files are different.\n"
            f"Source ({source_dev}): {lines_source}\n"
            f"Target ({target_dev}): {lines_target}"
        )

    if source_test:
        lines_source = count_lines(input_path=source_test)
        lines_target = count_lines(input_path=target_test)
        assert lines_source == lines_target, (
            f"The number of lines in the source and target files are different.\n"
            f"Source ({source_test}): {lines_source}\n"
            f"Target ({target_test}): {lines_target}"
        )

    if source_augmentation:
        lines_source = count_lines(input_path=source_augmentation)
        lines_target = count_lines(input_path=target_augmentation)
        assert lines_source == lines_target, (
            f"The number of lines in the source and target files are different.\n"
            f"Source ({source_augmentation}): {lines_source}\n"
            f"Target ({target_augmentation}): {lines_target}"
        )

    os.makedirs(os.path.abspath(output_dir), exist_ok=True)

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
            remove_tmp_dir=False if awesome_model_path else remove_awesome_model,
            tmp_dir=awesome_model_path,
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate alignments for a given dataset."
    )
    parser.add_argument(
        "--source_train",
        default=None,
        type=str,
        help="Path to the source training file. A txt file with one sentence per line",
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
        help="Path to the source development file. A txt file with one sentence per line",
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
        help="Path to the source test file. A txt file with one sentence per line",
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
        "--awesome_model_path",
        default=None,
        type=str,
        help="If provided, the path to a pretrained awesome model",
    )

    args = parser.parse_args()

    generate_alignments(
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
        awesome_model_path=args.awesome_model_path,
    )
