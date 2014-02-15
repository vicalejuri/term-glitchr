#!/usr/bin/python -u
# -*- coding: utf8 -*-

from threading import Timer
from blessings import Terminal

import sys,signal,tty,termios
from random import choice,uniform,randint
from time import sleep

from optparse import OptionParser

from chartables import CHARTABLES
from fx import BgFx, FgFx , BlinkFx, BoldFx

COLORS = ['black','red','green','yellow','blue','magenta','cyan','white']

FG_COLORS = ['black','magenta','red','green','blue']
BG_COLORS = ['bright_white', 'bright_magenta','bright_red','bright_green','bright_blue']

RENDERMODES = ['char','word','line','random','never']
render_count = 0

mframe = -1
options = {'column': 80,
            'table': 'maze_commodore' ,
            'speed': 100 ,
            'rendermode': 'char',
            'bold': 1.0, 'blink': 1.0 ,
            'colors_bg':  FG_COLORS,
            'colors_fg':  BG_COLORS }

term = Terminal()
options['column'] = term.width

# taken from http://code.activestate.com/recipes/134892/
def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr( fd, termios.TCSADRAIN, old_settings )

    return ch

def run():
    while 1:
        loop()
        if options.speed != 0:
            sleep( 1/options.speed )

def get_charpixel():
    """ Render a single charpixel """
    if options.table == 'input':
        c = getch()
        if c in ['\n','\t']:
            print(c)
    else:
        c = choice( CHARTABLES[ options.table ] )

    return c.encode('utf-8')

def render_block():
    global render_count
    render_count += 1

    curr_char = get_charpixel()
    sys.stdout.write( curr_char )

    # Get out of this block, when necessary
    if options.rendermode == 'char':
        render_count = 0
        return
    elif options.rendermode == 'word':
        # Break on 4 char
        if render_count == 4:
            render_count = 0
            return
    elif options.rendermode == 'line':
        if render_count == options.column:
            if options.breakline:
                sys.stdout.write('\n' * int(options.breakline))

            render_count = 0
            return
    elif options.rendermode == 'random':
        if render_count == randint(0,10):
            render_count = 0
            return

    render_block()


def loop():
    """ Render a single charpixel. Iterate over loop to get your image! """
    global mframe
    mframe += 1

    #if not mframe%options.column:
    #    sys.stdout.write('\n')

    # Render FX's
    for fx in fx_chain:
        sys.stdout.write( fx.render() )

    # Draw char pixel
    render_block()

    # Back to normal
    sys.stdout.write( term.normal )


# Handle ctrl-c cleanly
def exit_handler(signum, frame):
    sys.exit(0)
signal.signal( signal.SIGINT, exit_handler)

def main():
    global options, RENDERMODES,CHARTABLES

    parser = OptionParser()
    parser.add_option( '-r','--rendermode', dest='rendermode', default=options['rendermode'],
                                                               choices=RENDERMODES , help="Break mode on every c(char) , w(word) , l(line) , r(random), n(never)?" )
    parser.add_option( '-t','--table', dest='table',default=options['table'],
                                        choices=CHARTABLES.keys(), help="The character table to use.")
    parser.add_option( '-c','--columns',dest='column',type='int',default=options['column'],help="The number of columns")
    parser.add_option( '-s','--speed', dest='speed', type="float",
                                        default=options['speed'], help="Set the speed. ++ = FASTER , 0 = full-speed")

    parser.add_option( '--fg-table', type='string', default=options['colors_fg'], dest='colors_fg', help="Set color FG Mode. ")
    parser.add_option( '--bg-table', type='string', default=options['colors_bg'], dest='colors_bg', help="Set color BG Mode. ")

    parser.add_option( '--bold', type='float', default=0.0, dest='bold', help="Set bold mode on. Choose a threshold from 1(full) to 0(none)")
    parser.add_option( '--blink', type='float', default=0.0, dest='blink', help="Set blink mode on. Choose a threshold from 1(full) to 0(none)" )

    parser.add_option( '--breakline', default=1.0, dest='breakline', help="Break on paragraphs" )


    (opt,args) = parser.parse_args()

    # Save the options as globals, please
    options = opt
    options.colors_fg = options.colors_fg.split(',')
    options.colors_bg = options.colors_bg.split(',')

    # Fx'
    fx_chain = [BgFx(term, 1.0 ,args=options.colors_bg)]
    fx_chain.append( FgFx(term, 1.0, args=options.colors_fg)  )

    if options.bold > 0:
        fx_chain.append( BoldFx(term,options.bold) )
    if options.blink > 0:
        fx_chain.append( BlinkFx(term,options.blink) )

    # Proceed
    run()

if(__name__ == '__main__'):
    main()
