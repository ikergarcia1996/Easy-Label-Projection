from awesome.utils import data2awesome, count_lines, run_bash_command
from awesome.model_utils import train_awesome, inference_awesome
import os
import argparse
from typing import List
import shutil
import uuid


def generate_word_alignments_awesome(
    source_paths: List[str],
    target_paths: List[str],
    output_dir: str,
    output_names: List[str],
    source_parallel_corpus: List[str] = None,
    target_parallel_corpus: List[str] = None,
    tmp_dir: str = None,
    remove_tmp_dir: bool = True,
):

    train_model = False
    if tmp_dir is None:
        train_model = True
        tmp_dir = f"awesome_model_{str(uuid.uuid4().hex)}"
    else:
        remove_tmp_dir = False
        print(
            f"You provided a pretrained awesome model {tmp_dir} and the remove_tmp_dir flag is set to True. "
            f"To avoid removing the model by mistake, we will set the flag to False."
        )

    assert (
        len(source_paths) == len(target_paths) == len(output_names)
        and len(source_paths) > 0
    ), f"Number of source paths and target paths should be the same"
    assert (not source_parallel_corpus and not target_parallel_corpus) or (
        len(source_parallel_corpus) == len(target_parallel_corpus)
    ), f"Number of extra source paths and target paths should be the same"

    if not os.path.exists(os.path.dirname(output_dir)):
        os.makedirs(os.path.dirname(output_dir))

    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)

    for source_path, target_path in zip(source_paths, target_paths):
        source_lines: int = count_lines(source_path)
        target_lines: int = count_lines(target_path)
        assert source_lines == target_lines, (
            f"Number of lines in {source_path}: {source_lines}. "
            f"Number of lines in {target_path}: {target_lines}. "
        )

    for source_path, target_path in zip(source_parallel_corpus, target_parallel_corpus):
        source_lines: int = count_lines(source_path)
        target_lines: int = count_lines(target_path)
        assert source_lines == target_lines, (
            f"Number of lines in {source_path}: {source_lines}. "
            f"Number of lines in {target_path}: {target_lines}. "
        )
    if train_model:
        source_train_path: str = os.path.join(tmp_dir, "source_sentences.txt")
        target_train_path: str = os.path.join(tmp_dir, "target_sentences.txt")

        command: str = (
            f"cat {' '.join(source_paths)} "
            f"{'' if not source_parallel_corpus else ' '.join(source_parallel_corpus)} "
            f"> {source_train_path}"
        )
        run_bash_command(command)
        command: str = (
            f"cat {' '.join(target_paths)} "
            f"{'' if not target_parallel_corpus else ' '.join(target_parallel_corpus)} "
            f"> {target_train_path}"
        )
        run_bash_command(command)

        print("Data 2 awesome format...")
        data2awesome(
            source_path=source_train_path,
            target_path=target_train_path,
            output_path=os.path.join(tmp_dir, "dataset.awesome"),
        )

        print("Train awesome...")

        train_awesome(
            corpus_path=os.path.join(tmp_dir, "dataset.awesome"), output_dir=tmp_dir
        )

    for source_set_path, target_set_path, output_name in zip(
        source_paths, target_paths, output_names
    ):
        print(
            f"Awesome inference: {source_set_path}-{target_set_path} => {output_name}"
        )

        data2awesome(
            source_path=source_set_path,
            target_path=target_set_path,
            output_path=os.path.join(tmp_dir, f"{output_name}.awesome"),
        )

        inference_awesome(
            corpus_path=os.path.join(tmp_dir, f"{output_name}.awesome"),
            output_path=os.path.join(output_dir, output_name),
            model_name_or_path=tmp_dir,
        )

    if remove_tmp_dir:
        shutil.rmtree(tmp_dir, ignore_errors=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Alignments FastAlign")
    parser.add_argument(
        "--source_paths",
        type=str,
        required=True,
        nargs="+",
        help="Paths to the source sentences in txt format (one per line)",
    )

    parser.add_argument(
        "--target_paths",
        type=str,
        required=True,
        nargs="+",
        help="Paths to the target sentences in txt format (one per line)",
    )

    parser.add_argument(
        "--output_names",
        type=str,
        required=True,
        nargs="+",
        help="Names to the output files that we will store in the output_dir",
    )

    parser.add_argument(
        "--output_dir",
        type=str,
        required=True,
        help="Path to were the alignment file is going to be stored",
    )

    parser.add_argument(
        "--source_parallel_corpus",
        type=str,
        required=False,
        nargs="+",
        help="Paths to the dataset augmentation corpus source sentences (one per line)",
    )

    parser.add_argument(
        "--target_parallel_corpus",
        type=str,
        required=False,
        nargs="+",
        help="Paths to the dataset augmentation corpus target sentences (one per line)",
    )

    args = parser.parse_args()

    generate_word_alignments_awesome(
        source_paths=args.source_paths,
        target_paths=args.target_paths,
        source_parallel_corpus=args.source_parallel_corpus,
        target_parallel_corpus=args.target_parallel_corpus,
        output_names=args.output_names,
        output_dir=args.output_dir,
    )
