import argparse
from annotation_projection import generate_alignments


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate alignments for a given dataset."
    )
    parser.add_argument(
        "--source_train",
        default=None,
        type=str,
        help="Path to the source training file. A txt file with one sentence per line",
    )
    parser.add_argument(
        "--target_train",
        default=None,
        type=str,
        help="Path to the target training file. A txt file with one sentence per line",
    )
    parser.add_argument(
        "--source_dev",
        default=None,
        type=str,
        help="Path to the source development file. A txt file with one sentence per line",
    )
    parser.add_argument(
        "--target_dev",
        default=None,
        type=str,
        help="Path to the target development file. A txt file with one sentence per line",
    )
    parser.add_argument(
        "--source_test",
        default=None,
        type=str,
        help="Path to the source test file. A txt file with one sentence per line",
    )
    parser.add_argument(
        "--target_test",
        default=None,
        type=str,
        help="Path to the target test file. A txt file with one sentence per line",
    )
    parser.add_argument(
        "--source_augmentation",
        default=None,
        type=str,
        help="Path to the source augmentation file. A txt file with one sentence per line",
    )
    parser.add_argument(
        "--target_augmentation",
        default=None,
        type=str,
        help="Path to the target augmentation file. A txt file with one sentence per line",
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        help="Path to the output directory",
    )
    parser.add_argument(
        "--output_name",
        type=str,
        help="Name of the output file",
    )
    parser.add_argument(
        "--do_mgiza",
        action="store_true",
        help="Whether to generate alignments using mgiza",
    )
    parser.add_argument(
        "--do_fastalign",
        action="store_true",
        help="Whether to generate alignments using fast_align",
    )
    parser.add_argument(
        "--do_simalign",
        action="store_true",
        help="Whether to generate alignments using simalign",
    )
    parser.add_argument(
        "--do_awesome",
        action="store_true",
        help="Whether to generate alignments using awesome",
    )
    parser.add_argument(
        "--remove_awesome_model",
        action="store_true",
        help="Whether to remove the trained awesome model after the alignment is generated",
    )
    parser.add_argument(
        "--model_name_or_path",
        default="bert-base-multilingual-cased",
        type=str,
        help="Huggingface Hub model name or path to a local model",
    )

    args = parser.parse_args()

    generate_alignments(
        source_train=args.source_train,
        target_train=args.target_train,
        source_dev=args.source_dev,
        target_dev=args.target_dev,
        source_test=args.source_test,
        target_test=args.target_test,
        source_augmentation=args.source_augmentation,
        target_augmentation=args.target_augmentation,
        output_dir=args.output_dir,
        output_name=args.output_name,
        do_mgiza=args.do_mgiza,
        do_fastalign=args.do_fastalign,
        do_simalign=args.do_simalign,
        do_awesome=args.do_awesome,
        remove_awesome_model=args.remove_awesome_model,
        model_name_or_path=args.model_name_or_path,
    )
