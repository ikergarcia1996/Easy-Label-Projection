from torch.utils.data import IterableDataset
from typing import Dict, List
import math


def count_lines(input_path: str) -> int:
    with open(input_path, "r", encoding="utf8") as f:
        return sum(1 for _ in f)


def count_sentence_tsv(input_path: str) -> int:
    sentences = []
    lines = []
    with open(input_path, "r", encoding="utf8") as file:
        for line in file:
            line = line.rstrip().strip()
            if line == "":
                sentences.append(1)
                lines = []
            else:
                lines.append(line)

        if lines:
            sentences.append(1)
    return sum(sentences)


class AlignmentDataset(IterableDataset):
    def __init__(self, filename: str):

        self.filename = filename
        self.num_lines = count_lines(filename)
        print(f"Number of sentences in {filename}: {self.num_lines}")

    def __iter__(self):
        with open(self.filename, "r", encoding="utf8") as file:

            for alignment in file:
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

                yield alignment_dictionary

    def __getitem__(self, index):
        pass

    def __len__(self):
        return self.num_lines


class SourceDataset(IterableDataset):
    def __init__(self, filename: str):

        self.filename = filename
        self.num_lines = count_sentence_tsv(filename)
        print(f"Number of sentences in {filename}: {self.num_lines}")

    def __iter__(self):
        with open(self.filename, "r", encoding="utf8") as file:
            words = []
            tags_ids = []
            tags_type = []

            for line in file:
                line = line.rstrip().strip()
                if line == "":
                    yield words, tags_type, tags_ids
                    words = []
                    tags_ids = []
                    tags_type = []

                else:
                    tag: str
                    word: str
                    try:
                        word, tag = line.split()
                    except ValueError:
                        raise ValueError(f"Unable to split line: {line}")

                    if tag.startswith("B") or tag.startswith("U"):
                        try:
                            _, tag_type = tag.split("-")
                        except ValueError:
                            raise ValueError(
                                f"Unable to split tag: {tag_type} from line {line}"
                            )

                        tags_ids.append([len(words)])
                        tags_type.append(tag_type)

                    elif tag.startswith("I"):
                        try:
                            _, tag_type = tag.split("-")
                        except ValueError:
                            raise ValueError(
                                f"Unable to split tag: {tag_type} from line {line}"
                            )

                        if (
                            tags_ids[-1][-1] == (len(words) - 1)
                            and tags_type[-1] == tag_type
                        ):
                            tags_ids[-1].append(len(words))
                        else:
                            tags_ids.append([len(words)])
                            tags_type.append(tag_type)

                    words.append(word)

            if words:
                yield words, tags_type, tags_ids

    def __getitem__(self, index):
        pass

    def __len__(self):
        return self.num_lines


class TargetDataset(IterableDataset):
    def __init__(self, filename: str):

        self.filename = filename
        self.num_lines = count_lines(filename)
        print(f"Number of sentences in {filename}: {self.num_lines}")

    def __iter__(self):
        with open(self.filename, "r", encoding="utf8") as file:
            for sentence in file:
                words: List[str] = sentence.rstrip().strip().split()
                yield words

    def __getitem__(self, index):
        pass

    def __len__(self):
        return self.num_lines


class ProjectionDataloader:
    def __init__(
        self, source_tsv: str, target_txt: str, alignments_talp: str, batch_size: int
    ):

        self.source_dataset = SourceDataset(
            filename=source_tsv,
        )

        self.target_dataset = TargetDataset(
            filename=target_txt,
        )

        self.alignments_dataset = AlignmentDataset(
            filename=alignments_talp,
        )

        assert (
            len(self.source_dataset)
            == len(self.alignments_dataset)
            == len(self.target_dataset)
        ), (
            f"source_dataloader len: {len(self.source_dataset)}. "
            f"target_dataloader len: { len(self.target_dataset)}. "
            f"alignments_dataloader len: {len(self.alignments_dataset)}."
        )

        self.batch_size = batch_size

    def __iter__(self):
        batch: int = 0
        source_words_list = []
        tags_type_list = []
        tags_ids_list = []
        target_words_list = []
        alignment_dictionary_list = []

        for (
            (source_words, tags_type, tags_ids),
            (target_words),
            alignment_dictionary,
        ) in zip(self.source_dataset, self.target_dataset, self.alignments_dataset):

            batch += 1
            source_words_list.append(source_words)
            tags_type_list.append(tags_type)
            tags_ids_list.append(tags_ids)
            target_words_list.append(target_words)
            alignment_dictionary_list.append(alignment_dictionary)

            if batch == self.batch_size:
                yield source_words_list, tags_type_list, tags_ids_list, target_words_list, alignment_dictionary_list
                batch: int = 0
                source_words_list = []
                tags_type_list = []
                tags_ids_list = []
                target_words_list = []
                alignment_dictionary_list = []

        if batch:
            yield (
                source_words_list,
                tags_type_list,
                tags_ids_list,
                target_words_list,
                alignment_dictionary_list,
            )

    def __len__(self):
        return math.ceil(len(self.alignments_dataset) / self.batch_size)
