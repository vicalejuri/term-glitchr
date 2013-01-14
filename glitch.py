#!/usr/bin/python -u
# -*- coding: utf8 -*-

from threading import Timer
from blessings import Terminal

import sys,signal
from random import choice,uniform
from time import sleep

from optparse import OptionParser

def mk_utf8_table( start=0, end=10 ):
    return [unichr(i) for i in xrange(start,end)]

punc = [unichr(0x005F), \
unichr(0x203F), \
unichr(0x2040),\
unichr(0x2054),\
unichr(0xFE33),\
unichr(0xFE34),\
unichr(0xFE4D),\
unichr(0xFE4E),\
unichr(0xFE4F),\
unichr(0xFF3F)]

CHARTABLES = {
        'maze_commodore': [ u'╲', u'╱' ],
        'maze_ascii':   [ '\\','/' ],
        'glitch_dos': [ u'◤', u'◥', u'▌',u'▂', u'▒'],
        'hangul_jano_full': mk_utf8_table( 0x1100, 0x11FF ),
        'hangul_jano_esc': mk_utf8_table( 0x1161, 0x119D ),
        'punctuation_connector': punc,
        'cannada_aboriginal_full': mk_utf8_table( 0x1401, 0x167F ),
        'cannada_aboriginal_setas': mk_utf8_table( 0x1401, 0x141B ),
        'fuck':  mk_utf8_table( 0x1041, 0x2000 ),
        'spaces': [''],
        'dotted':  [ '+','-', \
                     '.',',', \
                     "'",'`', ]

}


mframe = -1
options = {'column': 80, 'table': 'maze_commodore' , 'speed': 100 ,
        'bold': 1.0, 'blink': 1.0 ,
        'colors_bg': 'black',
        'colors_fg': 'white'}

term = Terminal()
options['column'] = term.width

def main():
    while 1:
        loop()
        if options.speed != 0:
            sleep( 1/options.speed )

def loop():
    """ Render a single charpixel. Iterate over loop to get your image! """
    global mframe
    mframe += 1

    # New column on edge
    if not mframe%options.column:
        sys.stdout.write('\n')

    # Draw char pixel
    render_prechar()
    sys.stdout.write( get_charpixel() )
    render_postchar()

    if options.bold:
        sys.stdout.write( term.normal )


def get_charpixel():
    """ Render a single charpixel """
    c = choice( CHARTABLES[ options.table ] )
    return c.encode('utf-8')

def get_color(color_name):
    return getattr(term, color_name)

def render_prechar():
    rand = uniform(0,1)
    c = ''

    # Colors BG
    c = get_color( 'on_' + choice( options.colors_bg ) )
    c += get_color( choice( options.colors_fg ) )

    # Bold/blink
    c += (term.bold if (options.bold != 1.0 and rand < options.bold) else '')
    c += (term.blink  if (options.blink != 1.0 and rand < options.blink) else '')

    if c:
        sys.stdout.write( c )

def render_postchar():
    sys.stdout.write( term.normal )


# Handle ctrl-c cleanly
def exit_handler(signum, frame):
    sys.exit(0)
signal.signal( signal.SIGINT, exit_handler)


if(__name__ == '__main__'):
    parser = OptionParser()
    parser.add_option( '-c','--columns',dest='column',type='int',default=options['column'],help="The number of columns")
    parser.add_option( '-t','--table', dest='table',default=options['table'],
                                        choices=CHARTABLES.keys(), help="The character table to use.")
    parser.add_option( '-s','--speed', dest='speed', type="float",
                                        default=options['speed'], help="Set the speed. ++ = FASTER , 0 = full-speed")

    parser.add_option( '--fg', type='string', default='red,green,magenta,cyan,white', dest='colors_fg', help="Set color FG Mode. ")
    parser.add_option( '--bg', type='string', default='red,green,magenta,cyan,white', dest='colors_bg', help="Set color BG Mode. ")

    parser.add_option( '--discoteque',action='store_false', help="Discoteque mode." )
    parser.add_option( '--bold', type='float', default=1.0, dest='bold', help="Set bold mode on. Choose a likehood that char appears bold (randomly)")
    parser.add_option( '--blink', type='float', default=1.0, dest='blink', help="Set blink mode on. Choose a likehood that char appears blink (randomly)")


    (opt,args) = parser.parse_args()

    # Save the options as globals, please
    options = opt
    options.colors_fg = options.colors_fg.split(',')
    options.colors_bg = options.colors_bg.split(',')

    # Proceed
    main()
