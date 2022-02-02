"""
USAGE:
python3 translate_dataset_marian.py --source_path path_to_source_sentences.txt --output_path output_path.txt --model_name Helsinki-NLP/opus-mt-es-eu
OPTIONAL
--batch_size (8 or 16 for 8Gb GPU), default:8
--prefix (Prefix to add to every sentence if the model needs it, i.e >>es<<). Default: None
"""


from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer

from tqdm import tqdm
from typing import TextIO, List
import argparse
import torch
import logging
import os
from torch.cuda.amp import autocast

if torch.cuda.is_available():
    device = torch.device("cuda:0")
else:
    device = torch.device("cpu")
    logging.warning("GPU not found, using CPU, translation will be very slow.")


def blocks(files, size=65536):
    while True:
        b = files.read(size)
        if not b:
            break
        yield b


def count_lines(input_path: str) -> int:
    with open(input_path, "r", encoding="utf8") as f:
        return sum(bl.count("\n") for bl in blocks(f))


def get_batch(file: TextIO, batch_size: int, prefix: str = None) -> List[str]:
    lines: List[str] = []
    line: str = file.readline()
    while line:
        line = line.rstrip().strip()
        if line:
            if prefix is not None:
                lines.append(prefix + line)
            else:
                lines.append(line)
            if len(lines) >= batch_size:
                return lines
        line = file.readline()

    return lines


def translate(
    source_path: str,
    output_path: str,
    source_lang: str,
    target_lang: str,
    batch_size=16,
    fp16: bool = False,
):

    if not os.path.exists(os.path.dirname(output_path)):
        os.makedirs(os.path.dirname(output_path))

    tokenizer = M2M100Tokenizer.from_pretrained("facebook/m2m100_1.2B")

    tokenizer.src_lang = source_lang

    model = M2M100ForConditionalGeneration.from_pretrained("facebook/m2m100_1.2B").to(
        device
    )
    model.eval()

    total_lines: int = count_lines(source_path)

    with open(source_path, "r", encoding="utf8") as input_file:
        with open(output_path, "w+", encoding="utf8") as output_file:
            with tqdm(total=total_lines, desc="Dataset translation") as pbar:
                batch: List[str] = get_batch(file=input_file, batch_size=batch_size)

                while batch:

                    encoded_src = tokenizer(
                        batch,
                        return_tensors="pt",
                        padding=True,
                        truncation=True,
                        max_length=512,
                    ).to(device)

                    with autocast(enabled=fp16), torch.no_grad():
                        generated_tokens = model.generate(
                            **encoded_src,
                            forced_bos_token_id=tokenizer.lang_code_to_id[target_lang]
                        )

                    tgt_text = tokenizer.batch_decode(
                        generated_tokens.cpu(), skip_special_tokens=True
                    )

                    print("\n".join(tgt_text), file=output_file)

                    batch = get_batch(file=input_file, batch_size=batch_size)

                    pbar.update(batch_size)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the translation experiments")
    parser.add_argument(
        "--source_path",
        type=str,
        required=True,
        help="Path to the source dataset",
    )

    parser.add_argument(
        "--output_path",
        type=str,
        required=True,
        help="Path to the output dataset",
    )

    parser.add_argument(
        "--source_lang",
        type=str,
        required=True,
        help="Source language id. See: https://huggingface.co/facebook/m2m100_1.2B",
    )

    parser.add_argument(
        "--target_lang",
        type=str,
        required=True,
        help="Target language id. See: https://huggingface.co/facebook/m2m100_1.2B",
    )

    parser.add_argument(
        "--batch_size",
        type=int,
        default=8,
        help="Batch size",
    )

    parser.add_argument(
        "--fp16",
        action="store_true",
        help="Use FP16",
    )

    args = parser.parse_args()

    translate(
        source_path=args.source_path,
        output_path=args.output_path,
        source_lang=args.source_lang,
        target_lang=args.target_lang,
        batch_size=args.batch_size,
        fp16=args.fp16,
    )
