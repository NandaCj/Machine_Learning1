import pickle
import logging
import numpy as np

Log_Format = "%(asctime)s %(levelname)s [%(name)s] %(message)s"
logging.basicConfig(level='DEBUG', format=Log_Format)
logger = logging.getLogger(__name__)
Info = logger.info
Critical = logger.critical

Pickle_File = "Pickle_Dump"

class Helpers:

    def __init__(self):
        pass

    def Print_Type_And_Value(self, *args):
        print("************************************************")
        for arg in args:

            print ("Total Length of Argument : ", len(arg))
            print ("Argument Type :", type(arg), "\n")
            if isinstance(arg, (np.ndarray)):
                print ("--->Array Shape ", arg.shape)
            print ("Argument Value :", arg, "\n")
        print ("************************************************")

    def Pickle_Dump (self, Object_To_Dump):
        File_Object = open(Pickle_File, "wb")
        pickle.dump(Object_To_Dump, File_Object)

    def Pickle_Load (self):
        File_Object = open(Pickle_File, "rb")
        Loaded_Object = pickle.load(File_Object)

        return Loaded_Object

class StartLogging:

    def __init__(self, log_level='DEBUG'):
        logging.basicConfig(level=log_level)
        logger = logging.getLogger(log_level)
        global Info
        Info = logger.info


