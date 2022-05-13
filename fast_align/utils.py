import subprocess
from typing import List


def run_bash_command(command: str) -> None:
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


def data2fastalign(
    source_path: str,
    target_path: str,
    output_path: str,
):

    assert count_lines(source_path) == count_lines(target_path), (
        f"{source_path} and {target_path} should have the same number of lines. "
        f"{count_lines(source_path)} != {count_lines(target_path)}"
    )

    with open(source_path, "r", encoding="utf8") as source_file, open(
        target_path, "r", encoding="utf8"
    ) as target_file, open(output_path, "w", encoding="utf8") as output_file:
        for source_line, target_line in zip(source_file, target_file):
            source_line = source_line.strip().replace("\t", " ")
            target_line = target_line.strip().replace("\t", " ")
            print(f"{source_line} ||| {target_line}", file=output_file)
