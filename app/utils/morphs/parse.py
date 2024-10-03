import re
from typing import Tuple, TypedDict

from mecab import Morpheme

from app.extensions import mecab
from app.utils.morphs.types import (
    exclude_general,
    dependent_types,
    is_morph_type
)

type Ix = list[list[int]]


class SurfaceMap(TypedDict):
    surfaces: list[str]
    ix: list[Ix]


def get_morph_surface(morph: Morpheme) -> str:
    """Get the surface of a morpheme. This includes all parts of compound words
    and the first part of inflects. 거 (dependent noun) is replaced with 것.

    Args:
        morph (Morpheme): The morpheme to get the surface from.

    Returns:
        str: The morpheme's surface.
    """
    if morph.feature.type == "Compound":
        s = re.sub(r"[A-Z{2,3}*+]|(?<=\/).+?\+", "", morph.feature.expression)
        return s.replace("//", "")

    elif morph.feature.type == "Inflect":
        return morph.feature.expression.split("/")[0]

    elif is_morph_type(morph, "dependent noun") and morph.surface == "거":
        return "것"

    return morph.surface


def get_surface_ix_from_smap(surface: str, smap: SurfaceMap) -> int:
    """Get the index of a surface from a surface map.

    Args:
        surface (str)
        smap (SurfaceMap)

    Raises:
        ValueError: If the surface is not found

    Returns:
        int
    """
    i = 0
    while i < len(smap["surfaces"]) and smap["surfaces"][i] < surface:
        i = i + 1

    if i < len(smap["surfaces"]) and smap["surfaces"][i] == surface:
        return i

    else:
        raise ValueError


def get_smap_from_morphs(
        morphs: list[Morpheme]
    ) -> Tuple[SurfaceMap, SurfaceMap]:
    """Get the surface map of all units and modifiers from a list of morphemes.
    Units are morphemes that are independent units of meaning (e.g., nouns
    verbs, etc.). Modifiers are morphemes that are not (e.g., particles,
    suffixes, etc.)

    Args:
        morphs (list[Morpheme])

    Returns:
        Tuple[SurfaceMap, SurfaceMap]: A (unit_smap, modf_smap) tuple containing
            the surface maps of all units and modifiers
    """
    unit_smap: SurfaceMap = {"surfaces": [], "ix": []}
    modf_smap: SurfaceMap = {"surfaces": [], "ix": []}
    morphs = sorted(morphs, key=lambda x: x.surface)

    for i, morph in enumerate(morphs):
        surface = get_morph_surface(morph)

        # skip excluded morpheme types
        if is_morph_type(morph, exclude_general):
            continue

        # select whether surface map is a unit or modifier surface map
        if is_morph_type(morph, dependent_types):
            smap = modf_smap
        else:
            smap = unit_smap

        # append the surface and index
        try:
            i = get_surface_ix_from_smap(surface, smap)
            smap["ix"][i].append([morph.span.start, morph.span.end])

        except ValueError:
            smap["surfaces"].append(surface)
            smap["ix"].append([[morph.span.start, morph.span.end]])

    return unit_smap, modf_smap


def highlight_substrings(s: str, indices: list[list[int]]) -> list[dict]:
    """
    Extracts the sentences containing specified highlighted substrings from a
    given string `s` and returns the sentence along with the adjusted start and
    stop indices of the highlight within each sentence.

    This function identifies sentence boundaries using common sentence-ending
    punctuation (., !, ?), and ensures that the left side of the context starts
    from the beginning of the sentence containing the highlighted substring.

    Args:
        - s (str): The input string containing the text.
        - indices (list[list[int]]): A list of [start, stop] index pairs
        representing the substrings to highlight.  Both `start` and `stop` are
        inclusive indices referring to positions in `s`.

    Returns:
        - list[dict]: A list of dictionaries, where each dictionary has the
        following structure:
            - text (str): The sentence containing the highlighted substring.
            - start (int): The start index of the highlighted substring within
            the sentence.
            - stop (int): The stop index of the highlighted substring within the
            sentence.
    
    Example:
        s = "Hello world! This is an example sentence. Another one?"
        indices = [[0, 4], [13, 16]]
        highlight_substrings(s, indices)
        
        Output:
        [
            {"text": "Hello world!", "start": 0, "stop": 4},
            {"text": "This is an example sentence.", "start": 0, "stop": 3}
        ]
    
    Notes:
        - The function assumes that the input string `s` is well-formed and
        sentences are delimited by '.', '!', or '?'.
        - It skips any spaces or quotation marks immediately following
        sentence-ending punctuation.
        - If no sentence-ending punctuation is found before the start of a
        highlight, it considers the sentence to start at the beginning of the
        string.
        - If no sentence-ending punctuation is found after the end of a
        highlight, it considers the sentence to end at the end of the string.
    """
    results = []
    
    # Regular expression to match sentence-ending punctuation: ., !, ?
    sentence_endings = re.compile(r"[.!?]")
    
    for start, stop in indices:
        # Find the start of the sentence by searching backwards for the last sentence-ending punctuation
        sentence_start_matches = list(sentence_endings.finditer(s, 0, start))
        if sentence_start_matches:
            sentence_start = sentence_start_matches[-1].end()
        else:
            sentence_start = 0
        
        # Skip any spaces or quotes after the sentence start
        while (
            sentence_start < len(s) and
            (s[sentence_start] == " " or s[sentence_start] == "\"")
        ):
            sentence_start += 1

        # Find the end of the sentence by searching forwards for the next sentence-ending punctuation
        sentence_end_match = sentence_endings.search(s, stop)
        if sentence_end_match:
            sentence_end = sentence_end_match.end()
        else:
            sentence_end = len(s)

        # Skip any quotes at the sentence end
        while sentence_end < len(s) and s[sentence_end] == "\"":
            sentence_end += 1

        # Extract the sentence containing the highlight
        sentence = s[sentence_start:sentence_end]

        # Calculate the adjusted start and stop indices for the substring in the sentence
        adjusted_start = start - sentence_start
        adjusted_stop = stop - sentence_start

        results.append({
            "text": sentence,
            "start": adjusted_start,
            "stop": adjusted_stop
        })

    return results
