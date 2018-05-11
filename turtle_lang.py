import random
import turtle

import matplotlib
from arpeggio.cleanpeg import ParserPEG
from PIL import Image

from colors import read_color

grammar = r"""
hex_color = r'\#([a-fA-F0-9]{3}){1,2}' # 3 or 6 hex digits
lowercase_word = r'[a-z]{1,20}'
positive_integer = r'[1-9]\d*'

color_string = hex_color / lowercase_word   # we'll use matplotlib's colors list
color = "color" color_string
fillcolor = "fillcolor" color_string

pen_up = "pen up" / "pu"
pen_down = "pen down" / "pd"
pen_change = pen_up / pen_down

begin_fill = "begin_fill" / "bf"
end_fill = "end_fill" / "ef"
fill_change = begin_fill / end_fill

dot = "dot"

left = "left" / "lt"
right = "right" / "rt"
turn_direction = left / right
rotation = turn_direction positive_integer

forward = "forward" / "fd"
backward = "backward" / "bk"
direction = forward / backward
movement = direction positive_integer

expression = pen_change / fill_change / color / fillcolor / dot / rotation / movement

body = statement+
loop = ("loop" / "lp") positive_integer body ("end loop" / "el")

probability = r'0?\.\d{1,10}'
else_clause = "else" body
maybe = ("maybe" / "mb") probability? body else_clause? ("end maybe" / "em")

statement = loop / maybe / expression
program = statement+ EOF
"""

parser = ParserPEG(grammar, 'program')

def do_rotation(rot, t):
    assert rot.turn_direction[0][0].rule_name in ('left', 'right'), "expected rot.turn_direction to be left or right. got " + rot.turn_direction.rule_name
    direction = t.left if rot.turn_direction[0][0].rule_name == 'left' else t.right
    degrees = int(rot.positive_integer.value)
    direction(degrees)

def do_movement(mov, t):
    assert mov.direction[0][0].rule_name in ('forward', 'backward'), "expected mov.direction to be forward or backward. got " + mov.direction.rule_name
    direction = t.forward if mov.direction[0][0].rule_name == 'forward' else t.backward
    steps = int(mov.positive_integer.value)
    direction(steps)

def do_expression(expr, t):
    print('top of do expression', expr.rule_name, expr)
    if expr.rule_name == 'pen_change':
        if expr[0].rule_name == 'pen_up':
            t.penUp()
        else:
            assert expr[0].rule_name == 'pen_down'
            t.penDown()
    elif expr.rule_name == 'fill_change':
        if expr[0].rule_name == 'begin_fill':
            t.begin_fill()
        else:
            assert expr[0].rule_name == 'end_fill'
            t.end_fill()
    elif expr.rule_name == 'color':
        t.color(read_color(expr.color_string))
    elif expr.rule_name == 'fillcolor':
        t.fillcolor(read_color(expr.color_string))
    elif expr.rule_name == 'dot':
        t.dot()
    elif expr.rule_name == 'rotation':
        do_rotation(expr, t)
    elif expr.rule_name == 'movement':
        do_movement(expr, t)
    else:
        raise RuntimeError('Unrecognized Expression type: ' + expr.rule_name)

def do_maybe(mb, t):
    assert mb.rule_name == 'maybe', "Expected to be called on a maybe, received " + mb.rule_name
    if mb[1].rule_name == 'body':
        # no probability, so choose 0.5
        prob = 0.5
    else:
        assert mb[1].rule_name == 'probability'
        prob = float(mb[1].value)
    if random.random() < prob:
        do_statement(mb.body, t)
    elif mb[-2].rule_name == 'else_clause':
        do_statement(mb.else_clause.body, t)

def do_loop(loop, t):
    assert loop.rule_name == 'loop', "Expected to be called on a loop, received " + loop.rule_name
    iters = int(loop.positive_integer.value)
    for _ in range(iters):
        for stmt in loop.body:
            print('about to do', stmt)
            do_statement(stmt, t)


def do_statement(statement, t):
    print('top of do statement', statement.rule_name, statement)
    if statement.rule_name == 'statement':
        return do_statement(statement[0], t)
    elif statement.rule_name == 'body':
        for stmt in statement:
            do_statement(stmt, t)
    elif statement.rule_name == 'expression':
        return do_expression(statement[0], t)
    elif statement.rule_name == 'maybe':
        return do_maybe(statement, t)
    elif statement.rule_name == 'loop':
        return do_loop(statement, t)

def run_turtle_program(source):
    """
    parse and run the turtle program, producing an image.

    return the image (as a filename?)
    """
    ast = parser.parse(source)

    t = turtle.Turtle()
    for stmt in ast.statement:
        do_statement(stmt, t)
    canvas = turtle.Screen().getcanvas()
    canvas.postscript(file='image.eps')
    img = Image.open('image.eps')
    img.save('image.png', 'png')
    turtle.Screen().bye()
    return 'image.png'
