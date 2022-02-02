from typing import TextIO, List
import os
import argparse


def to_IOB_encoding(input_path: str, output_path: str, block_size=65536) -> None:
    # From IOB2 or BILOU
    prev_tag_b: str = "O"
    prev_tag_t: str = ""
    input_file: TextIO = open(input_path, "r", encoding="utf-8")
    output_file: TextIO = open(output_path, "w+", encoding="utf-8")

    lines: List[str] = input_file.readlines(block_size)
    line_no: int = 0
    while lines:
        text_2_write: List[str] = []
        for line in lines:

            if line == "\n":
                prev_tag_b = "O"
                prev_tag_t = ""
                text_2_write.append(line)
            else:
                try:
                    word, tag = line.rstrip().split(" ")
                except ValueError:
                    input_file.close()
                    output_file.close()
                    raise ValueError(
                        f"Error in line {line_no}, unable to split the text in 2 fields. Text: {line}"
                    )
                if tag == "O":
                    prev_tag_b = "O"
                    prev_tag_t = ""
                    text_2_write.append(line)
                else:
                    try:
                        b, t = tag.split("-")
                    except ValueError:
                        input_file.close()
                        output_file.close()
                        raise ValueError(
                            f"Error in line {line_no}, unable to split the tag in 2 fields. Text: {line} Tag: {tag}"
                        )
                    if (b == "B" or b == "U") and prev_tag_b != "O" and prev_tag_t == t:
                        text_2_write.append(f"{word} B-{t}\n")
                    else:
                        text_2_write.append(f"{word} I-{t}\n")
                    prev_tag_b = b
                    prev_tag_t = t
            line_no += 1

        print("".join(text_2_write), file=output_file, end="")
        lines = input_file.readlines(block_size)

    input_file.close()
    output_file.close()


def to_IOB2_encoding(input_path: str, output_path: str, block_size=65536) -> None:
    # From IOB or BILOU
    prev_tag_b: str = "O"
    prev_tag_t: str = ""
    input_file: TextIO = open(input_path, "r", encoding="utf-8")
    output_file: TextIO = open(output_path, "w+", encoding="utf-8")

    lines: List[str] = input_file.readlines(block_size)
    line_no: int = 0
    while lines:
        text_2_write: List[str] = []
        for line in lines:

            if line == "\n":
                prev_tag_b = "O"
                prev_tag_t = ""
                text_2_write.append(line)
            else:
                try:
                    word, tag = line.rstrip().split(" ")
                except ValueError:
                    input_file.close()
                    output_file.close()
                    raise ValueError(
                        f"Error in line {line_no}, unable to split the text in 2 fields. Text: {line}"
                    )
                if tag == "O":
                    prev_tag_b = "O"
                    prev_tag_t = ""
                    text_2_write.append(line)
                else:
                    try:
                        b, t = tag.split("-")
                    except ValueError:
                        input_file.close()
                        output_file.close()
                        raise ValueError(
                            f"Error in line {line_no}, unable to split the tag in 2 fields. Text: {line} Tag: {tag}"
                        )
                    if (b == "B" or b == "U") or (
                        (prev_tag_b == "O") or (prev_tag_t != "" and prev_tag_t != t)
                    ):
                        text_2_write.append(f"{word} B-{t}\n")
                    else:
                        text_2_write.append(f"{word} I-{t}\n")
                    prev_tag_b = b
                    prev_tag_t = t
            line_no += 1

        print("".join(text_2_write), file=output_file, end="")
        lines = input_file.readlines(block_size)

    input_file.close()
    output_file.close()


def to_BILOU_encoding(input_path: str, output_path: str, block_size=65536) -> None:
    # From IOB or IOB2
    prev_word: str = ""
    prev_word_tag_tmp: str = ""
    input_file: TextIO = open(input_path, "r", encoding="utf-8")
    output_file: TextIO = open(output_path, "w+", encoding="utf-8")

    lines: List[str] = input_file.readlines(block_size)
    line_no: int = 0
    while lines:
        text_2_write: List[str] = []
        for line in lines:

            if line == "\n":
                if prev_word != "":
                    try:
                        prev_b, prev_t = prev_word_tag_tmp.split("-")
                    except ValueError:
                        raise ValueError(
                            f"Error in line {line_no}, unable to split the tag in 2 fields. Tag: {prev_word_tag_tmp}"
                        )

                    if prev_b == "B":
                        text_2_write.append(f"{prev_word} U-{prev_t}\n")
                    else:
                        text_2_write.append(f"{prev_word} L-{prev_t}\n")

                text_2_write.append(line)
                prev_word: str = ""
                prev_word_tag_tmp: str = ""

            else:
                try:
                    word, tag = line.rstrip().split(" ")
                except ValueError:
                    input_file.close()
                    output_file.close()
                    raise ValueError(
                        f"Error in line {line_no}, unable to split the text in 2 fields. Text: {line}"
                    )

                if tag == "O":
                    if prev_word != "":
                        try:
                            prev_b, prev_t = prev_word_tag_tmp.split("-")
                        except ValueError:
                            raise ValueError(
                                f"Error in line {line_no}, unable to split the tag in 2 fields. Tag: {prev_word_tag_tmp}"
                            )

                        if prev_b == "B":
                            text_2_write.append(f"{prev_word} U-{prev_t}\n")
                        else:
                            text_2_write.append(f"{prev_word} L-{prev_t}\n")

                    text_2_write.append(line)
                    prev_word: str = ""
                    prev_word_tag_tmp: str = ""

                else:

                    try:
                        b, t = tag.split("-")
                    except ValueError:
                        raise ValueError(
                            f"Error in line {line_no}, unable to split the tag in 2 fields. Text: {line} Tag: {tag}"
                        )

                    if prev_word == "":
                        if b == "U":
                            text_2_write.append(line)
                            prev_word = ""
                            prev_word_tag_tmp = ""
                        else:
                            prev_word = word
                            prev_word_tag_tmp = f"B-{t}"

                    else:
                        try:
                            prev_b, prev_t = prev_word_tag_tmp.split("-")
                        except ValueError:
                            raise ValueError(
                                f"Error in line {line_no}, unable to split the tag in 2 fields. Tag: {prev_word_tag_tmp}"
                            )

                        if b == "U":
                            if prev_b == "B":
                                text_2_write.append(f"{prev_word} U-{prev_t}\n")
                            else:
                                text_2_write.append(f"{prev_word} L-{prev_t}\n")

                            text_2_write.append(line)
                            prev_word = ""
                            prev_word_tag_tmp = ""

                        elif b == "B":
                            if prev_b == "B":
                                text_2_write.append(f"{prev_word} U-{prev_t}\n")
                            else:
                                text_2_write.append(f"{prev_word} L-{prev_t}\n")
                            prev_word = word
                            prev_word_tag_tmp = f"B-{t}"

                        else:
                            if prev_t != t:
                                if prev_b == "B":
                                    text_2_write.append(f"{prev_word} U-{prev_t}\n")
                                else:
                                    text_2_write.append(f"{prev_word} L-{prev_t}\n")
                                prev_word = word
                                prev_word_tag_tmp = f"B-{t}"
                            else:
                                if prev_b == "B":
                                    text_2_write.append(f"{prev_word} B-{prev_t}\n")
                                else:
                                    text_2_write.append(f"{prev_word} I-{prev_t}\n")

                                prev_word = word
                                prev_word_tag_tmp = f"I-{t}"

            line_no += 1

        print("".join(text_2_write), file=output_file, end="")
        lines = input_file.readlines(block_size)

    if prev_word != "":
        try:
            prev_b, prev_t = prev_word_tag_tmp.split("-")
        except ValueError:
            raise ValueError(
                f"Error in line {line_no}, unable to split the tag in 2 fields. Tag: {prev_word_tag_tmp}"
            )

        if prev_b == "B":
            print(f"{prev_word} U-{prev_t}\n", file=output_file, end="")
        else:
            print(f"{prev_word} L-{prev_t}\n", file=output_file, end="")

    input_file.close()
    output_file.close()


def rewrite_only_spans(dataset_path: str, block_size=65536) -> None:
    input_file: TextIO = open(dataset_path, "r", encoding="utf-8")
    output_file: TextIO = open(f"{dataset_path}.tmp", "w+", encoding="utf-8")

    lines: List[str] = input_file.readlines(block_size)
    line_no: int = 0
    text_to_print = []
    while lines:
        for line in lines:
            line_no += 1
            line = line.rstrip()
            if line == "":
                text_to_print.append("\n")
            else:
                try:
                    word, tag = line.split(" ")
                except ValueError:
                    input_file.close()
                    output_file.close()
                    raise ValueError(
                        f"Error in line {line_no}. Unable to split in word and tag. Line: {line}"
                    )

                if tag == "O":
                    tb = "O"
                else:
                    try:
                        tb, tt = tag.split("-")
                    except ValueError:
                        input_file.close()
                        output_file.close()
                        raise ValueError(
                            f"Error in line {line_no}. Unable to tag. Tag: {tag}. Line: {line}"
                        )

                text_to_print.append(f"{word} {tb}\n")

        print("".join(text_to_print), file=output_file, end="")
        text_to_print = []
        lines = input_file.readlines(block_size)

    input_file.close()
    output_file.close()

    os.remove(dataset_path)
    os.rename(f"{dataset_path}.tmp", dataset_path)


def rewrite_dataset(dataset_path: str, encoding: str, output_path=None) -> None:

    if not os.path.exists(os.path.dirname(output_path)):
        os.makedirs(os.path.dirname(output_path))

    if encoding is not None:
        if encoding == "IOB":
            to_IOB_encoding(dataset_path, f"{dataset_path}.tmp")
        elif encoding == "IOB2":
            to_IOB2_encoding(dataset_path, f"{dataset_path}.tmp")
        elif encoding == "BILOU":
            to_BILOU_encoding(dataset_path, f"{dataset_path}.tmp")
        else:
            raise NotImplementedError(
                f"Encoding {encoding} not supported. Supported encodings [IOB,IOB2,BILOU]"
            )

        if output_path is None:
            os.remove(dataset_path)
            os.rename(f"{dataset_path}.tmp", dataset_path)
        else:
            os.rename(f"{dataset_path}.tmp", output_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Alignments FastAlign")
    parser.add_argument(
        "--dataset_path",
        type=str,
        required=True,
        help="Path to the source dataset in IOB/IOB2/BILOU format",
    )

    parser.add_argument(
        "--encoding",
        type=str,
        required=True,
        choices=["IOB", "IOB2", "BILOU"],
        help="Encoding to which the dataset will be converted",
    )

    parser.add_argument(
        "--output_path",
        type=str,
        required=True,
        help="Output path",
    )

    args = parser.parse_args()

    rewrite_dataset(
        dataset_path=args.dataset_path,
        encoding=args.encoding,
        output_path=args.output_path,
    )
