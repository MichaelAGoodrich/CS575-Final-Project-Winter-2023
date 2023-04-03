""" Database manager
        Reads .csv file into pandas dataframe
        Extracts genres, movies, MPAA ratings, actors, and directors
        Finds relationships between various elements.

        https://www.kaggle.com/datasets/russellyates88/suicide-rates-overview-1985-to-2016

        CS 575 Class
        Brigham Young University

        April 2023

"""
import pandas as pd

class DatabaseManager:
    def __init__(self,file_name):
        self.dataframe = pd.read_csv(file_name)
    
    ###############################
    # Public Extraction Utilities #
    ###############################
    def printDatabaseOverview(self):
        self.__showHead()
        self.__showInfo()

    def getNodesOfType(self,category):
        """ An object of interest is identified by a node """
        ### Returns a dictionary indexed by node_type with corresponding label 
        if category not in set(self.dataframe.columns): raise ValueError
        
        node_set = set()
        entries = self.dataframe[category]
        for i in range(len(entries)):
            iterator = self.__getCategoryIterator(category,entries[i])
            for entry in iterator:
                node_set.add(entry)
        return node_set
    def getEdges(self,category_1, category_2):
        """ A pairwise relationship is identified by an edge """
        ### Step 1: Error check
        if category_1 not in set(self.dataframe.columns) or category_2 not in set(self.dataframe.columns): raise ValueError
        if category_1 == category_2: raise ValueError
        
        ### Step 2: Identify pairwise relationships
        entries_1 = self.dataframe[category_1]
        entries_2 = self.dataframe[category_2]
        set_of_edges = set()
        for i in range(len(entries_1)):
            iterator_1 = self.__getCategoryIterator(category_1,entries_1[i])
            iterator_2 = self.__getCategoryIterator(category_2,entries_2[i])
            for e1 in iterator_1:
                for e2 in iterator_2:
                    set_of_edges.add((str(e1),str(e2)))
        return set_of_edges

    ##############################
    # Private Overview Utilities #
    ##############################
    def __showHead(self): 
        # This function returns the first n rows for the object based on position. 
        # It is useful for quickly testing if your object has the right type of data in it.
        # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.head.html
        print(self.dataframe.head())
    def __showInfo(self):
        # This method prints information about a DataFrame including the index dtype and 
        # columns, non-null values and memory usage.
        # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.info.html
        print(self.dataframe.info())

    ################################
    # Private Extraction Utilities #
    ################################
    def __getCategoryIterator(self,category,value):
        if category in {'genre','writers','directors','casts'}:
            my_iterator = set(value.split(','))
        else:
            my_iterator = {value,} # Notice the trailing comma. Necessary to allow iteration
        return my_iterator