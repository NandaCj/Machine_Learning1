class summa:
    def __init__(self):
        pass

    def func(self):
        pass

class Decorator:

    def __init__(self, Func, *args):
        self.Func = Func
        print ("Args:", args)

    def __call__(self, *args, **kwargs):
        print ("Args inside a __call__", args)
        print ("Welcome To Decorator Function, What do you need ?")
        self.Func(self)
        print ("Thanks for Coming You are Decoratored")

# @Decorator
# def Function():
#     print ("I need Decoration")

#Function()