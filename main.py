# Load libraries
import pandas
from pandas.plotting import scatter_matrix
from matplotlib import pyplot
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
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
            (~dataframe['Province/State'].str.contains(',', na=False))
        ]
    ).drop(['Country/Region'], axis=1).transpose()
    dataframe_us.columns = dataframe_us.iloc[0]
    dataframe_us.drop(dataframe_us.index[0], inplace=True)
    dataframe_us = dataframe_us.loc[(dataframe.sum(axis=0) != 0)]
    print(dataframe_us)
    dataframe_us.plot.line()
    pyplot.show()


if __name__ == '__main__':
    main()