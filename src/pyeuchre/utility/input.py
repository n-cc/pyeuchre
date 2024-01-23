"""Classes and functions pertaining to parsing input."""


def parse_bool(s: str) -> bool:
    """Parses input for a yes or no question.

    Args:
        s (str): Input to parse.
    """
    return s.lower() in ["y", "yes"]
