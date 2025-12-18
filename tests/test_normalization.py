from stringmop.normalization import normalize

class TestNormalize:

    val = ' Jamón \tSerrano  \n'

    def test_empty(self) -> None:
        assert normalize('') == ''

    def test_default(self) -> None:
        assert normalize(self.val) == 'jamon serrano'

    def test_uppercase_explicit(self) -> None:
        assert normalize(self.val, to_uppercase=True) == 'JAMON SERRANO'
        assert normalize(self.val, to_uppercase=False) == 'jamon serrano'

    def test_repl_whitespace_explicit(self) -> None:
        assert normalize(str_src = self.val, repl_whitespace=True) == 'jamon serrano'
        assert normalize(str_src = self.val, repl_whitespace=False) =='jamon \tserrano'