import unittest
from numpy.testing import assert_array_almost_equal

from mckit.parser.mcnp_input_parser import mcnp_input_lexer, mcnp_input_parser
from mckit.parser.meshtal_parser import meshtal_lexer, meshtal_parser
from tests.parser_test_data import lex_ans
from tests.parser_test_data import parser_ans
from tests.parser_test_data import meshtal_ans


class TestLexer(unittest.TestCase):
    def test_lex(self):
        for i, name in enumerate(lex_ans.ans.keys()):
            mcnp_input_lexer.begin('INITIAL')
            with (self.subTest(i=i)):
                with open('tests/parser_test_data/{0}.txt'.format(name)) as f:
                    text = f.read()
                mcnp_input_lexer.input(text)
                for l in lex_ans.ans[name]:
                    if isinstance(l[0], str):
                        t = mcnp_input_lexer.token()
                        #print(t.lineno, t.value)
                        self.assertEqual(l[0], t.type)
                        self.assertEqual(l[1], t.value)
                        self.assertEqual(l[2], t.lineno)
                    else:
                        with self.assertRaises(ValueError) as ex:
                            mcnp_input_lexer.token()
                        msg, sym, line, column = ex.exception.args
                        self.assertEqual(l[1], line)
                        self.assertEqual(l[2], column)


class TestParser(unittest.TestCase):
    def test_parse(self):
        for i, name in enumerate(parser_ans.ans.keys()):
            with (self.subTest(i=i)):
                with open('tests/parser_test_data/{0}.txt'.format(name)) as f:
                    text = f.read()
                mcnp_input_lexer.begin('INITIAL')
                title, cells, surfaces, data = mcnp_input_parser.parse(text, lexer=mcnp_input_lexer)
                ans = parser_ans.ans[name]
                self.assertEqual(title, ans['title'])
                self.assertEqual(cells, ans['cells'])
                self.assertEqual(surfaces, ans['surfaces'])
                self.assertEqual(data, ans['data'])


class TestMeshtalParser(unittest.TestCase):
    def test_parse(self):
        with open('tests/parser_test_data/fmesh.m') as f:
            text = f.read()
        meshtal_lexer.begin('INITIAL')
        tallies = meshtal_parser.parse(text, lexer=meshtal_lexer)
        self.assertEqual(tallies.keys(), meshtal_ans.ans.keys())
        for k in ['date', 'histories', 'title']:
            self.assertEqual(tallies[k], meshtal_ans.ans[k])
        for t, a in zip(tallies['tallies'], meshtal_ans.ans['tallies']):
            for k in ['name', 'particle', 'geom']:
                self.assertEqual(t[k], a[k])
            for k, v in a['bins'].items():
                assert_array_almost_equal(t['bins'][k], v)
            assert_array_almost_equal(t['result'], a['result'])
            assert_array_almost_equal(t['error'], a['error'])


if __name__ == '__main__':
    unittest.main()
