# Run.py. Place that Mike uses to experiment with code.
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np 

def main():
    from DatabaseManager import DatabaseManager # I don't know if it's good form to do this or not
    database = DatabaseManager('datasets/suicide_rates_by_category.csv')
    database.printDatabaseOverview()

    # Code patterned after https://www.kaggle.com/code/chingchunyeh/suicide-rates-overview-1985-to-2016
    # Getting a feel for how to bin up the suicide rate
    df = pd.read_csv('datasets/suicide_rates_by_category.csv')
    df.rename(columns={"suicides/100k pop":"suicides_per_100k","HDI for year":"HDI_for_year",
                    " gdp_for_year ($) ":"gdp_for_year"," gdp_per_capita ($) ":"gdp_per_capita",
                        "gdp_per_capita ($)":"gdp_per_capita"}, inplace=True)
    sns.histplot(data=df,x="suicides_per_100k")
    plt.show()


main()