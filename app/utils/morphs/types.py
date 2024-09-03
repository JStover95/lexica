from mecab import Morpheme

# Sorted from most commonly occurring to least
morph_types = {
    "common noun": lambda pos: pos.startswith("NNG"),
    "nominal postposition": lambda pos: pos[0:3] in ["JKS", "JKC", "JKG", "JKO"],
    "verb": lambda pos: pos.startswith("VV"),
    "ending": lambda pos: pos[0:2] in ["EC", "ET"],
    "symbol": lambda pos: pos.startswith("S") and pos[1] not in ["F"],
    "verbial postposition": lambda pos: pos[0:3] in ["JKB", "JKV", "JKQ"],
    "sentence-final punctuation": lambda pos: pos.startswith("SF"),
    "verb suffix": lambda pos: pos.startswith("XSV"),
    "adjective suffix": lambda pos: pos.startswith("XSA"),
    "auxiliary": lambda pos: pos.startswith("JX"),
    "adverb": lambda pos: pos.startswith("MA"),
    "dependent noun": lambda pos: pos.startswith("NNB") and not pos.startswith("NNBC"),
    "number": lambda pos: pos.startswith("SN"),
    "sentence-final ending": lambda pos: pos[0:2] in ["EP", "EF"],
    "adjective": lambda pos: pos.startswith("VA"),
    "noun suffix": lambda pos: pos.startswith("XSN"),
    "auxiliary verb": lambda pos: pos.startswith("VX"),
    "determiner": lambda pos: pos.startswith("MM"),
    "proper noun": lambda pos: pos.startswith("NNP"),
    "prefix": lambda pos: pos.startswith("XP"),
    "conjunction": lambda pos: pos.startswith("JC"),
    "copula": lambda pos: pos.startswith("VC"),
    "pronoun": lambda pos: pos.startswith("NP"),
    "counting noun": lambda pos: pos.startswith("NNBC"),
    "numeral": lambda pos: pos.startswith("NR"),
    "interjection": lambda pos: pos.startswith("IC"),
    "root": lambda pos: pos.startswith("XR"),
    "unknown": lambda pos: pos[0:2] in ["UN", "NA"]
}

# Morphemes to always skip when parsing text
exclude_general = [
    "symbol",
    "sentence-final punctuation",
    "number",
    "copula",
    "unknown"
]

# Morphemes to exclude when querying the dictionary
exclude_dictionary = [
    "nominal postposition",
    "ending",
    "symbol",
    "verbial postposition",
    "sentence-final punctuation",
    "auxiliary",
    "number",
    "sentence-final ending",
    "noun suffix",
    "conjunction",
    "copula",
    "unknown"
]

# Morphemes that do not contain meaning in isolation or are not used in isolation
dependent_types = [
    "nominal postposition",
    "ending",
    "verbial postposition",
    "verb suffix",
    "adjective suffix",
    "auxiliary",
    "dependent noun",
    "sentence-final ending",
    "auxiliary verb",
    "conjunction"
]


def is_morph_type(morph: Morpheme | str, types: list[str] | str) -> bool:
    """
    Determine whether a given Morpheme or part of speech tag is a morpheme type.
    A string or list of strings can be passed to `types`. Returns True if the
    Morpheme or part of speech tag matches one of the morpheme types and False
    otherwise.

    Possible morpheme types are:
        - common noun
        - nominal postposition
        - verb
        - ending
        - symbol
        - verbial postposition
        - sentence-final punctuation
        - verb suffix
        - adjective suffix
        - auxiliary
        - adverb
        - dependent noun
        - number
        - sentence-final ending
        - adjective
        - noun suffix
        - auxiliary verb
        - determiner
        - proper noun
        - prefix
        - conjunction
        - copula
        - pronoun
        - counting noun
        - numeral
        - interjection
        - root
        - unknown

    Args:
        - morph (Morpheme | str): The Morpheme or part of speech tag to check.
        - types (list[str] | str): One or more morpheme types.
    """
    if type(morph) is Morpheme:
        pos = morph.pos
    else:
        pos = morph

    if type(types) is list:
        return any(map(lambda x: morph_types[x](pos), types))
    else:
        return morph_types[types](pos)


def get_morph_type(morph: Morpheme) -> str:
    """
    Get the morpheme type of a given Morpheme.

    Args:
        - morph (Morpheme): The Morpheme to get the type of

    Returns:
        - str: The morpheme type

    Raises:
        - ValueError: If the Morpheme part of speech tag is not found
    """
    if type(morph) is Morpheme:
        pos = morph.pos
    else:
        pos = morph

    for key, function in morph_types.items():
        if function(pos):
            return key

    raise ValueError("Morph pos not found: %s" % str(pos))
