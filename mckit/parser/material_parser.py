import re
import sly
import mckit.material as mat
from mckit.parser.common.utils import drop_c_comments
import mckit.parser.common.utils as cmn
from mckit.parser.common.Lexer import Lexer as LexerBase


# noinspection PyPep8Naming,PyUnboundLocalVariable,PyUnresolvedReferences,SpellCheckingInspection
class Lexer(LexerBase):
    literals = {':', '(', ')'}
    ignore = ' \t'
    reflags = re.IGNORECASE | re.MULTILINE
    tokens = {NAME, FRACTION, OPTION, EOL_COMMENT, FLOAT, INTEGER}

    OPTION = r'(?:(?:gas|estep|cond)\s+\d+)|(?:(?:n|p|pn|e)lib\s+\S+)'

    @_(r'm\d+')
    def NAME(self, t):
        t.value = int(t.value[1:])
        return t

    @_(r'\d+(?:\.\d+[cdepuy])')
    def FRACTION(self, t):
        if '.' in t.value:
            isotope, lib = t.value.split('.')
            isotope = int(isotope)
            lib = lib[:] # drop dot
            lib = cmn.ensure_lower(lib)
            t.value = isotope, lib
        else:
            t = self.on_integer(t)
        return t

    @_(cmn.LINE_WITH_COMMENT)
    def EOL_COMMENT(self, t):
        t.value = t.value.strip()
        return t

    @_(cmn.FLOAT)
    def FLOAT(self, token):
        return self.on_float(token)

    @_(cmn.INTEGER)
    def INTEGER(self, token):
        return self.on_integer(token)


# noinspection PyUnresolvedReferences
class Parser(sly.Parser):
    tokens = Lexer.tokens

    @staticmethod
    def build_composition(name, fractions, options=None, comments=None):
        atomic = []
        weight = []
        for el, fraction in fractions:
            if fraction < 0.0:
                weight.append((el, -fraction))
            else:
                atomic.append((el, fraction))
        if options is None:
            options = {'name': name}
        else:
            options['name'] = name
        if comments:
            options['comment'] = comments
        return mat.Composition(atomic=atomic, weight=weight, **options)

    @_('composition_a comments')
    def composition(self, p):
        name, fractions, options = p.composition_a
        return Parser.build_composition(name, fractions, options, p.comments)

    @_('composition_a')
    def composition(self, p):
        name, fractions, options = p.composition_a
        return Parser.build_composition(name, fractions, options)

    @_('NAME fractions options')
    def composition_a(self, p):
        return p.NAME, p.fractions, p.options

    @_('NAME fractions')
    def composition_a(self, p):
        return p.NAME, p.fractions, None

    @_('fractions fraction')
    def fractions(self, p):
        p.fractions.append(p.fraction)
        return p.fractions

    @_('fraction')
    def fractions(self, p):
        return [p.fraction]

    @_('fraction_a EOL_COMMENT')
    def fraction(self, p):
        name, lib, frac = p.fraction_a
        return mat.Element(name, lib=lib, comment=p.EOL_COMMENT), frac

    @_('fraction_a')
    def fraction(self, p):
        name, lib, frac = p.fraction_a
        return mat.Element(name, lib=lib), frac

    @_('FRACTION FLOAT')
    def fraction_a(self, p):
        isotope, lib = p.FRACTION
        return isotope, lib, p.FLOAT

    @_('options option')
    def options(self, p):
        option, value = p.option
        p.options[option] = value
        return p.options

    @_('option')
    def options(self, p):
        option, value = p.option
        result = dict()
        result[option] = value
        return result

    @_('OPTION')
    def option(self, p):
        option, value = p.OPTION.split()
        if not option.islower():
            option = option.lower()
        if option in ("gas", "estep", "cond"):
            value = int(value)
        return option, value

    @_('comments comment')
    def comments(self, p):
        p.comments.append(p.comment)
        return p.comments

    @_('comment')
    def comments(self, p):
        return [p.comment]

    @_('EOL_COMMENT')
    def comment(self, p):
        return p.EOL_COMMENT


def parse(text):
    text = drop_c_comments(text)
    lexer = Lexer()
    parser = Parser()
    result = parser.parse(lexer.tokenize(text))
    return result
