from typing import Dict, List
from tokenization.utils import count_lines
import argparse


def alignment2dict(alignment: str) -> Dict[int, List[int]]:
    alignment_dictionary: Dict[int, List[int]] = {}
    for pair in alignment.rstrip().strip().split():
        try:
            source, target = pair.split("-")
            source, target = int(source), int(target)
            if source in alignment_dictionary:
                alignment_dictionary[source].append(target)
            else:
                alignment_dictionary[source] = [target]

        except ValueError:
            raise ValueError(
                f"Unable to split pair {pair} from alignment line: {alignment}."
            )

    return alignment_dictionary


def dict2alignment(alignment: Dict[int, List[int]]) -> str:
    alignments: List[str] = []

    for key, values in alignment.items():
        for v in values:
            alignments.append(f"{key}-{v}")

    return " ".join(alignments)


def detokenize_alignment(
    source_sentence: List[str],
    target_sentence: List[str],
    tokenized_source: List[str],
    tokenized_target: List[str],
    alignments: Dict[int, List[int]],
) -> Dict[int, List[int]]:
    # Detokenize source
    new_alignments: Dict[int, List[int]] = {}
    tokenized_index = 0
    for index in range(len(source_sentence)):
        tokenized_word: str = ""
        target_indexes: List[int] = []
        while tokenized_word != source_sentence[index]:
            tokenized_word += tokenized_source[tokenized_index]
            target_indexes.append(tokenized_index)
            tokenized_index += 1

        new_alignments[index] = []
        try:
            [new_alignments[index].extend(alignments[t]) for t in target_indexes]
        except KeyError:  # No alignment for this word
            continue

    # Detokenize target
    tokenized_index = 0
    for index in range(len(target_sentence)):
        tokenized_word: str = ""
        target_indexes: List[int] = []
        while tokenized_word != target_sentence[index]:
            tokenized_word += tokenized_target[tokenized_index]
            target_indexes.append(tokenized_index)
            tokenized_index += 1

        for key in new_alignments.keys():
            new_alignments[key] = list(
                set([index if x in target_indexes else x for x in new_alignments[key]])
            )

    return new_alignments


def detokenize_alignments(
    source_sentences_path: str,
    target_sentences_path: str,
    tokenized_source_sentences_path: str,
    tokenized_target_sentences_path: str,
    alignments_path: str,
    output_alignments: str,
):

    source_sentences_lines = count_lines(source_sentences_path)
    target_sentences_lines = count_lines(target_sentences_path)
    tokenized_source_sentences_lines = count_lines(tokenized_source_sentences_path)
    tokenized_target_sentences_lines = count_lines(tokenized_target_sentences_path)
    alignments_lines = count_lines(alignments_path)

    assert (
        source_sentences_lines
        == target_sentences_lines
        == tokenized_source_sentences_lines
        == tokenized_target_sentences_lines
        == alignments_lines
    ), (
        f"All input files must have the same number of lines. "
        f"{source_sentences_path}: {source_sentences_lines}. "
        f"{target_sentences_path}: {target_sentences_lines}. "
        f"{tokenized_source_sentences_path}: {tokenized_source_sentences_lines}. "
        f"{tokenized_target_sentences_path}: {tokenized_target_sentences_lines}. "
        f"{alignments_path}: {alignments_lines}."
    )
    """
    print(
        f"We will detokenize the alignment file  {alignments_path}. "
        f"source_sentences_path: {source_sentences_path}. "
        f"target_sentences_path: {target_sentences_path}. "
        f"tokenized_source_sentences_path: {tokenized_source_sentences_path}. "
        f"tokenized_target_sentences_path: {tokenized_target_sentences_path}. "
        f"Output: {output_alignments}"
    )
    """
    with open(source_sentences_path, "r", encoding="utf8") as source_sentences, open(
        target_sentences_path, "r", encoding="utf8"
    ) as target_sentences, open(
        tokenized_source_sentences_path, "r", encoding="utf8"
    ) as tokenized_source_sentences, open(
        tokenized_target_sentences_path, "r", encoding="utf8"
    ) as tokenized_target_sentences, open(
        alignments_path, "r", encoding="utf8"
    ) as alignments, open(
        output_alignments, "w+", encoding="utf8"
    ) as output:

        for (
            source_sentence,
            target_sentence,
            tokenized_source,
            tokenized_target,
            alignment,
        ) in zip(
            source_sentences,
            target_sentences,
            tokenized_source_sentences,
            tokenized_target_sentences,
            alignments,
        ):

            new_alignment: Dict[int, List[int]] = detokenize_alignment(
                source_sentence=source_sentence.split(),
                target_sentence=target_sentence.split(),
                tokenized_source=tokenized_source.split(),
                tokenized_target=tokenized_target.split(),
                alignments=alignment2dict(alignment),
            )

            print(dict2alignment(new_alignment), file=output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Alignments FastAlign")
    parser.add_argument(
        "--source_sentences_path",
        type=str,
        required=True,
        help="Paths to the source sentences in txt format (one per line)",
    )

    parser.add_argument(
        "--target_sentences_path",
        type=str,
        required=True,
        help="Paths to the target sentences in txt format (one per line)",
    )

    parser.add_argument(
        "--tokenized_source_sentences_path",
        type=str,
        required=True,
        help="Paths to the tokenized source sentences in txt format (one per line)",
    )

    parser.add_argument(
        "--tokenized_target_sentences_path",
        type=str,
        required=True,
        help="Paths to the tokenized target sentences in txt format (one per line)",
    )

    parser.add_argument(
        "--alignments_path",
        type=str,
        required=True,
        help="Paths to alignments in talp format (one per line)",
    )

    parser.add_argument(
        "--output_alignments",
        type=str,
        required=True,
        help="Path where the detokenized alignments are going to be written",
    )

    args = parser.parse_args()

    detokenize_alignments(
        source_sentences_path=args.source_sentences_path,
        target_sentences_path=args.target_sentences_path,
        tokenized_source_sentences_path=args.tokenized_source_sentences_path,
        tokenized_target_sentences_path=args.tokenized_target_sentences_path,
        alignments_path=args.alignments_path,
        output_alignments=args.output_alignments,
    )
