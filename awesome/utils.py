import subprocess
from shlex import quote
import os


def run_bash_command(command: str) -> None:
    subprocess.run(["bash", "-c", command])


def blocks(files, size=65536):
    while True:
        b = files.read(size)
        if not b:
            break
        yield b


def count_lines(input_path: str) -> int:
    with open(input_path, "r", encoding="utf8") as f:
        return sum(bl.count("\n") for bl in blocks(f))


def data2awesome(
    source_path: str,
    target_path: str,
    output_path: str,
):

    command = f'sed "s/\\t/ /g" {quote(source_path)} > {quote(source_path)}.tmp'
    run_bash_command(command)
    command = f'sed "s/\\t/ /g" {quote(target_path)} > {quote(target_path)}.tmp'
    run_bash_command(command)
    command = (
        f'paste -d "\\t" {quote(source_path)}.tmp {quote(target_path)}.tmp |'
        f' sed "s/\\t/ ||| /g" > {quote(output_path)}'
    )
    run_bash_command(command)

    os.remove(f"{quote(source_path)}.tmp")
    os.remove(f"{quote(target_path)}.tmp")
