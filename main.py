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
    dataset = pandas.read_csv(csv_file_name).transpose()
    dataframe = pandas.DataFrame(dataset)
    dataframe.drop(['Lat', 'Long'],axis='index', inplace=True)
    dataframe.columns = dataframe.iloc[1]
    dataframe.drop(dataframe.index[1], inplace=True)
    columns = [column for column in dataframe.columns if column == 'US']
    dataframe = dataframe[columns]
    print(dataframe)


if __name__ == '__main__':
    main()