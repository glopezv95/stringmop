from unidecode import unidecode
import re

def normalize(
        str_src: str,
        to_uppercase: bool = False,
        repl_whitespace: bool = True,
        keep_only_alphanumeric: bool = False
        ) -> str:
    """
    Converts an input string to uppercase or lowercase, strips whitespace characters, 
    and transliterates it to an ASCII string.

    Parameters
    ----------
    str_src : str
        The source string to normalize.
    to_uppercase : bool, optional
        If True, the output string is converted to uppercase. If False, the string 
        is converted to lowercase. Default is True.
    repl_whitespace : bool, optional
        If True, all whitespace sequences are replaced with a single space " ". 
        Default is True.
    keep_only_alphanumeric : bool, optional
        If True, all non-alphanumeric characters except whitespaces are removed. 
        Default is False.

    Returns
    -------
    str
        The normalized string.

    Examples
    --------
    >>> normalize_string(" Héllo \tWórld! ", to_uppercase=True)
    'HELLO WORLD!'

    >>> normalize_string(" Héllo  \tWórld! ", repl_whitespace=False)
    'hello  \tworld!'
    """
    str_dst = unidecode(str_src)
    str_dst = str_dst.upper() if to_uppercase else str_dst.lower()
    str_dst = (
        re.sub(r'\s+', ' ', str_dst.strip())
        if repl_whitespace
        else str_dst.strip()
    )
    if keep_only_alphanumeric:
        str_dst = re.sub(r'[^a-zA-Z0-9\s]', '', str_dst)

    return str_dst