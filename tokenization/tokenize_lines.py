import multiprocessing as mp
from multiprocessing.pool import Pool
import psutil
from functools import partial
import math
from typing import List, Callable, TextIO
import spacy.tokenizer
import argparse
from tokenization.utils import tokenize2text, get_tokenizer


def batch(iterable, n=1) -> iter:

    l: int = len(iterable)
    p: int = math.ceil(l / n)
    for ndx in range(0, l, p):
        yield iterable[ndx : min(ndx + p, l)]


def process_lines_thread(
    process_function: Callable, tokenizer: spacy.tokenizer.Tokenizer, lines: List[str]
) -> List[str]:
    try:
        return [process_function(line.strip(), tokenizer) for line in lines]
    except ValueError:
        raise


def save_thread(file, data) -> None:
    print("".join(data), file=file, end="")


def fast_tokenize_lines(
    input_path: str,
    output_path: str,
    tokenizer: spacy.tokenizer.Tokenizer,
    process_function: Callable,
    block_size: int = int(psutil.virtual_memory()[1] * 0.001),
    num_parallel: int = psutil.cpu_count(),
    skip_lines: int = 0,
) -> None:

    input_file: TextIO = open(input_path, "r", encoding="utf-8")
    output_file: TextIO = open(output_path, "w+", encoding="utf-8")

    if skip_lines:
        for _ in range(skip_lines):
            _ = input_file.readline()

    pool: Pool = mp.Pool(num_parallel)
    func: partial[List[str]] = partial(
        process_lines_thread, process_function, tokenizer
    )
    lines: List[str] = input_file.readlines(block_size)

    num_lines_print = 0
    num_lines = 0
    while lines:
        try:
            result: List[str] = pool.map(func, batch(lines, num_parallel))
        except ValueError:
            raise

        print(
            "".join([item for sublist in result for item in sublist]),
            file=output_file,
            end="",
        )

        num_lines += len(lines)
        num_lines_print += 1

        if num_lines_print % 100 == 0:
            print(f"Number lines processed: {num_lines}.", end="\r")

        lines = input_file.readlines(block_size)

    pool.close()
    pool.join()

    input_file.close()
    output_file.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Alignments FastAlign")
    parser.add_argument(
        "--input_path",
        type=str,
        required=True,
        help="Path to the source sentences in txt format (one per line)",
    )

    parser.add_argument(
        "--output_path",
        type=str,
        required=True,
        help="Path to the source sentences in txt format (one per line)",
    )

    parser.add_argument(
        "--language",
        type=str,
        required=True,
        choices=[
            "en",
            "es",
            "de",
            "it",
            "nl",
            "cat",
            "ca",
            "ned",
            "eu",
            "fr",
            "ru",
            "trk",
        ],
        help="Text language",
    )

    args = parser.parse_args()

    tokenizer = get_tokenizer(language=args.language)

    fast_tokenize_lines(
        input_path=args.input_path,
        output_path=args.output_path,
        tokenizer=tokenizer,
        process_function=tokenize2text,
    )
