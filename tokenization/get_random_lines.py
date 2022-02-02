from tokenization.utils import count_lines
import random
import math
import argparse


def get_random_lines_parallel_corpus(
    source_file_path: str,
    target_file_path: str,
    source_output_path: str,
    target_output_path: str,
    skip_lines: int = 0,
    number_of_lines: int = 50000,
):

    assert (
        number_of_lines > 0
    ), f"Number_of_lines should be greater than 0. number_of_lines: {number_of_lines}"

    num_lines_source = count_lines(source_file_path)
    num_lines_target = count_lines(target_file_path)

    assert num_lines_source == num_lines_target, (
        f"Source and target files should have the same number of lines. "
        f"{source_file_path}: {num_lines_source} lines. "
        f"{target_file_path}: {num_lines_target} lines."
    )

    random_lines_ids = list(range(skip_lines, num_lines_source))
    random.shuffle(random_lines_ids)
    random_lines_ids = set(random_lines_ids[:number_of_lines])

    with open(source_file_path, "r", encoding="utf8") as source_input, open(
        target_file_path, "r", encoding="utf8"
    ) as target_input, open(
        source_output_path, "w+", encoding="utf8"
    ) as source_output, open(
        target_output_path, "w+", encoding="utf8"
    ) as target_output:

        line_no: int = 0
        filtered_sentences: int = 0
        for source_line, target_line in zip(source_input, target_input):
            source_line: str
            target_line: str
            if line_no in random_lines_ids:

                source_line, target_line = (
                    source_line.rstrip().strip(),
                    target_line.rstrip().strip(),
                )

                # Some sentences in europarl start with a dot, remove it.
                while source_line.startswith("."):
                    source_line = source_line[1:]
                while target_line.startswith("."):
                    target_line = target_line[1:]

                source_line, target_line = (
                    source_line.strip(),
                    target_line.strip(),
                )

                if source_line != "" and target_line != "":
                    print(source_line, file=source_output)
                    print(target_line, file=target_output)

                else:
                    filtered_sentences += 1

            line_no += 1

        print(
            f"Total lines in the output file: {len(random_lines_ids)}. Filtered lines: {filtered_sentences}"
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Alignments FastAlign")
    parser.add_argument(
        "--source_file_path",
        type=str,
        required=True,
        help="Paths to the source sentences in txt format (one per line)",
    )

    parser.add_argument(
        "--target_file_path",
        type=str,
        required=True,
        help="Paths to the target sentences in txt format (one per line)",
    )

    parser.add_argument(
        "--source_output_path",
        type=str,
        required=True,
        help="Path where the random source lines will be written",
    )

    parser.add_argument(
        "--target_output_path",
        type=str,
        required=True,
        help="Path where the random target lines will be written",
    )

    parser.add_argument(
        "--skip_lines",
        type=str,
        default=0,
        help="Number of lines to skip at the beginning of the file",
    )

    parser.add_argument(
        "--number_of_lines",
        type=float,
        required=True,
        help="Number of lines that we will get",
    )

    args = parser.parse_args()

    get_random_lines_parallel_corpus(
        source_file_path=args.source_file_path,
        target_file_path=args.target_file_path,
        source_output_path=args.source_output_path,
        target_output_path=args.target_output_path,
        skip_lines=args.skip_lines,
        number_of_lines=args.number_of_lines,
    )
