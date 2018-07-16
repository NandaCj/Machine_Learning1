class simple_call:
    def __init__(self):
        print "Working"

class class1:
    var = "var1"

class class2 :
    var = "var2"

class class3:
    var = "var3"

class Home (class3, class2, class1):
    def __init__(self):
        print (self.var)

if __name__ == "__main__":
    Home()
