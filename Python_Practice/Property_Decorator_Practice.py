
class Test1 :
    """
    @property Decorator is used to call any Function as a variable
        it will treat a method as variable inside that Class only
        Outside class it returns a property Obj , u can use any inbuilt
            datatype to read it such as str or list

    """

    @property
    def Func1(self):
        Name = "Nandha"
        return Name

    def Print_Name(self):
        print(self.Func1)

if __name__ == "__main__":
    # Obj = Test1()
    # Obj.Print_Name()

    print (str(Test1().Func1))
