from typing import Tuple

from l2ai.collections import Content, contents, DictionaryEntry
from l2ai.utils.types import SurfaceMap

type Ix = list[list[int]]
type ResultMap = tuple[list[str], Ix]
type QueryResult = dict[str, list[DictionaryEntry]]
type InferenceResult = dict[str, list[Tuple[float, str]]]
type SearchResults = list[Tuple[Ix, Content]]

exclude_surfaces = ["하", "되"]
exclude_words = ["것", "수", "있다", "안", "하다", "되다"]


def group_adjacent_ix(
        rmap: ResultMap,
        include: list[str] | None = None
    ) -> list[Ix]:
    """Group adjacent indices in a result map. Indices that are directly
    adjacent (separated by 1 character or less) are combined into a single pair
    of indices. Indices that are adjacent (separated by less than 20 characters)
    are grouped into a set of indices.

    By default, common surfaces (e.g., 하, 되) are excluded unless their indices
    are directly adjacent to another pair of indices. This behavior can be
    overridden by passing a list of surfaces to include.

    Args:
        rmap (ResultMap)
        include (list[str] | None, optional): Surfaces to include, overriding
            the default behavior of excluding common surfaces. Defaults to None.

    Returns:
        list[Ix]: Sets of indices grouped by adjacency
    """

    # get surfaces to exclude
    if include is None:
        exclude = exclude_surfaces
    else:
        exclude = [s for s in exclude_surfaces if not s in include]

    # skip excluded surfaces to get the first indices
    i = 0
    while i < len(rmap[0]) and rmap[0][i] in exclude:
        i = i + 1

    if i == len(rmap[0]):
        return []

    result: list[Ix] = [[rmap[1][i]]]
    i = i + 1

    while i < len(rmap[1]):

        # if these indices are directly adjacent to the previous indices
        if rmap[1][i][0] - result[-1][-1][1] < 2:

            # combine the two indices and continue
            result[-1][-1][1] = rmap[1][i][1]
            i = i + 1

        else:

            # if this surface is not excluded
            if rmap[0][i] not in exclude:

                # if these indices are adjacent to the previous indices
                if rmap[1][i][0] - result[-1][-1][1] < 20:

                    # append these indices to the previous set of indices
                    result[-1].append(rmap[1][i])

                else:

                    # append these indices as a new set of indices
                    result.append([rmap[1][i]])

            i = i + 1

    return result


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
            i = i + 1
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
        SearchResults: A list of (indices, Content) tuples, where
            each tuple is a search result. Indices indicate the location of all
            matches in the database entry.
    """
    result: list[Ix] = []

    for qentry in qresult:

        # get the surface maps of all found units and modifiers
        urmap = get_rmap(qunits, qentry, "units")
        mrmap = get_rmap(qmodfs, qentry, "modifiers")
        quicksort_with_key(urmap[1], urmap[0])
        quicksort_with_key(mrmap[1], mrmap[0])

        include = None

        # force to include excluded words if all queried units are excluded
        if all(map(lambda x: x in exclude_surfaces, qunits["surfaces"])):
            include = qunits["surfaces"]

        # if units were found
        if len(urmap[1]):

            # append modifier indices to adjacent unit indices
            i = 0
            for ix in mrmap[1]:
                while i < len(urmap[1]) and urmap[1][i][1] < ix[0]:
                    i = i + 1
                if i < len(urmap[1]) and urmap[1][i][1] == ix[0]:
                    urmap[1][i][1] = ix[1]

            # group adjacent indices of the combined units and modifiers
            grouped = group_adjacent_ix(urmap, include)
            result.extend([(ix, qentry) for ix in grouped])

        # else if only modifiers were queried
        elif not len(qunits["ix"]):

            # group adjacent indices of only modifiers
            grouped = group_adjacent_ix(mrmap, include)
            result.extend([(ix, qentry) for ix in grouped])

        # else if any units were queried and none were found
        else:
            continue

    # sort by the largest number of matches
    by_sum = lambda x: sum(map(lambda y: y[1] - y[0], x[0]))
    result = sorted(result, key=by_sum, reverse=True)

    # sort by the longest match
    by_max = lambda x: max(map(lambda y: y[1] - y[0], x[0]))
    result = sorted(result, key=by_max, reverse=True)

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
