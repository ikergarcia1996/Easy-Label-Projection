from shlex import quote
from awesome.utils import run_bash_command
import sys


def train_awesome(
    corpus_path: str,
    output_dir: str,
    model_name_or_path: str = "bert-base-multilingual-cased",
    batch_size: int = 8,
    gradient_accumulation_steps: int = 1,
    num_train_epochs: int = 1,
    learning_rate: float = 2e-5,
    max_steps: int = 40000,
) -> None:

    command = (
        f"awesome-train "
        f"--output_dir={quote(output_dir)} "
        f"--model_name_or_path={quote(model_name_or_path)} "
        f"--extraction 'softmax' "
        f"--do_train "
        f"--train_mlm "
        f"--train_tlm "
        f"--train_tlm_full "
        f"--train_so "
        f"--train_psi "
        f"--train_data_file={corpus_path} "
        f"--per_gpu_train_batch_size {quote(str(batch_size))} "
        f"--gradient_accumulation_steps {quote(str(gradient_accumulation_steps))} "
        f"--num_train_epochs {quote(str(num_train_epochs))} "
        f"--max_steps {quote(str(max_steps))} "
        f"--learning_rate {quote(str(learning_rate))} "
        f"--overwrite_output_dir "
        f"--save_steps {quote(str(sys.maxsize))} "
        f"--overwrite_cache "
        f"--fp16 "
    )

    print(command)
    run_bash_command(command)


def inference_awesome(
    corpus_path: str,
    output_path: str,
    model_name_or_path: str = "bert-base-multilingual-cased",
    batch_size: int = 32,
) -> None:

    command: str = (
        f"awesome-align "
        f"--output_file={output_path} "
        f"--model_name_or_path={model_name_or_path} "
        f"--data_file={corpus_path} "
        f"--extraction 'softmax' "
        f"--batch_size {batch_size} "
    )

    print(command)

    run_bash_command(command)
