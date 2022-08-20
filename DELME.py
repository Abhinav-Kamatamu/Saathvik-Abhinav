import pygame, sys, time


class Hi:
    def __init__(self):
        self.things = [self.f_1, self.f_2]

    def f_1(self):
        print('f1')

    def f_2(self):
        print('f2')

    def run(self):
        for i in self.things:
            i()


hi = Hi()
#hi.run()
