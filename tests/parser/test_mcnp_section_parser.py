# -*- coding: utf-8 -*-

import pytest
from io import StringIO

from mckit.parser.mcnp_section_parser import *



@pytest.mark.parametrize("text,expected", [
    ( "aaa\n\nbbb", ["aaa", "bbb"]),
    ("aaa\n   \nbbb", ["aaa", "bbb"]),
    ("aaa\nbbb", ["aaa\nbbb"]),
])
def test_blank_line_pattern(text, expected):
    actual = BLANK_LINE_PATTERN.split(text)
    assert actual == expected


@pytest.mark.parametrize("text,expected", [
    ( "1 0 1\n", ('1 0 1\n', 0)),
    ("1 0 1 $bla bla bla\n", ('1 0 1\n', 1)),
    (
        "1 0 1 $bla bla bla\n" +
        "c the comment with the space before c\n" +
        "   2 -3",
        (
            "1 0 1\n" +
            "   2 -3", 2
        )
    ),
])
def test_removing_comment_pattern(text, expected):
    actual = REMOVE_COMMENT_PATTERN.subn('', text)
    assert expected == actual


@pytest.mark.parametrize("text,comment,card", [
    ("1 0 1\n", None, '1 0 1\n'),
    (
            """
c the preceding comment
1 0 1
"""[1:-1],
            """
c the preceding comment
"""[1:],
            "1 0 1"
    ),
    (
            """
c the preceding comment
1 0 1
 c The next card comment (with space before it)
  2 $next card
"""[1:-1],
            """
c the preceding comment
"""[1:],
            "1 0 1\n"
    ),
    (
"""
C ----------------------------------------------------------------------------C
C    TRANSFORMATIONS                                                          C
C    ROTATION WITH RESPECT TO Z-AXIS (-20,|5|,20)                             C
C ----------------------------------------------------------------------------C
*TR1    0  0  0
        20.0000    70.0000  90
       110.0000    20.0000  90
       90        90         0
"""[1:-1],
"""
C ----------------------------------------------------------------------------C
C    TRANSFORMATIONS                                                          C
C    ROTATION WITH RESPECT TO Z-AXIS (-20,|5|,20)                             C
C ----------------------------------------------------------------------------C
"""[1:],
"""
*TR1    0  0  0
        20.0000    70.0000  90
       110.0000    20.0000  90
       90        90         0
"""[1:-1]
    ),
])
def test_card_pattern(text, comment, card):
    res = CARD_PATTERN.match(text)
    groups = res.groupdict()
    actual_comment = groups["comment"]
    assert comment == actual_comment
    actual_card = groups["card"]
    assert actual_card == card


@pytest.mark.parametrize("text,cards,kind", [
    (
            """
c the preceding comment
1 0 1
c next comment
  2 $next card (starts with less than 5 spaces)
"""[1:-1],
            [
                Card("c the preceding comment"),
                Card("1 0 1", kind=Kind.CELL),
                Card("c next comment"),
                Card("  2 $next card (starts with less than 5 spaces)", kind=Kind.CELL)
            ],
            Kind.CELL,
    ),
    (
            """
c the preceding comment
1 0 1
c inner comment
     2 $continuation
c the second preceding comment
2 0 -1 $the next card
c the trailing comment
c the second line of the trailing comment
"""[1:-1],
        [
            Card("c the preceding comment"),
            Card(
                """
1 0 1
c inner comment
     2 $continuation
"""[1:-1], kind=Kind.CELL),
            Card("c the second preceding comment"),
            Card("2 0 -1 $the next card", kind=Kind.CELL),
            Card(
                    """
c the trailing comment
c the second line of the trailing comment
"""[1:-1]),
            ],
            Kind.CELL,
    ),
    (
            """
  cut 5j  $ card starts in column < 5
ctme 3000
"""[1:],
        [Card("  cut 5j  $ card starts in column < 5"), Card("ctme 3000")],
        None,
    ),
    (
        """
m100
      1001.31c 0.6666
      8000.21c 0.3334
"""[1:-1],
        [Card(
        """
m100
      1001.31c 0.6666
      8000.21c 0.3334
"""[1:-1],
            kind=Kind.MATERIAL
        )],
        None
    ),
])
def test_split_to_cards(text, cards, kind):
    actual_cards = list(split_to_cards(text, kind))
    assert actual_cards == cards


@pytest.mark.parametrize("text", [
        (
        """
sdef
sp1
si1
ds3
sb45
wwp:n
"""[1:-1]
        ),
])
def test_sdef_cards(text):
    actual_cards = list(split_to_cards(text))
    for card in actual_cards:
        assert card.is_sdef, "Should be SDEF card"



def test_card_constructor():
    descr = "1 0 1"
    c = Card(descr)
    assert c.text == descr


def test_input_sections_constructor():
    title = "Testing"
    cell_cards = [Card("1 0 1"), Card("2 0 -1")]
    surface_cards = [Card("1 so 100")]
    t = InputSections(
        title,
        cell_cards,
        surface_cards,
        [Card("sdef")],
    )
    assert t.title == title


@pytest.mark.parametrize("text,expected,kind", [
    (
            """
1 0 1 $bla bla bla
"""[1:-1],
            [
                Card("1 0 1", kind=Kind.CELL)
            ],
            Kind.CELL,
    ),
    (
            """
c some comment
c second line
1 0 1 $bla bla bla
     2 $continuation
c trailing comment
"""[1:-1],
            [
                Card(
                    """
1 0 1 2
"""[1:-1], kind=Kind.CELL
                )
            ],
            Kind.CELL,
    ),
    (
            """
c some comment
c second line
1 0 1 $bla bla bla
     2 $continuation
c trailing comment
2
     0 -1  $rrrrrr
c z-z-zz-z-z-z
"""[1:-1],
            [
                Card(
                    """
1 0 1 2
"""[1:-1], kind=Kind.CELL
                ),
                Card(
                    """
2 0 -1
"""[1:-1], kind=Kind.CELL
                ),
            ],
            Kind.CELL,
    ),
])
def test_clean_mcnp_cards(text, expected, kind):
    actual = list(clean_mcnp_cards(split_to_cards(text, kind)))
    assert actual == expected


@pytest.mark.parametrize("text,expected", [
    (
            """
test
1 0 1 $bla bla bla

1 so 1

sdef
"""[1:],
            None,
    ),
    (
            """
test
c some comment
c second line
1 0 1 $bla bla bla
     2 $continuation
2 0 -1
c trailing comment

1 so 1

sdef
"""[1:],
            None,
    ),
    (
            """
test
c some comment
c second line
1 0 1 $bla bla bla
     2 $continuation
c trailing comment
2
    0 -1  $rrrrrr
c z-z-zz-z-z-z

1 so 1

sdef
"""[1:],
            None
    ),
    (
            """
continue
ctme 3000
"""[1:],
            None
    ),
])
def test_print(text, expected):
    stream = StringIO(text)
    sections = parse_sections(stream)
    out = StringIO()
    sections.print(out)
    if expected is None:
        expected = text.strip()
    actual = out.getvalue().strip()
    assert actual == expected
