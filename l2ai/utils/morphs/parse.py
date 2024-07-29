import re
from typing import Tuple

from mecab import Morpheme

from l2ai.extensions import mecab
from l2ai.utils.morphs.types import (
    exclude_general,
    dependent_types,
    is_morph_type
)
from l2ai.utils.types import SurfaceMap


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
