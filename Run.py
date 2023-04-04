# Run.py. Place that Mike uses to experiment with code.
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np 

def main():
    # Exercise the necessary parts of the Database manager
    from DatabaseManager import DatabaseManager # I don't know if it's good form to do this or not
    database = DatabaseManager('datasets/suicide_rates_by_category.csv')
    database.printDatabaseOverview()
    database.showUniqueNodesOfType('generation')
    database.cleanDatabase()
    database.showUniqueNodesOfType('generation')
    database.binCategory('suicides_per_100k',binlist = [0,25,75,100,125,150,300])
    database.showUniqueNodesOfType('suicides_per_100k_bins')
    del database

    # Extract a knowledge graph

main()