from matplotlib import pyplot as plt


class Matplot:

    def __init__(self):
        pass

    def Scatter_Plot (self, X_Label, X_Values, Y_Label, Y_Values):
        plt.xlabel(X_Label); plt.ylabel(Y_Label)
        plt.scatter(X_Values, Y_Values)
        plt.show()

    def Line_Plot (self, X_Label, X_Values, Y_Label, Y_Values):
        plt.xlabel(X_Label);plt.ylabel(Y_Label)
        plt.plot(X_Values, Y_Values)
        plt.show()

if __name__ == "__main__":
    matplot = Matplot()
    X_Values = [1, 3, 5, 7, 9]
    Y_Values = [i*2 for i in X_Values]
    # matplot.Line_Plot("X Values", X_Values, "Y Values",Y_Values)
    matplot.Scatter_Plot("X Values", X_Values, "Y Values", Y_Values)

