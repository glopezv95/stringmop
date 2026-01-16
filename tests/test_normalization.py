from stringmop.normalization import normalize

class TestNormalize:

    val = ' Jamó_n \tSerra%no  \n'

    def test_empty(self) -> None:
        assert normalize('') == ''

    def test_default(self) -> None:
        assert normalize(self.val) == 'jamo_n serra%no'

    def test_uppercase_explicit(self) -> None:
        assert normalize(self.val, to_uppercase=True) == 'JAMO_N SERRA%NO'
        assert normalize(self.val, to_uppercase=False) == 'jamo_n serra%no'

    def test_repl_whitespace_explicit(self) -> None:
        assert (
            normalize(self.val, repl_whitespace=True)
            == 'jamo_n serra%no'
        )
        assert (
            normalize(self.val, repl_whitespace=False)
            =='jamo_n \tserra%no'
        )

    def test_keep_only_aplhanumeric_explicit(self) -> None:
        assert (
            normalize(self.val, keep_only_alphanumeric=False)
            == 'jamo_n serra%no'
        )
        assert (
            normalize(self.val, keep_only_alphanumeric=True)
            == 'jamon serrano'
        )