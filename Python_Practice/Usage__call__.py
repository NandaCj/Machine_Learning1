"""

__call__ is used to call an instance as a Function
Ex : obj = class1 ()
    here obj is the instance -- it will call the __init__ method
    whereas calling the obj as obj() -- will call the __call__ method

https://stackoverflow.com/questions/9663562/what-is-the-difference-between-init-and-call-in-python

"""

class class_decorator1:
    def __init__(self, func1):
        """ The Func Object will be transferred to the __init__ method only"""
        print ("class_decorator1")
        self.f = func1
        pass


    def __call__(self):
        #self.f()
        print ("Inside class_decorator1 class __call__ method")


class class_decorator:
    def __init__(self, func1):
        print ("class_decorator")
        self.f = func1
        pass
    def __call__(self):
        #self.f()
        print ("Inside class_decorator class __call__ method")




class class1(object):
    def __init__(self, func):
        print("__Init__")

    def __call__(self):
        print ("__Call__")

# obj = class1(); print (type(obj))
# obj()
#
# @class_decorator1
# @class_decorator

# @class1
# def func ():
#     print ("calling Normal func")
#
# func()


# Using a decorator that accepts Arguments:

class class2():
    def __init__(self,func):
        #print(arg)
        self.f = func
        # self.func=func
        print("__Init__")

    def __call__(self,arg):
        def new_func(arg):

            return  self.f(arg)
            print ("__Call__")
        return new_func

@class2("Text")
def func1 (arg):
    print ("printing", arg)

#func1(1234)






















