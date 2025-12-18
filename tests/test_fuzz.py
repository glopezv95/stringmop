from stringmop.fuzz import _extract_one, _build_fuzz_extraction, fuzz_replace
from stringmop.types import FuzzExtractions, FuzzExtraction

class TestExtractOne:

    score_cutoff = 90.0

    def test_empty(self) -> None:
        assert _extract_one(str_src='', strs_repl=[], score_cutoff=self.score_cutoff) == (None, 0, -1)

    def test_generic_correct(self) -> None:
        str_src = 'Jamón Serpano'
        strs_repl = ['jamon \nserrano', 'judías verde   ']
        result, _, _ = _extract_one(str_src=str_src, strs_repl=strs_repl, score_cutoff=self.score_cutoff)

        assert result == ('jamon \nserrano')

    def test_generic_incorrect(self) -> None:
        str_src = 'Jamón Serpano'
        strs_repl = ['Fish and Chips', 'Papas Arrugás']
        result, _, _ = _extract_one(str_src=str_src, strs_repl=strs_repl, score_cutoff=self.score_cutoff)

        assert result is None

    def test_processor(self) -> None:
        str_src = 'Jamón Serrano'
        strs_repl = ['Jamon Serrana', 'jamon serrano']
        result, _, _ = _extract_one(str_src=str_src, strs_repl=strs_repl, score_cutoff=self.score_cutoff)

        assert result == 'jamon serrano'

    def test_cutoff(self) -> None:
        str_src = 'Jamón Serpano'
        strs_repl = ['Fish and Chips', 'Papas Arrugás']
        result, _, _ = _extract_one(str_src=str_src, strs_repl=strs_repl, score_cutoff=10.0)

        assert result == 'Papas Arrugás'

class TestBuildExtraction:

    str_src = 'Jamón Serpano'

    def test_empty(self) -> None:
        result = _build_fuzz_extraction(str_src='', extraction=('', 0, -1))

        assert isinstance(result, FuzzExtraction)
        assert result.str_src == ''
        assert result.str_repl == ''
        assert result.score == 0

    def test_generic_correct(self) -> None:
        strs_repl = ['jamon \nserrano', 'judías verde   ']
        extraction = _extract_one(str_src=self.str_src, strs_repl=strs_repl, score_cutoff=90.0)
        result = _build_fuzz_extraction(str_src='Jamón Serpano', extraction=extraction)

        assert result.str_src == self.str_src
        assert result.str_repl == 'jamon \nserrano'

    def test_generic_incorrect(self) -> None:
        strs_repl = ['Fish and Chips', 'Papas Arrugás']
        extraction = _extract_one(str_src=self.str_src, strs_repl=strs_repl, score_cutoff=90.0)
        result = _build_fuzz_extraction(str_src='Jamón Serpano', extraction=extraction)

        assert result.str_src == self.str_src
        assert result.str_repl == None

class TestFuzzReplace:

    def test_empty(self) -> None:
        result = fuzz_replace(strs_src=[], strs_repl=[])

        assert isinstance(result, FuzzExtractions)
        assert result.extractions == []

    def test_generic(self) -> None:
        strs_src = ['Jamón Serpano', '  JUDÍAS \tverdes']
        strs_repl = ['Jamón Serrano', 'Papas Arrugás']
        result = fuzz_replace(strs_src=strs_src, strs_repl=strs_repl)

        assert [ext.str_src for ext in result.extractions] == strs_src
        assert [ext.str_repl for ext in result.extractions] == ['Jamón Serrano', None]

    def test_generic_correct(self) -> None:
        strs_src = ['Jamón Serpano', '  JUDÍAS \tverdes']
        strs_repl = ['jamon \nserrano', 'judías verde   ']
        result = fuzz_replace(strs_src=strs_src, strs_repl=strs_repl)

        assert [ext.str_src for ext in result.extractions] == strs_src
        assert [ext.str_repl for ext in result.extractions] == strs_repl

    def test_generic_incorrect(self) -> None:
        strs_src = ['Jamón Serpano', '  JUDÍAS \tverdes']
        strs_repl = ['Fish and Chips', 'Papas Arrugás']
        result = fuzz_replace(strs_src=strs_src, strs_repl=strs_repl)

        assert [ext.str_src for ext in result.extractions] == strs_src == strs_src
        assert [ext.str_repl for ext in result.extractions] == [None, None]

    def test_processor(self) -> None:
        strs_src = ['Jamón Serrano']
        strs_repl = ['Jamon Serrana', 'jamon serrano']
        result = fuzz_replace(strs_src=strs_src, strs_repl=strs_repl)

        assert [ext.str_src for ext in result.extractions] == strs_src
        assert [ext.str_repl for ext in result.extractions] == ['jamon serrano']

    def test_cutoff(self) -> None:
        strs_src = ['Jamón Serpano', '  JUDÍAS \tverdes']
        strs_repl = ['Fish and Chips', 'Papas Arrugás']
        result = fuzz_replace(strs_src=strs_src, strs_repl=strs_repl)
        result_cutoff = fuzz_replace(strs_src=strs_src, strs_repl=strs_repl, score_cutoff=10.0)

        assert [ext.str_src for ext in result.extractions] == strs_src
        assert [ext.str_repl for ext in result.extractions] == [None, None]

        assert [ext.str_src for ext in result_cutoff.extractions] == strs_src
        assert [ext.str_repl for ext in result_cutoff.extractions] == ['Papas Arrugás', 'Papas Arrugás']