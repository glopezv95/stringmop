from rapidfuzz.process import extractOne
from collections.abc import Sequence
from typing import Optional

from stringmop.normalization import normalize
from stringmop.types import FuzzExtraction, FuzzExtractions

def _extract_one(
        str_src: str,
        strs_repl: Sequence[str],
        score_cutoff: float
        ) -> tuple[Optional[str], float, int]:
    """
    Apply rapidfuzz.process.extractOne fuzzy to a string to replace it with the closest match
    from a replacement list.

    Parameters
    ----------
    strs_src : str
        The string to be matched and potentially replaced.
    strs_repl : Sequence[str]
        A sequence of candidate strings used for replacement.
    score_cutoff : float
        Minimum similarity score (0.0-100.0) required to consider a match valid.
        Default is 90.0.

    Returns
    -------
    tuple[Optional[str], float, int]
        Tuple containing the replacement string, the similarity score, and the index of the replacement.
    """
    return extractOne(str_src, strs_repl, processor=normalize, score_cutoff=score_cutoff) or (None, 0, -1)

def _build_fuzz_extraction(str_src: str, extraction: tuple[Optional[str], float, int]) -> FuzzExtraction:
    """
    Convert a rapidfuzz.process.extractOne extraction to a stringmop.types.FuzzExtraction object.

    Parameters
    ----------
    str_src : str
        The string to be assinged to stringmop.types.FuzzExtraction.str_src.
    extraction: tuple[Optional[str], float, int]
        The rapidfuzz.process.extractOne extraction.

    Returns
    -------
    stringmop.types.FuzzExtraction
        Tuple containing the replacement string, the similarity score, and the index of the replacement.
    """
    str_repl, score, _ = extraction
    
    return FuzzExtraction(str_src=str_src, str_repl=str_repl, score=score)

def fuzz_replace(
        strs_src: Sequence[str],
        strs_repl: Sequence[str],
        score_cutoff: float = 90.0
        ) -> FuzzExtractions:
    """
    Perform fuzzy string matching to replace source strings with the closest matches 
    from a replacement list.

    Parameters
    ----------
    strs_src : Sequence[str]
        A sequence of strings to be matched and potentially replaced.
    strs_repl : Sequence[str]
        A sequence of candidate strings used for replacement.
    score_cutoff : float, optional
        Minimum similarity score (0.0-100.0) required to consider a match valid.
        Default is 90.0.

    Returns
    -------
    stringmop.types.FuzzExtractions
        Object containing a list of stringmop.typesFuzzExtraction objects.
    
    Examples
    --------
    >>> strs_src = ["apple", "bannana", "cherry"]
    >>> strs_repl = ["apple", "banana", "cherry"]
    >>> fuzz_replace(strs_src, strs_repl)
    FuzzExtractions(
        strs_src=['apple', 'bannana', 'cherry'],
        strs_repl=['apple', 'banana', 'cherry'],
        scores=[100, 92, 100]
    )
    """
    rapidfuzz_extractions = [
        _extract_one(str_src=str_src, strs_repl=strs_repl, score_cutoff=score_cutoff)
        for str_src in strs_src
    ]
    extractions = [
        _build_fuzz_extraction(str_src=strs_src[i], extraction=extraction)
        for i, extraction in enumerate(rapidfuzz_extractions)
    ]

    return FuzzExtractions(extractions=extractions)