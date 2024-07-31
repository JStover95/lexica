from itertools import groupby

from l2ai.collections import DictionaryEntry, dictionary_entries, senses
from l2ai.extensions import mecab
from l2ai.utils.morphs.parse import get_morph_surface
from l2ai.utils.morphs.types import exclude_dictionary, is_morph_type


type QueryResult = dict[str, list[DictionaryEntry]]


def get_query_str(
        query: str,
        context: str | None = None,
        punctuation: bool = False
    ) -> list[str]:  # TODO: duplicate verbs with suffixes
    """Get keys for querying the dictionary and the parts of speech of each key,
    as they are labeled in the dictionary. These keys are the dictionary forms
    of each word in query. When a word contains suffixes (e.g., auxiliary
    verbs), both are returned. Parts of speech are returned to help
    differentiate between homonyms. Compound words are not included. A sentence
    containing the query can be passed as context if the query's meaning is
    dependent on context. Keys are returned in the order they appear in query
    and without duplicates removed.

    Args:
        query (str)
        context (str | None, optional): An optional sentence that contains query
            for cases when the meaning of query depends on context. Defaults to
            None.
        punctuation (bool, optional): Whether to include sentence-final
            punctuation as a key. This is useful for determining queries that
            span multiple sentences.

    Returns:
        Tuple[list[str], list[str]]: A (keys, parts of speech) tuple.
    """

    # if there is context, use the start and end indices of the query
    if context is not None:
        start = context.index(query)
        end = start + len(query)
        morphs = mecab.parse(context)

    else:
        start = 0
        end = len(query)
        morphs = mecab.parse(query)

    result: list[str] = []
    prefix: str | None = None

    for morph in morphs:
        if start > morph.span.start:
            continue

        if morph.span.end > end:
            break

        if (
            punctuation and
            is_morph_type(morph, "sentence-final punctuation")
        ):
            pass

        # skip morphemes that are excluded from the dictionary
        elif is_morph_type(morph, exclude_dictionary):
            continue

        surface = get_morph_surface(morph)

        # prepend prefixes and roots to this morpheme
        if prefix is not None:
            surface = prefix[0] + surface

        # prepend prefixes and roots to the next morpheme
        if is_morph_type(morph, ["prefix", "root"]):
            prefix = surface
            continue

        # append verb and adjective suffixes with "다" ending
        if is_morph_type(morph, ["verb suffix", "adjective suffix"]):
            try:

                # append to prefixes and roots that were not appended to result
                if prefix:
                    surface = surface + "다"
                
                # append to the last element in result
                else:
                    result[-1] = result[-1] + surface + "다"
                    continue

            # if there is no prefix or root and no morphemes appended to result
            except IndexError:
                surface = surface + "다"

        # append noun suffixes to the last element in result if not already
        # appended to a prefix or root
        if is_morph_type(morph, "noun suffix"):
            try:
                if not prefix:
                    result[-1] = result[-1] + surface
                    continue

            except IndexError:
                pass

        # append "다" ending to verbs and ajectives
        if is_morph_type(morph, ["verb", "adjective", "auxiliary verb"]):
            surface = surface + "다"

        result.append(surface)
        prefix = None

    if result or prefix:
        result = result or [prefix]

    return " ".join(result)


def query_dictionary(query: str) -> list[list[DictionaryEntry]]:
    """Query the dictionary for all words, idioms, or proverbs in a string.
    Dictionary entries are only retured if all of at least one of the entry's
    variations is found in the query string. This is done by checking that the
    query string contains at least one element of each entry's "queryStr" field.
    Synonyms are sorted and grouped together in nested lists. For example:

    [
        [
            DictionaryEntry(variations=["가다"], ...)
            DictionaryEntry(variations=["가다"], ...)
        ],
        [
            DictionaryEntry(variations=["나다"], ...)
        ],
        [
            DictionaryEntry(variations=["하다"], ...)
            DictionaryEntry(variations=["하다"], ...)
        ]
    ]

    Args:
        query (str)

    Returns:
        list[list[DictionaryEntry]]
    """

    qstr = get_query_str(query, punctuation=True)
    result: DictionaryEntry = dictionary_entries.find(
        {"$text": {"$search": qstr}}).sort({"writtenForm": 1}
    )

    in_qstr = lambda x: x in qstr
    entries = filter(lambda x: any(map(in_qstr, x["queryStrs"])), result)

    for entry in entries:
        entry["senses"] = senses.find({"dictionaryEntryId": entry["_id"]})

    groups = groupby(entries, lambda x: x["writtenForm"])

    return [list(v) for _, v in groups]
