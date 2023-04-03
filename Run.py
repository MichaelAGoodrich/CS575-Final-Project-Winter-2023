# Run.py. Place that Mike uses to experiment with code.
def main():
    from DatabaseManager import DatabaseManager # I don't know if it's good form to do this or not
    database = DatabaseManager('datasets/suicide_rates_by_category.csv')
    database.printDatabaseOverview()

main()