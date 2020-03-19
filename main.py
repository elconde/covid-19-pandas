# Load libraries
import pandas
import matplotlib.pyplot
import os

PROJECT_DIR = os.path.dirname(__file__)


def plot_nyc(dataframe):
    """Plot New York City"""
    dataframe = (
        dataframe[
            (dataframe['Country/Region'] == 'US') &
            (dataframe['Province/State'].str.contains('New York', na=False))
            ]
    ).drop(['Country/Region'], axis=1).transpose()
    dataframe.columns = dataframe.iloc[0]
    dataframe.drop(dataframe.index[0], inplace=True)
    dataframe = dataframe.loc[(dataframe.sum(axis=1) != 0)]
    dataframe = dataframe.apply(pandas.to_numeric)
    dataframe.interpolate(inplace=True)
    dataframe.plot.line()
    matplotlib.pyplot.show()


def plot_us_vs_china(dataframe):
    """Plot NYC vs. China."""
    dataframe = dataframe.groupby(['Country/Region']).sum().transpose()
    first_nonzero_idx = (dataframe['US'].nonzero()[0][0])
    dataframe['US'] = dataframe['US'].shift(-first_nonzero_idx)
    dataframe.plot.line()
    matplotlib.pyplot.show()


def main():
    """Main"""
    dataframe = read_csv()
    # plot_top_ten(dataframe)
    # plot_nyc(dataframe)
    plot_us_vs_china(dataframe)


def plot_top_ten(dataframe):
    """Plot the top ten infected countries."""
    dataframe = remove_us_counties(dataframe).groupby(['Country/Region']).sum()
    # Get the 10 largest
    dataframe = dataframe.nlargest(10, dataframe.columns[-1])
    # Plot
    dataframe.transpose().plot.line()
    matplotlib.pyplot.show()


def remove_us_counties(dataframe):
    """Remove U.S. counties which are already included in state data"""
    dataframe: pandas.DataFrame = dataframe[
        ~(dataframe['Province/State'].str.contains(',', na=False))
    ]
    return dataframe


def read_csv():
    """Read the CSV file and return the dataframe"""
    csv_file_name = os.path.join(
        PROJECT_DIR, 'COVID-19', 'csse_covid_19_data',
        'csse_covid_19_time_series', 'time_series_19-covid-Confirmed.csv'
    )
    dataframe = pandas.DataFrame(pandas.read_csv(csv_file_name))
    dataframe.drop(['Lat', 'Long'], axis=1, inplace=True)
    return dataframe


if __name__ == '__main__':
    main()