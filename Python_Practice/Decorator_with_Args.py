#Simple Decoraotor Function Accpeting Arguments
# To make a decorator to accept arguments use another function and put all the deco codes into it .

def decorator_function_with_args(decoraotor_arguments):
    def decorator_function(func):
        def decorator_function_implementation(arg):
            print (decoraotor_arguments)
            func(arg)
        return decorator_function_implementation
    return  decorator_function


@decorator_function_with_args("Decorator Arguments")
def function_tobe_decorated(arg):
    print ("Function_tobe_decorated \n Argument Passed =",arg )

function_tobe_decorated("Argument Passed")