class ClassBasedDecoratorWithParams():

    def __init__(self, arg1, arg2):
        print "INIT ClassBasedDecoratorWithParams"
        print arg1
        print arg2

    def __call__(self, fn, *args, **kwargs):
        print "CALL ClassBasedDecoratorWithParams"

        def new_func(*args, **kwargs):
            print "Function has been decorated.  Congratulations."
            return fn(*args, **kwargs)
        return new_func


@ClassBasedDecoratorWithParams("Passed Args1", "Passed Args2")
def print_args_again(*args):
    for arg in args:
        print arg


print_args_again(1, 2, 3)
print_args_again("asd", "sda","rege")
