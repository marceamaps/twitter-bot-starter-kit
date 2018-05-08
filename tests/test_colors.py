from arpeggio.cleanpeg import ParserPEG
from nose.tools import eq_

from turtle_lang import grammar
from colors import read_color

parser = ParserPEG(grammar, 'color_string')


def test_color_parsing():
    eq_(read_color(parser.parse('#123')), '#112233')
    eq_(read_color(parser.parse('#abcabc')), '#abcabc')
    eq_(read_color(parser.parse('red')).lower(), '#ff0000')
