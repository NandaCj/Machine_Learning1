import pickle


Pickle_File = "Pickle_Dump"

class Helpers:

    def __init__(self):
        pass

    def Print_Type_And_Value(self, *args):
        print("************************************************")
        for arg in args:
            print ("Argument Type :", type(arg), "\n")
            print ("Argument Value :", arg, "\n")
        print ("************************************************")

    def Pickle_Dump (self, Object_To_Dump):
        File_Object = open(Pickle_File, "wb")
        pickle.dump(Object_To_Dump, File_Object)

    def Pickle_Load (self):
        File_Object = open(Pickle_File, "rb")
        Loaded_Object = pickle.load(File_Object)

        return Loaded_Object