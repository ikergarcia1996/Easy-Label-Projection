import os
from shlex import quote
from fast_align.utils import run_bash_command


def read_err(err):
    T, m = "", ""
    for line in open(err):
        if "expected target length" in line:
            m = line.split()[-1]
        elif "final tension" in line:
            T = line.split()[-1]
    return T, m


def align_corpus(
    fast_align_dir: str,
    corpus_path: str,
    output_dir: str,
    alignment_direction: str,
) -> None:

    print(f"Running Fast Align...")
    assert alignment_direction not in [
        "forward, reverse, combine"
    ], f"alignment_direction {alignment_direction} not supported. Supported directions: [forward, reverse, combine]"

    fast_align_executable: str = os.path.join(fast_align_dir, "fast_align")
    atools_executable: str = os.path.join(fast_align_dir, "atools")

    if alignment_direction == "forward" or alignment_direction == "combine":
        print(f"    Running Forward Direction...")
        forward_name: str = "forward.talp"
        forward_command: str = (
            f"{quote(fast_align_executable)} "
            f"-i {quote(corpus_path)} "
            f"-d -o -v "
            f"> {quote(os.path.join(output_dir,forward_name))}"
        )
        run_bash_command(forward_command)

    if alignment_direction == "reverse" or alignment_direction == "combine":
        print(f"    Running Reverse Direction...")
        reverse_name: str = "reverse.talp"
        reverse_command: str = (
            f"{quote(fast_align_executable)} "
            f"-i {quote(corpus_path)} "
            f"-r -d -o -v "
            f"> {quote(os.path.join(output_dir,reverse_name))}"
        )
        run_bash_command(reverse_command)

    if alignment_direction == "combine":
        print(f"    Combining directions wi the grow-diag-final-and method...")
        forward_name: str = "forward.talp"
        reverse_name: str = "reverse.talp"
        combine_name: str = "grow_diag_final-and.talp"
        combine_command: str = (
            f"{quote(atools_executable)} "
            f"-i {quote(os.path.join(output_dir,forward_name))} "
            f"-j {quote(os.path.join(output_dir,reverse_name))} "
            f"-c grow-diag-final-and "
            f"> {quote(os.path.join(output_dir,combine_name))}"
        )

        run_bash_command(combine_command)

    print(f"Done!")


def train_fast_align(
    fast_align_dir: str,
    corpus_path: str,
    output_dir: str,
) -> None:
    fast_align_executable = os.path.join(fast_align_dir, "fast_align")

    forward_params_name: str = "fwd_params"
    forward_align_name: str = "foward.talp"
    forward_error_name: str = "fwd_err"
    forward_command: str = (
        f"{quote(fast_align_executable)} "
        f"-i {quote(corpus_path)} "
        f"-d -o -v -p "
        f" {quote(os.path.join(output_dir, forward_params_name))} "
        f"> {quote(os.path.join(output_dir, forward_align_name))} "
        f"2> {quote(os.path.join(output_dir, forward_error_name))}"
    )

    reverse_params_name: str = "rev_params"
    reverse_align_name: str = "reverse.talp"
    reverse_error_name: str = "rev_err"
    reverse_command: str = (
        f"{quote(fast_align_executable)} "
        f"-i {quote(corpus_path)} "
        f"-r -d -o -v -p "
        f" {quote(os.path.join(output_dir, reverse_params_name))} "
        f"> {quote(os.path.join(output_dir, reverse_align_name))} "
        f"2> {quote(os.path.join(output_dir, reverse_error_name))}"
    )

    run_bash_command(forward_command)
    run_bash_command(reverse_command)


def inference_fast_align(
    fast_align_dir: str,
    corpus_path: str,
    model_dir: str,
    output_path: str,
    heuristic: str = "grow-diag-final-and",
) -> None:
    fast_align_executable: str = os.path.join(fast_align_dir, "fast_align")
    atools_executable: str = os.path.join(fast_align_dir, "atools")
    forward_params_name: str = os.path.join(model_dir, "fwd_params")
    forward_error_name: str = os.path.join(model_dir, "fwd_err")
    reverse_params_name: str = os.path.join(model_dir, "rev_params")
    reverse_error_name: str = os.path.join(model_dir, "rev_err")

    fwd_T, fwd_m = read_err(forward_error_name)
    rev_T, rev_m = read_err(reverse_error_name)

    forward_file_name = f"{output_path}.forward"
    forward_command = (
        f"{fast_align_executable} "
        f"-i {corpus_path} "
        f"-d "
        f"-T {fwd_T} "
        f"-m {fwd_m} "
        f"-f {forward_params_name} "
        f"> {forward_file_name} "
    )
    run_bash_command(forward_command)

    get_column_command = (
        f"cat {forward_file_name} | "
        f"awk -F  \"\\\\\\\\|\\\\\\\\|\\\\\\\\|\" '{{print $3}}' | "
        f"awk '{{$1=$1}};1' "
        f"> {forward_file_name}.tmp"
    )
    run_bash_command(get_column_command)
    move_command = f"mv {forward_file_name}.tmp {forward_file_name}"
    run_bash_command(move_command)

    reverse_file_name = f"{output_path}.reverse"
    reverse_command = (
        f"{fast_align_executable} "
        f"-i {corpus_path} "
        f"-r "
        f"-d "
        f"-T {rev_T} "
        f"-m {rev_m} "
        f"-f {reverse_params_name} "
        f"> {reverse_file_name} "
    )
    run_bash_command(reverse_command)

    get_column_command = (
        f"cat {reverse_file_name} | "
        f"awk -F  \"\\\\\\\\|\\\\\\\\|\\\\\\\\|\" '{{print $3}}' | "
        f"awk '{{$1=$1}};1' "
        f"> {reverse_file_name}.tmp "
    )
    run_bash_command(get_column_command)
    move_command = f"mv {reverse_file_name}.tmp {reverse_file_name}"
    run_bash_command(move_command)

    combine_command: str = (
        f"{quote(atools_executable)} "
        f"-i {forward_file_name} "
        f"-j {reverse_file_name} "
        f"-c {heuristic} "
        f"> {output_path}"
    )
    run_bash_command(combine_command)
