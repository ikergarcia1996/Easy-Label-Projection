import spacy
from spacy.lang.en import English
from spacy.lang.es import Spanish
from spacy.lang.de import German
from spacy.lang.it import Italian
from spacy.lang.nl import Dutch
from spacy.lang.ca import Catalan
from spacy.lang.eu import Basque
from spacy.lang.fr import French
from spacy.lang.ru import Russian
from spacy.lang.tr import Turkish
from spacy.tokenizer import Tokenizer


def get_tokenizer(language: str) -> spacy.tokenizer.Tokenizer:
    if language == "en":
        nlp = English()
    elif language == "es":
        nlp = Spanish()
    elif language == "de":
        nlp = German()
    elif language == "it":
        nlp = Italian()
    elif language == "nl" or language == "ned":
        nlp = Dutch()
    elif language == "cat" or language == "ca":
        nlp = Catalan()
    elif language == "eu":
        nlp = Basque()
    elif language == "fr":
        nlp = French()
    elif language == "ru":
        nlp = Russian()
    elif language == "trk" or language == "tr":
        nlp = Turkish()
    else:
        raise ValueError(
            f"Language {language} not implemented yet."
            f"Available languages: [en,es,de,it,nl,cat,eu,fr,ru,[trk|tr]"
        )

    return nlp.tokenizer


def tokenize2conll(line: str, tokenizer: spacy.tokenizer.Tokenizer) -> str:

    s = "".join(
        [f"{word} O\n" for word in tokenizer(line) if len(str(word).strip()) > 0]
    )
    if len(s) > 0:
        s += "\n"
    return s


def tokenize2text(line: str, tokenizer: spacy.tokenizer.Tokenizer) -> str:
    s = " ".join([str(word) for word in tokenizer(line)]) + "\n"
    return s


def blocks(files, size=65536):
    while True:
        b = files.read(size)
        if not b:
            break
        yield b


def count_lines(input_path: str) -> int:
    with open(input_path, "r", encoding="utf8") as f:
        return sum(bl.count("\n") for bl in blocks(f))
