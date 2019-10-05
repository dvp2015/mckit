import logging
import re
import sys
import typing as tp
from enum import IntEnum
from timeit import default_timer as timer

import six
from attr import attrs, attrib

LOG = logging.getLogger(__name__)


BLANK_LINE_PATTERN = re.compile(
    r'\n\s*\n',
    flags=re.MULTILINE,
)

COMMENT_LINE_PATTERN = re.compile(
    r'^\s{,5}[cC]( .*)?\s*$'
)

# pattern to remove comments from a card text
REMOVE_COMMENT_PATTERN = re.compile(
    r'(\s*\$.*$)|(^\s{0,4}c\s.*\n?)',
    flags=re.MULTILINE | re.IGNORECASE
)


# pattern to split section text to optional "comment" and subsequent MCNP card pairs
CARD_PATTERN = re.compile(
    r"(?P<comment>((^\s{,5}c( .*)?\s*$)\n?)+)?(?P<card>^\s{,5}(\*|\w).*(\n((^\s{,5}c.*\n?)*^\s{5,}\S.*\n?)*)?)?",
    flags=re.MULTILINE | re.IGNORECASE
)

# pattern to replace subsequent spaces with a single one
SPACE_PATTERN = re.compile(
    r"\s+",
    flags=re.MULTILINE
)


class Kind(IntEnum):
    COMMENT = 0,
    CELL = 1,
    SURFACE = 2,
    MATERIAL = 3,
    TRANSFORMATION = 4,
    SDEF = 5,
    GENERIC = 6

    @classmethod
    def from_card_text(cls, text: str):
        if text[0] in "mM" and str.isdigit(text[1]):
            return Kind.MATERIAL
        # check if a label is for transformation card, example: TR20 or *tr1
        i = 0
        if text[0] == "*":
            i = 1
        if text[i] in "tT" and text[i + 1] in "rR" and str.isdigit(text[i + 2]):
            return Kind.TRANSFORMATION
        label: str = text.split(maxsplit=2)[0]
        if 'sdef' == label.lower():
            return Kind.SDEF
        if is_comment_text(text, skip_asserts=True):
            return Kind.COMMENT
        return Kind.GENERIC


@attrs
class Card(object):
    """
    Generic MCNP card raw text item

    The card kind is defined either from parsing context (for cells and surfaces) or
    from card label
    """

    text: str = attrib()
    kind: tp.Optional[Kind] = attrib(default=None)

    # noinspection PyUnusedLocal,PyUnresolvedReferences
    @kind.validator
    def check(self, attribute, value):
        if self.kind is None:
            self.kind = Kind.from_card_text(self.text)

    @property
    def is_comment(self):
        return self.kind is Kind.COMMENT

    @property
    def is_material(self):
        return self.kind is Kind.MATERIAL


    @property
    def is_transformation(self):
        return self.kind is Kind.TRANSFORMATION

    @property
    def is_cell(self):
        return self.kind is Kind.CELL


    @property
    def is_surface(self):
        return self.kind is Kind.SURFACE


    @property
    def is_sdef(self):
        return self.kind is Kind.SDEF



    def get_clean_text(self):
        return get_clean_text(self.text)


@attrs
class InputSections(object):
    title: tp.Optional[str] = attrib(default=None)
    cell_cards: tp.Optional[tp.List[Card]] = attrib(default=None)
    surface_cards: tp.Optional[tp.List[Card]] = attrib(default=None)
    data_cards: tp.Optional[tp.List[Card]] = attrib(default=None)
    message: tp.Optional[str] = attrib(default=None)
    remainder: tp.Optional[str] = attrib(default=None)
    is_continue: bool = attrib(default=False)

    # noinspection PyUnusedLocal,PyUnresolvedReferences
    @is_continue.validator
    def check(self, attribute, value):
        if self.is_continue:
            if self.cell_cards or self.surface_cards:
                raise ValueError("Cells and Surfaces shouldn't present in 'continue' mode model")
            if not self.data_cards:
                raise ValueError("At least one data card should present in 'continue' mode model")

    def print(self, stream=sys.stdout):
        if self.message:
            print(self.message, file=stream)
            print(file=stream)
        if self.title:
            print(self.title, file=stream)
        if not self.is_continue:
            for card in self.cell_cards:
                print(card.text, file=stream)
            print(file=stream)
            for card in self.surface_cards:
                print(card.text, file=stream)
            print(file=stream)
        if self.data_cards:
            for card in self.data_cards:
                print(card.text, file=stream)
            print(file=stream)
        if self.remainder:
            print(self.remainder, file=stream)


def split_to_cards(text, kind=None):
    for res in CARD_PATTERN.finditer(text):
        groups = res.groupdict()
        comment = groups["comment"]
        card = groups["card"]
        if comment:
            comment = comment.rstrip()
            yield Card(comment, kind=Kind.COMMENT)
        if card:
            card = card.rstrip()
            if kind is None:
                _kind = Kind.from_card_text(card)
            else:
                _kind = kind
            yield Card(card, kind=_kind)


# noinspection PyIncorrectDocstring,PyUnresolvedReferences
def parse_sections(inp: tp.TextIO) -> InputSections:
    """
    Splits input file to sections according to mcnp input format.

    Long Description
    ----------------
    The parser provides minimal separation of text sections from the input file
    based on Blank Line Delimiter entries
    The sections can be parsed later and in order different from the input file
    using specific low level parsers for cell, surface and data cards.

    From MCNP manual
    ~~~~~~~~~~~~~~~~
    An input file has the following form::
        Message Block           | Optional
        Blank Line Delimiter    | Required if Message Block is present
        Title Card
        Cell Cards
        Blank Line Delimiter
        Surface Cards
        Blank Line Delimiter
        Data Cards
        Blank Line Terminator    | Recommended
        Anything Else            | Optional


    Parameters
    ----------
    inp - stream

    Exceptions
    ----------
    The parser performs verification of the input using builder object,
    on errors the builder raises SectionParserError.

    Returns
    -------
    mcnp_input_sections object, containing text of sections from the file
    """

    message = None
    cell_cards = None
    surface_cards = None
    data_cards = None
    remainder = None

    sections = BLANK_LINE_PATTERN.split(inp.read(), 5)

    # The first line can be message or title.
    kw = sections[0][:len("message:")].lower()

    i = 0

    if 'message:' == kw:
        message = sections[0]
        i += 1

    title, cur_section = sections[i].split('\n', 1)
    i += 1
    if not title:
        raise ValueError("Cannot find the MCNP model title")

    is_continue = check_title_is_continue(title)

    if is_continue:
        data_cards = list(split_to_cards(cur_section))
        if i < len(sections):
            remainder = '\n\n'.join(sections[i:])
        result = InputSections(
            title,
            cell_cards=cell_cards,
            surface_cards=surface_cards,
            data_cards=data_cards,
            message=message,
            remainder=remainder,
            is_continue=True
        )
    else:
        cell_cards = list(split_to_cards(cur_section, kind=Kind.CELL))
        if i < len(sections):
            cur_section = sections[i]
            surface_cards = list(split_to_cards(cur_section, kind=Kind.SURFACE))
            i += 1
            if i < len(sections):
                cur_section = sections[i]
                data_cards = list(split_to_cards(cur_section, kind=None))
                i += 1
                if i < len(sections):
                    remainder = '\n\n'.join(sections[i:])
        result = InputSections(
            title,
            cell_cards=cell_cards,
            surface_cards=surface_cards,
            data_cards=data_cards,
            message=message,
            remainder=remainder,
            is_continue=False
        )

    return result


CONTINUE_LEN = len("continue")


def check_title_is_continue(title):
    return title[:CONTINUE_LEN].lower() == 'continue'


def is_comment(seq):
    if isinstance(seq, six.string_types):
        return is_comment_text(seq, skip_asserts=True)
    res = next((text for text in seq.split('\n') if not is_comment_text(text)), False)
    return not res


def is_comment_text(text, skip_asserts=False):
    if not skip_asserts:
        assert isinstance(text, six.string_types), "The parameter 'line' should be text"
    if '\n' in text:
        res = next((line for line in text.split('\n') if not is_comment_line(line)), False)
        return not res
    else:
        return is_comment_line(text, skip_asserts=True)


def is_comment_line(line, skip_asserts=False):
    if not skip_asserts:
        assert isinstance(line, six.string_types), "The parameter 'line' should be text"
        assert '\n' not in line, "The parameter 'line' should be the single text line"
    return COMMENT_LINE_PATTERN.match(line)


def get_clean_text(text):
    without_comments = REMOVE_COMMENT_PATTERN.subn('', text)[0]
    with_spaces_normalized = SPACE_PATTERN.subn(' ', without_comments)[0]
    return with_spaces_normalized


def clean_mcnp_cards(iterable):
    for x in iterable:
        if x.kind is not Kind.COMMENT:
            clean_text = x.get_clean_text()
            t = Card(clean_text, kind=x.kind)
            yield t
