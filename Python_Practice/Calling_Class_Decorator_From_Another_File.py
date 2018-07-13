from Class_Decorator import *

class Summa:
    def __init__(self):
        self.Function()

    @Decorator
    def Function(self):
        print ("I am from Another Class, Can I Get Decorated")

Summa()