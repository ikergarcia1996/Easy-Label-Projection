from typing import List
import re
import subprocess


def run_bash_command(command: str) -> None:
    print(command)
    subprocess.run(["bash", "-c", command])


def count_lines(input_path: str) -> int:
    with open(input_path, "r", encoding="utf8") as f:
        return sum(1 for _ in f)


def concatenate_files(input_paths: List[str], output_path: str) -> None:
    with open(output_path, "w", encoding="utf8") as output_file:
        for input_path in input_paths:
            with open(input_path, "r", encoding="utf8") as input_file:
                for line in input_file:
                    line = line.strip().rstrip()
                    if line != "":
                        print(line, file=output_file)


def mgiza2fastalign(input_path, output_path, reverse=False):
    with open(input_path, "r", encoding="utf8") as input_file:
        with open(output_path, "w+", encoding="utf8") as output_file:
            word_format = re.compile(r"[^ ]+ \({[0-9|\s]*}\)")
            line: str = input_file.readline()
            while line:
                header: str = line
                sentence: str = input_file.readline()
                alignments: List[str] = re.findall(word_format, input_file.readline())

                fastalign_line: List[str] = []

                for source_id, alignment in enumerate(alignments):

                    try:
                        word, dictionary = alignment.strip().split(" ", 1)
                    except ValueError:
                        raise ValueError(
                            f"Error in line: {alignments}. alignment: {alignment}"
                        )
                    if word != "NULL":
                        for target_id in dictionary[2:-2].split():
                            if not reverse:
                                fastalign_line.append(
                                    f"{int(source_id)-1}-{int(target_id)-1}"
                                )
                            else:
                                fastalign_line.append(
                                    f"{int(target_id) - 1}-{int(source_id) - 1}"
                                )

                print(" ".join(fastalign_line), file=output_file)

                line = input_file.readline()
