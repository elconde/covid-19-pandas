# Load libraries
import pandas
from matplotlib import pyplot
import os

PROJECT_DIR = os.path.dirname(__file__)


def main():
    """Load dataset"""
    csv_file_name = os.path.join(
        PROJECT_DIR, 'COVID-19', 'csse_covid_19_data',
        'csse_covid_19_time_series', 'time_series_19-covid-Confirmed.csv'
    )
    dataframe = pandas.DataFrame(pandas.read_csv(csv_file_name))
    dataframe.drop(['Lat', 'Long'], axis=1, inplace=True)
    # Get rid of U.S. counties
    dataframe: pandas.DataFrame = dataframe[
        ~(dataframe['Province/State'].str.contains(',', na=False))
    ]
    # Group by country
    dataframe = dataframe.groupby(['Country/Region']).sum()
    # Get the 10 largest
    dataframe = dataframe.nlargest(10, dataframe.columns[-1])
    # Plot
    dataframe.transpose().plot.line()
    pyplot.show()


if __name__ == '__main__':
    main()