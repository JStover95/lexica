from typing import Any

def b(s: Any) -> str:
    return "\033[94m%s\033[0m" % s


def g(s: Any) -> str:
    return "\033[92m%s\033[0m" % s
