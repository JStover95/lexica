from itertools import groupby

from app.collections import (
    DictionaryEntry,
    DictionaryEntry,
    dictionary_entries,
    senses
)
from app.extensions import mecab
from app.utils.morphs.parse import get_morph_surface
from app.utils.morphs.types import exclude_dictionary, is_morph_type


type QueryResult = dict[str, list[DictionaryEntry]]

# Single common words to not return a dictionary entry for
exclude_words = ["것", "수", "있다", "안", "하다", "되다", ""]


def get_query_str(
        query: str,
        context: str | None = None,
        punctuation: bool = False
    ) -> str:  # TODO: duplicate verbs with suffixes
    """Get a space-separated string of keys for executing a text search against
    dictionary entries in the database. These keys are the dictionary forms of
    each word in query. When a word contains suffixes (e.g., auxiliary verbs),
    both are returned. Compound words are not included. A sentence containing
    the query can be passed as context if the query's meaning is dependent on
    context. Keys are returned in the order they appear in query and without
    duplicates removed.

    Args:
        query (str)
        context (str | None, optional): An optional sentence that contains query
            for cases when the meaning of query depends on context. Defaults to
            None.
        punctuation (bool, optional): Whether to include sentence-final
            punctuation as a key. This is useful for determining queries that
            span multiple sentences.

    Returns:
        str: A space-separated string of keys that can be used for a text search
            against dictionary entries stored in the database
    """

    # If there is context, use the start and end indices of the query
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

        # Skip leading and trailing morphs that were passed as context
        if start > morph.span.start:
            continue

        if morph.span.end > end:
            break

        # Skip sentence final punctuation unless explicitly included
        if (
            punctuation and
            is_morph_type(morph, "sentence-final punctuation")
        ):
            pass

        # Skip morphemes that are excluded from the dictionary
        elif is_morph_type(morph, exclude_dictionary):
            continue

        surface = get_morph_surface(morph)

        # Prepend prefixes and roots to this morpheme
        if prefix is not None:
            surface = prefix[0] + surface

        # Prepend prefixes and roots to the next morpheme
        if is_morph_type(morph, ["prefix", "root"]):
            prefix = surface
            continue

        # Append verb and adjective suffixes with "다" ending
        if is_morph_type(morph, ["verb suffix", "adjective suffix"]):
            try:

                # Append to prefixes and roots that were not appended to result
                if prefix:
                    surface = surface + "다"
                
                # Append to the last element in result
                else:
                    result[-1] = result[-1] + surface + "다"
                    continue

            # If there is no prefix or root and no morphemes appended to result
            except IndexError:
                surface = surface + "다"

        # Append noun suffixes to the last element in result if not already appended to a prefix or root
        if is_morph_type(morph, "noun suffix"):
            try:
                if not prefix:
                    result[-1] = result[-1] + surface
                    continue

            except IndexError:
                pass

        # Append "다" ending to verbs and ajectives
        if is_morph_type(morph, ["verb", "adjective", "auxiliary verb"]):
            surface = surface + "다"

        result.append(surface)
        prefix = None

    # Handle cases when the only query key is a prefix
    if result or prefix:
        result = result or [prefix]

    return " ".join(result)


def query_dictionary(
        query: str,
        context: str | None = None
    ) -> list[list[DictionaryEntry]]:
    """Query the dictionary for all words, idioms, or proverbs in a string.
    Dictionary entries are only retured if at least one of the entry's
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

    qstr = get_query_str(query, context=context, punctuation=True)
    entries: list[DictionaryEntry] = list(dictionary_entries.find(
        {"$text": {"$search": qstr}}).sort({"writtenForm": 1}
    ))

    # Remove entries that are excluded words
    entries_filtered = list(filter(
        lambda entry: any(
            (x in qstr and x not in exclude_words) for x in entry["queryStrs"]
        ),
        entries
    ))

    # Add senses to each entry
    result: list[DictionaryEntry] = []
    for entry in entries_filtered:
        entry["senses"] = list(senses.find({"dictionaryEntryId": entry["_id"]}))
        result.append(entry)

    # Group entries by their first query string, which is always the query string of the writtedForm field
    groups = groupby(result, lambda x: x["queryStrs"][0])
    groups = [list(v) for _, v in groups]

    # Handle cases where the query returns multiple written forms per query key
    result = []
    for group in groups:
        written_forms = []

        # Get all written forms in this group
        for entry in group:
            if entry["writtenForm"] not in written_forms:
                written_forms.append(entry["writtenForm"])

        # Remove written forms that are not in the original query string
        if len(written_forms) > 1:
            group = [entry for entry in group if entry["writtenForm"] in qstr]

        result.append(group)

    return result
