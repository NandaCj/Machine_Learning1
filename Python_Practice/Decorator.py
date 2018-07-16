#Simple Decoraotor Function

# When a function is decoroatored the return type of 'decorator_function_implementation' is what we get
#when the object of the decorator_function_implementation is returned then we can call that fucntion


def decorator_function(func):
    def decorator_function_implementation():
        func()
    return decorator_function_implementation


@decorator_function
def function_tobe_decorated():
    print ("Function_tobe_decorated")

print (function_tobe_decorated())