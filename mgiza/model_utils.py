import os
import subprocess
import glob
from shlex import quote
from mgiza.config_file import get_config_file
from shutil import copyfile
from mgiza.utils import mgiza2fastalign, run_bash_command


def run_mgiza(mgizapp_dir, source_file, target_file, output_dir, output_name):
    print("plain2snt step...")
    bin_dir: str = os.path.join(mgizapp_dir, "bin")
    plain2snt = os.path.join(bin_dir, "plain2snt")
    source_vcb = os.path.join(output_dir, "source.vcb")
    target_vcb = os.path.join(output_dir, "target.vcb")
    snt1 = os.path.join(output_dir, "source_target.snt")
    snt2 = os.path.join(output_dir, "target_source.snt")
    command = (
        f"{quote(plain2snt)} {quote(source_file)} {quote(target_file)} "
        f"-vcb1 {quote(source_vcb)} -vcb2 {quote(target_vcb)} "
        f"-snt1 {quote(snt1)} -snt2 {quote(snt2)}"
    )
    run_bash_command(command)

    print("snt2cooc step...")

    plain2snt = os.path.join(bin_dir, "snt2cooc")
    cooc = os.path.join(output_dir, "data.cooc")
    command = f"{quote(plain2snt)} {quote(cooc)} {quote(source_vcb)} {quote(target_vcb)} {quote(snt1)}"
    run_bash_command(command)

    config_file = get_config_file(
        coocurrencefile=cooc,
        corpusfile=snt1,
        log_file=os.path.join(output_dir, "log_file.txt"),
        sourcevocabularyfile=source_vcb,
        targetvocabularyfile=target_vcb,
        outputpath=output_dir,
    )

    config_file_path = os.path.join(output_dir, "configfile")
    with open(config_file_path, "w+") as cfile:
        print(config_file, file=cfile)

    print("Running mgiza...")

    mgiza = os.path.join(bin_dir, "mgiza")
    command = f"{quote(mgiza)} {quote(config_file_path)}"
    run_bash_command(command)

    print("Merging files...")
    files = glob.glob(os.path.join(output_dir, "src_trg.dict.A3.final.*"))
    files_path = " ".join([quote(file) for file in files])

    merge_script = os.path.join(mgizapp_dir, "scripts/merge_alignment.py")
    ouputfile = os.path.join(output_dir, output_name)
    command = f"python3 {quote(merge_script)} {files_path} > {quote(ouputfile)}"
    run_bash_command(command)

    # Remove partial files
    for file in files:
        os.remove(file)


def make_classed(mgizapp_dir, output_dir, source_file, target_file):
    bin_dir: str = os.path.join(mgizapp_dir, "bin")
    mkcls: str = os.path.join(bin_dir, "mkcls")

    print("MKCLS step...")
    source_classes_path = os.path.join(output_dir, "source.vcb.classes")
    command = (
        f"{quote(mkcls)} -n10 -p{quote(source_file)} -V{quote(source_classes_path)}"
    )

    run_bash_command(command)

    target_classes_path = os.path.join(output_dir, "target.vcb.classes")
    command = (
        f"{quote(mkcls)} -n10 -p{quote(target_file)} -V{quote(target_classes_path)}"
    )

    run_bash_command(command)

    return source_classes_path, target_classes_path


def align_corpus(
    source_file: str,
    target_file,
    output_dir: str,
    mgizapp_dir: str = "mgiza/mgizapp",
    atools_executable: str = "fast_align/fast_align/build/atools",
    alignment_direction: str = "combine",
):

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    source_classes_path, target_classes_path = make_classed(
        mgizapp_dir=mgizapp_dir,
        output_dir=output_dir,
        source_file=source_file,
        target_file=target_file,
    )

    forward_dir = os.path.join(output_dir, "forward")
    reverse_dir = os.path.join(output_dir, "reverse")

    if alignment_direction == "forward" or alignment_direction == "combine":
        print("FORWARD DIRECTION")
        if not os.path.exists(forward_dir):
            os.makedirs(forward_dir)

        copyfile(source_classes_path, os.path.join(forward_dir, "source.vcb.classes"))
        copyfile(target_classes_path, os.path.join(forward_dir, "target.vcb.classes"))
        run_mgiza(
            mgizapp_dir=mgizapp_dir,
            source_file=source_file,
            target_file=target_file,
            output_dir=forward_dir,
            output_name="forward.giza",
        )
        print("giza2talp")
        mgiza2fastalign(
            os.path.join(forward_dir, "forward.giza"),
            os.path.join(forward_dir, "forward.talp"),
            reverse=False,
        )

    if alignment_direction == "reverse" or alignment_direction == "combine":
        print("REVERSE DIRECTION")
        if not os.path.exists(reverse_dir):
            os.makedirs(reverse_dir)
        copyfile(source_classes_path, os.path.join(reverse_dir, "target.vcb.classes"))
        copyfile(source_classes_path, os.path.join(reverse_dir, "source.classes"))
        run_mgiza(
            mgizapp_dir=mgizapp_dir,
            source_file=target_file,
            target_file=source_file,
            output_dir=reverse_dir,
            output_name="reverse.giza",
        )
        print("giza2talp")
        mgiza2fastalign(
            os.path.join(reverse_dir, "reverse.giza"),
            os.path.join(reverse_dir, "reverse.talp"),
            reverse=True,
        )

    if alignment_direction == "forward" or alignment_direction == "combine":
        os.rename(
            os.path.join(forward_dir, "forward.talp"),
            os.path.join(output_dir, "forward.talp"),
        )
    if alignment_direction == "reverse" or alignment_direction == "combine":
        os.rename(
            os.path.join(reverse_dir, "reverse.talp"),
            os.path.join(output_dir, "reverse.talp"),
        )
    if alignment_direction == "combine":
        print("Combining directions with the grow-diag-final-and method...")
        forward_file = os.path.join(output_dir, "forward.talp")
        reverse_file = os.path.join(output_dir, "reverse.talp")
        output_file = os.path.join(output_dir, "grow_diag_final-and.talp")

        combine_command: str = (
            f"{quote(atools_executable)} "
            f"-i {quote(forward_file)} "
            f"-j {quote(reverse_file)} "
            f"-c grow-diag-final-and "
            f"> {quote(output_file)}"
        )

        run_bash_command(combine_command)
