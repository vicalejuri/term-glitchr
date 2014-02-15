def mk_utf8_table( start=0, end=10 ):
    return [unichr(i) for i in xrange(start,end)]

PUNCS = [unichr(0x005F), \
    unichr(0x203F), \
    unichr(0x2040),\
    unichr(0x2054),\
    unichr(0xFE33),\
    unichr(0xFE34),\
    unichr(0xFE4D),\
    unichr(0xFE4E),\
    unichr(0xFE4F),\
    unichr(0xFF3F)
]

CHARTABLES = {
        'maze_commodore':              m[ u'╲', u'╱' ],
        'maze_ascii':                   [ '\\','/' ],
        'glitch_dos':                   [ u'◤', u'◥', u'▌',u'▂', u'▒'],
        'hangul_jano_full':             mk_utf8_table( 0x1100, 0x11FF ),
        'hangul_jano_esc':              mk_utf8_table( 0x1161, 0x119D ),
        'punctuation_connector':        PUNCS,
        'cannada_aboriginal_full':      mk_utf8_table( 0x1401, 0x167F ),
        'cannada_aboriginal_setas':     mk_utf8_table( 0x1401, 0x141B ),
        'fuck':                         mk_utf8_table( 0x1041, 0x2000 ),
        'input': [' '],
        'dotted':  [ '+','-', \
                     '.',',', \
                     "'",'`', ]
