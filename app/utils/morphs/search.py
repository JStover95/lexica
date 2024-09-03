from app.extensions import mecab
from app.collections import Content, contents
from app.utils.morphs.parse import get_smap_from_morphs, SurfaceMap, Ix

type ResultMap = tuple[list[str], Ix]
type SearchResults = list[tuple[Content, Ix]]

exclude_surfaces = ["하", "되"]
exclude_words = ["것", "수", "있다", "안", "하다", "되다"]


def quicksort_with_key(
        *args: list,
        low: int | None = None,
        high: int | None = None
    ) -> None:
    """Quicksort two or more lists using the first as the sort key.

    Args:
        low (int | None, optional): Defaults to None.
        high (int | None, optional): Defaults to None.
    
    Raises:
        ValueError: If all lists are not the same length.
    """
    def partition_with_key(*args: list, low: int = 0, high: int = 0) -> int:
        args = list(args)
        list1 = args[0]
        pivot = list1[high]
        i = low - 1

        for j in range(low, high):
            if list1[j] <= pivot:
                i += 1
                list1[i], list1[j] = list1[j], list1[i]

                for l in args[1:]:
                    l[i], l[j] = l[j], l[i]

        list1[i + 1], list1[high] = list1[high], list1[i + 1]

        for l in args[1:]:
            l[i + 1], l[high] = l[high], l[i + 1]

        return i + 1

    args = list(args)
    list1 = args[0]

    if any(map(lambda x: len(list1) != len(x), args[1:])):
        raise ValueError("All lists must be equal length")

    if low is None:
        low = 0
    if high is None:
        high = len(list1) - 1

    if low < high:
        pivot_index = partition_with_key(*args, low=low, high=high)
        quicksort_with_key(*args, low=low, high=pivot_index - 1)
        quicksort_with_key(*args, low=pivot_index + 1, high=high)


def get_rmap(qsmap: SurfaceMap, qentry: Content, key: str) -> ResultMap:
    """Get the result map of all units or modifiers in a query that are found in
    a database entry. Whether this is performed on units or modifiers is
    determined by the key parameter.

    Surface maps stored in the database contain a list of indices for each
    unique unit or modifier. Result maps are a list of indices for every
    occurence of a unit or modifier.

    Args:
        qsmap (SurfaceMap): The SurfaceMap of the query, for either units or
            modifiers depending on the key parameter
        qentry (Content): The database entry
        key (str): "units" or "modifiers"

    Returns:
        ResultMap
    """
    result: ResultMap = [[], []]
    surfaces = qentry["surfaces"][key]
    ix = qentry["ix"][key]

    i = 0
    for surface in qsmap["surfaces"]:
        while i < len(surfaces) and surfaces[i] < surface:
            i += 1
        if i == len(surfaces):
            continue

        if surfaces[i] == surface:
            result[0].extend([surface] * len(ix[i]))
            result[1].extend(ix[i])

    return result


def get_search_results(
        qunits: SurfaceMap,
        qmodfs: SurfaceMap,
        qresult: list[Content]
    ) -> SearchResults:
    """Get search results from a database query. Search results are a list of
    (indices, Content) tuples, where indices represent the locations of all
    matches in the database entry for each search result.

    The final search results are sorted by relevance: first by the total number
    of matches in each result, then by the longest match in each result.

    By default, this function ignores certain common words (하다, 되다, etc.)
    except when the query contains only these common words.

    Args:
        qunits (SurfaceMap): The units surface map of the query
        qmodfs (SurfaceMap): The modifiers surface map of the query
        qresult (list[Content]): The result of a database query

    Returns:
        SearchResults: A list of (Content, indidices) tuples, where
            each tuple is a search result. Indices indicate the location of all
            matches in the database entry.
    """
    result = []

    for qentry in qresult:

        # get the surface maps of all found units and modifiers
        urmap = get_rmap(qunits, qentry, "units")
        mrmap = get_rmap(qmodfs, qentry, "modifiers")
        quicksort_with_key(urmap[1], urmap[0])
        quicksort_with_key(mrmap[1], mrmap[0])

        # if units were found
        if len(urmap[1]):

            # append modifier indices to adjacent unit indices
            i = 0
            for ix in mrmap[1]:
                while i < len(urmap[1]) and urmap[1][i][1] < ix[0]:
                    i += 1
                if i < len(urmap[1]) and urmap[1][i][1] == ix[0]:
                    urmap[1][i][1] = ix[1]
            rmap = urmap

        # else if only modifiers were queried
        elif not len(qunits["ix"]):
            rmap = mrmap

        # else if any units were queried and none were found
        else:
            continue

        # force to include excluded words if all queried units are excluded
        force_include = []
        if all(map(lambda x: x in exclude_surfaces, qunits["surfaces"])):
            force_include = qunits["surfaces"]

        # remove force included words from excluded words if any
        if force_include:
            exclude = [s for s in exclude_surfaces if not s in force_include]
        else:
            exclude = exclude_surfaces

        # remove exluded words from the result
        i = 0
        to_append = []
        while i < len(rmap[0]):
            if rmap[0][i] not in exclude:
                to_append.append(rmap[1][i])
            i += 1

        if to_append:
            result.append((qentry, to_append))

    return result


def query_content(qunits: SurfaceMap, qmodfs: SurfaceMap) -> list[Content]:
    """Query database contents. Queries are only performed using units. If no
    units are passed, then the query will be performed using modifiers.

    Args:
        qunits (SurfaceMap): Units SurfaceMap of the query
        qmodfs (SurfaceMap): Modifiers SurfaceMap of the query

    Returns:
        list[Content]
    """
    if qunits["surfaces"]:
        query = qunits["surfaces"]
        key = "units"

    else:
        query = qmodfs["surfaces"]
        key = "modifiers"

    return list(contents.find({"surfaces.%s" % key: {"$in": query}}))


def get_query_content_results(query: str) -> SearchResults:
    qmorphs = mecab.parse(query)
    qunits, qmodfs = get_smap_from_morphs(qmorphs)
    qresult = query_content(qunits, qmodfs)
    return get_search_results(qunits, qmodfs, qresult)
