from typing import TypedDict

type Ix = list[list[int]]


class SurfaceMap(TypedDict):
    surfaces: list[str]
    ix: list[Ix]
