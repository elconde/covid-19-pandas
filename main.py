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
    dataset = pandas.read_csv(csv_file_name)
    dataframe = pandas.DataFrame(dataset)
    dataframe.drop(['Lat', 'Long'], axis=1, inplace=True)
    dataframe_us = (
        dataframe[
            (dataframe['Country/Region'] == 'US') &
            (dataframe['Province/State'].str.contains('New York', na=False))
        ]
    ).drop(['Country/Region'], axis=1).transpose()
    dataframe_us.columns = dataframe_us.iloc[0]
    dataframe_us.drop(dataframe_us.index[0], inplace=True)
    dataframe_us = dataframe_us.loc[(dataframe_us.sum(axis=1) != 0)]
    dataframe_us = dataframe_us.apply(pandas.to_numeric)
    dataframe_us.interpolate(inplace=True)
    dataframe_us.plot.line()
    pyplot.show()


if __name__ == '__main__':
    main()