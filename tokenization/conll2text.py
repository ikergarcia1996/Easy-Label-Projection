import os
import argparse
import subprocess
from shlex import quote


def run_bash_command(command: str) -> None:
    subprocess.run(["bash", "-c", command])


def conll2text(
    input_path: str, sentences_output_path: str, tags_output_path: str = None
):

    if not os.path.exists(os.path.dirname(sentences_output_path)):
        os.makedirs(os.path.dirname(sentences_output_path))
    if tags_output_path and not os.path.exists(os.path.dirname(tags_output_path)):
        os.makedirs(os.path.dirname(tags_output_path))

    command = (
        f"cat {quote(input_path)} | awk '{{ print $1 }}' | "
        f"awk ' /^$/ {{ print; }} /./ {{ printf(\"%s \", $0); }} ' "
        f"> {quote(sentences_output_path)}"
    )

    run_bash_command(command)

    if tags_output_path:
        command = (
            f"cat {quote(input_path)} | awk '{{ print $2 }}' | "
            f"awk ' /^$/ {{ print; }} /./ {{ printf(\"%s \", $0); }} ' "
            f"> {quote(tags_output_path)}"
        )

    run_bash_command(command)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Alignments FastAlign")
    parser.add_argument(
        "--input_path",
        type=str,
        required=True,
        help="Input path (tabulate dataset format)",
    )

    parser.add_argument(
        "--sentences_output_path",
        type=str,
        required=True,
        help="Path where the sentences will be stored in txt format (one per line)",
    )

    parser.add_argument(
        "--tags_output_path",
        type=str,
        default=None,
        help="Path where the tags will be stored in txt format (one per line)",
    )

    args = parser.parse_args()

    conll2text(
        input_path=args.input_path,
        sentences_output_path=args.sentences_output_path,
        tags_output_path=args.tags_output_path,
    )
