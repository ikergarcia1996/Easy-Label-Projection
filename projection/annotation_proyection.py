import multiprocessing
import os
from typing import List, Dict
from projection.dataset import ProjectionDataloader
import math
from tqdm import tqdm
import string

puncs = set(string.punctuation)


def batch(iterable, n=1) -> iter:

    l: int = len(iterable)
    p: int = math.ceil(l / n)
    for ndx in range(0, l, p):
        yield iterable[ndx : min(ndx + p, l)]


def sentence_projection(
    source_words: List[str],
    source_tags_type: List[str],
    source_tags_ids: List[List[int]],
    target_words: List[str],
    alignments: Dict,
) -> List[str]:

    assert len(source_tags_type) == len(source_tags_ids)

    if len(target_words) == 0 or len(source_words) == 0:
        print(
            f"Warning, empty sentence found. source_words: {source_words}. target_words: {target_words}"
        )
        return ["O"] * len(target_words)

    # GET TARGET TAGS IDS

    target_tags_ids: List[List[int]] = []
    target_tags_types: List[str] = []

    for source_tag_ids, source_tag_type in zip(source_tags_ids, source_tags_type):
        target_tag = []
        for tag_id in source_tag_ids:
            try:
                target_tag.extend(alignments[tag_id])
            except KeyError:
                continue

        target_tag = sorted(
            list(set(target_tag))
        )  # ENSURE NO DUPLICATED VALUES AND SORT

        if target_tag:
            target_tags_ids.append(target_tag)
            target_tags_types.append(source_tag_type)

    # REMOVE TAGS THAT ARE PUNCTUATION

    for target_tag_idx in range(len(target_tags_ids) - 1, -1, -1):
        target_tags_c = target_tags_ids[target_tag_idx].copy()
        for tag_idx in range(len(target_tags_ids[target_tag_idx]) - 1, -1, -1):
            try:
                tword = target_words[target_tags_ids[target_tag_idx][tag_idx]].strip()
            except IndexError:
                raise IndexError(
                    f"\ntarget_tags_ids: {target_tags_ids}\n"
                    f"target_tags_c: {target_tags_c}\n"
                    f"target_tags_ids[target_tag_idx]: {target_tags_ids[target_tag_idx]}\n"
                    f"tag_idx: {tag_idx}\n"
                    f"target_tag_idx:{target_tag_idx}\n"
                    f"source_words: {source_words}\n"
                    f"target_words: {target_words}\n"
                )
            if all([char in puncs for char in tword]):
                # print(f"Warning: Removing word: {tword} from projected tag. ")
                del target_tags_ids[target_tag_idx][tag_idx]

        if len(target_tags_ids[target_tag_idx]) == 0:
            del target_tags_ids[target_tag_idx]
            del target_tags_types[target_tag_idx]
            # print(f"Warning: Removing tag: {[target_words[i] for i in target_tags_c]}")

    # FIX DISCONTINUOUS SPANS

    for target_tag_no, target_tag_ids in enumerate(target_tags_ids):

        # SPLIT IN GROUPS

        groups: List[List[int]] = [[target_tag_ids[0]]]
        for tag_id in target_tag_ids[1:]:
            if tag_id != groups[-1][-1] + 1:
                groups.append([tag_id])
            else:
                groups[-1].append(tag_id)

        # MERGE GROUPS WITH GAP = 1

        i = 0
        while i < len(groups) - 1:
            if groups[i + 1][-1] - groups[i][0] <= 2:

                groups[i] = (
                    groups[i]
                    + list(range(groups[i][-1] + 1, groups[i + 1][0]))
                    + groups[i + 1]
                )
                del groups[i + 1]
            else:
                i += 1

        # GET LARGEST GROUP

        target_tags_ids[target_tag_no] = max(groups, key=len)

    # FIX COLLISIONS
    # MERGE SAME TYPE TAGS

    i = 0
    while i < len(target_tags_ids) - 1:
        if target_tags_ids[i][-1] >= target_tags_ids[i + 1][0]:

            if target_tags_types[i] == target_tags_types[i + 1]:
                target_tags_ids[i] = sorted(
                    list(set(target_tags_ids[i] + target_tags_ids[i + 1]))
                )

                del target_tags_ids[i + 1]
                del target_tags_types[i + 1]

            else:
                i += 1
        else:
            i += 1

    # GET LARGEST TAG IF COLLISION
    i = 0
    while i < len(target_tags_ids) - 1:
        if target_tags_ids[i][-1] >= target_tags_ids[i + 1][0]:
            if len(target_tags_ids[i]) > len(target_tags_ids[i + 1]):
                del target_tags_types[i + 1]
                del target_tags_ids[i + 1]
            else:
                del target_tags_types[i]
                del target_tags_ids[i]

        else:
            i += 1

    # WRITE TAGS

    target_tags: List[str] = ["O"] * len(target_words)

    for tag_ids, tag_type in zip(target_tags_ids, target_tags_types):
        try:
            if tag_ids:
                target_tags[tag_ids[0]] = f"B-{tag_type}"
                for tag_id in tag_ids[1:]:
                    target_tags[tag_id] = f"I-{tag_type}"
        except IndexError:
            print(f"target_tags: {target_tags}. tag_id:{tag_ids}")
            print(f"Source words: {source_words}")
            print(f"Source tags: {source_tags_ids}")
            print(f"target_words: {target_words}.")
            print(f"alignments: {alignments}")
            print("=================================")
            raise

    return target_tags


def sentences_projection(
    sources_words: List[List[str]],
    sources_tags_type: List[List[str]],
    sources_tags_ids: List[List[List[int]]],
    target_words: List[List[str]],
    alignments: List[Dict],
) -> str:

    assert (
        len(sources_words)
        == len(sources_tags_type)
        == len(sources_tags_ids)
        == len(target_words)
        == len(alignments)
    ), (
        f"len(sources_words): {len(sources_words)}. "
        f"len(sources_tags_type): {len(sources_tags_type)}. "
        f"len(sources_tags_ids): {len(sources_tags_ids)}. "
        f"len(target_words): {len(target_words)}. "
        f"len(alignments): {len(alignments)}. \n"
        f"sources_words: {sources_words}. "
        f"sources_tags_ids: {sources_tags_ids}. "
        f"target_words: {target_words}. "
        f"alignments: {alignments}."
    )

    output: List[str] = []

    for (
        source_words,
        source_tags_type,
        source_tags_ids,
        target_words,
        alignments,
    ) in zip(
        sources_words, sources_tags_type, sources_tags_ids, target_words, alignments
    ):
        if target_words and source_words:
            target_tags = sentence_projection(
                source_words=source_words,
                source_tags_type=source_tags_type,
                source_tags_ids=source_tags_ids,
                target_words=target_words,
                alignments=alignments,
            )

            assert len(target_words) == len(target_tags)

            output.append(
                "\n".join([f"{w} {t}" for w, t in zip(target_words, target_tags)])
            )

        else:
            print(
                f"Warning, empty sentence found. source_words: {source_words}. target_words: {target_words}"
            )

    return "\n\n".join(output)


def dataset_projection(
    source_dataset: str,
    target_sentences: str,
    alignments_path: str,
    batch_size: int,
    output_path: str,
):
    print(
        f"Datset projection:\n"
        f"Source dataset: {source_dataset}.\n"
        f"Target_sentences: {target_sentences}.\n"
        f"alignments_path: {alignments_path}.\n"
        f"batch_size: {batch_size}.\n"
        f"output_path:{output_path}.\n"
    )
    if not os.path.exists(os.path.dirname(output_path)):
        os.makedirs(os.path.dirname(output_path))

    data_loader = ProjectionDataloader(
        source_tsv=source_dataset,
        target_txt=target_sentences,
        alignments_talp=alignments_path,
        batch_size=batch_size,
    )
    data_loader_len = len(data_loader)

    data_loader = iter(data_loader)

    source_words, tags_type, tags_ids, target_words, alignment_dictionary = next(
        data_loader
    )

    projections = []

    with open(output_path, "w+", encoding="utf8") as output_file, tqdm(
        total=data_loader_len, desc="Annotation projection"
    ) as pbar:
        while (
            source_words
            and tags_type
            and tags_ids
            and target_words
            and alignment_dictionary
        ):
            with multiprocessing.Pool(os.cpu_count()) as pool:

                async_job = pool.starmap_async(
                    sentences_projection,
                    zip(
                        batch(source_words, n=os.cpu_count()),
                        batch(tags_type, n=os.cpu_count()),
                        batch(tags_ids, n=os.cpu_count()),
                        batch(target_words, n=os.cpu_count()),
                        batch(alignment_dictionary, n=os.cpu_count()),
                    ),
                )

                if projections:
                    print("\n\n".join(projections), file=output_file)
                    print(file=output_file)

                pbar.update(1)

                try:
                    (
                        source_words,
                        tags_type,
                        tags_ids,
                        target_words,
                        alignment_dictionary,
                    ) = next(data_loader)
                except StopIteration:
                    source_words = []
                    tags_type = []
                    tags_ids = []
                    target_words = []
                    alignment_dictionary = []

                projections = async_job.get()

        if projections:
            print("\n\n".join(projections), file=output_file)
            print(file=output_file)
