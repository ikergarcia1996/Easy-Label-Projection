import os
import argparse
from typing import Optional


def text2conll(
    sentences_path: str,
    output_path: str,
    source_sentences_path: Optional[str] = None,
    iob2_path: str = None,
    source_iob2_path: Optional[str] = None,
    use_O_as_backoff: bool = False,
):

    if not iob2_path:
        source_sentences_path = None
        source_iob2_path = None
        print("Warning: No iob2_path, we will not use backoff sentences")

    if use_O_as_backoff:
        source_sentences_path = None
        source_iob2_path = None
        print("Warning: use_O_as_backoff, we will use O's as backoff")

    if not os.path.exists(os.path.dirname(output_path)):
        os.makedirs(os.path.dirname(output_path))

    total_sentences: int = 0
    projected_sentences: int = 0

    with open(sentences_path, "r", encoding="utf8") as sentences, open(
        output_path, "w+", encoding="utf8"
    ) as output:

        if iob2_path:
            iob2_tags = open(iob2_path, "r", encoding="utf8")
        else:
            iob2_tags = None

        if source_sentences_path:
            source_sentences = open(source_sentences_path, "r", encoding="utf8")
            source_iob2 = open(source_iob2_path, "r", encoding="utf8")

        sentence = sentences.readline().rstrip().strip()

        if iob2_tags:
            iob2_tag = iob2_tags.readline().rstrip().strip()
        else:
            iob2_tag = None

        if source_sentences_path:
            source_sentence, source_iob2_tag = (
                source_sentences.readline().rstrip().strip(),
                source_iob2.readline().rstrip().strip(),
            )
        while sentence:

            if iob2_tag:
                if len(iob2_tag) == 0:
                    if source_sentences_path:
                        sentence = source_sentence
                        iob2_tag = source_iob2_tag
                    if use_O_as_backoff:
                        iob2_tag = " ".join(["0"] * len(sentence.split()))

                if iob2_tag and len(iob2_tag) > 0:
                    words = sentence.split()
                    iob2_tag = iob2_tag.split()

                    assert len(words) == len(
                        iob2_tag
                    ), f"We must have a tag for each word. Words: {words}. Tags: {iob2_tag}."

                    for word, tag in zip(words, iob2_tag):
                        print(f"{word} {tag}", file=output)
                    print(file=output)
                    projected_sentences += 1

                else:
                    if source_sentences_path:
                        raise ValueError(
                            f"Something went wrong, no backoff sentence found. "
                            f"source_sentences_path: {source_sentences_path} "
                            f"source_iob2_path: {source_iob2_path}"
                        )
            else:
                for word in sentence.split():
                    print(f"{word} O", file=output)
                print(file=output)
                projected_sentences += 1

            total_sentences += 1

            if iob2_tags:
                iob2_tag = iob2_tags.readline().rstrip().strip()
            else:
                iob2_tag = None

            if source_sentences_path:
                source_sentence, source_iob2_tag = (
                    source_sentences.readline().rstrip().strip(),
                    source_iob2.readline().rstrip().strip(),
                )

            sentence = sentences.readline().rstrip().strip()

    print(
        f"Projected {projected_sentences} of {total_sentences} examples: "
        f"{round((projected_sentences/total_sentences)*100,2)}%"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Alignments FastAlign")
    parser.add_argument(
        "--sentences_path",
        type=str,
        required=True,
        help="Path to the source sentences in txt format (one per line)",
    )

    parser.add_argument(
        "--iob2_path",
        type=str,
        default=None,
        help="Path to the source sentences in txt format (one per line)",
    )

    parser.add_argument(
        "--output_path",
        type=str,
        required=True,
        help="Path to the source sentences in txt format (one per line)",
    )

    parser.add_argument(
        "--source_sentences_path",
        type=str,
        default=None,
        help="Path to the source sentences in txt format (one per line)",
    )

    parser.add_argument(
        "--source_iob2_path",
        type=str,
        default=None,
        help="Path to the source iob2 tags in txt format (one per line)",
    )

    parser.add_argument(
        "--use_O_as_backoff",
        action="store_true",
        help="If we don't have IOB2 tag for a sentence, use O's",
    )

    args = parser.parse_args()

    text2conll(
        sentences_path=args.sentences_path,
        iob2_path=args.iob2_path,
        output_path=args.output_path,
        source_sentences_path=args.source_sentences_path,
        source_iob2_path=args.source_iob2_path,
        use_O_as_backoff=args.use_O_as_backoff,
    )
