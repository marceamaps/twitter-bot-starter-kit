from nose.tools import assert_raises
from turtle_lang import parser
from arpeggio import NoMatch
import matplotlib

def test_simple_example():
    parser.parse('forward 10')

def test_loop():
    parser.parse('''
    forward 10
    loop 5
        maybe
            color red
        end maybe
        right 90
        forward 10
    end loop
    ''')

def test_unfinished_loop():
    assert_raises(NoMatch, parser.parse, """
    loop 12
       maybe color red end maybe
    """)
