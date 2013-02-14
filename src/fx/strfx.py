from random import uniform,choice

class StrFx():
    def __init__(self, term,likehood, args=None):
        self.term = term
        self.likehood = likehood
        self.args= args

    def render(self):
        self.r = uniform(0,1)
        if self.r < self.likehood:
            return self.write()
        return ''

    def write(self):
        return ''


class BgFx(StrFx):
    def write(self):
        return getattr(self.term, 'on_' + choice( self.args) )

class FgFx(StrFx):
    def write(self):
        return getattr(self.term, choice( self.args ) )

class BlinkFx(StrFx):
    def write(self):
        return self.term.blink

class BoldFx(StrFx):
    def write(self):
        return self.term.bold
