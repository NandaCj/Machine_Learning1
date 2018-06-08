from Helpers.Logging import *
import os
from collectiveintelligence_book_master import clusters


blogdata = os.path.dirname(os.path.dirname(__file__)) + '/collectiveintelligence_book_master/blogdata.txt'
print (blogdata)
class Clustering :

    def __init__(self):
        blogname, words, data = clusters.readfile(blogdata)
        Info("{} --> {} --> {}".format(type(blogname), len(blogname), blogname ))
        Info("{} --> {} --> {}".format(type(words), len(words), words))
        Info("{} --> {} --> {}".format(type(data), len(data), data))

        clust = clusters.hcluster(data)




if __name__ == '__main__':
    Clustering()
