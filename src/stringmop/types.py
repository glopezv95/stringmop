from dataclasses import dataclass
from typing import Optional
from collections.abc import Sequence

@dataclass
class FuzzExtraction:
    """
    Stores the result of a stringmop.fuzz.fuzz_replace string replacement.

    Attributes
    ----------
    str_src : str
        Original input string.
    str_repl : Optional[str]
        Best-matched replacement for the input string, or None if no match.
    score : float
        Similarity score between str_src and str_repl (0.0–100.0).
    """
    str_src: str
    str_repl: Optional[str]
    score: float

@dataclass
class FuzzExtractions:
    """
    Stores the results of fuzzy string replacements.

    Attributes
    ----------
    extractions: Sequence[stringmop.types.FuzzExtraction]
        Sequence of extractions.
    """
    extractions: Sequence[FuzzExtraction]