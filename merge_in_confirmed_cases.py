"""Merge the confirmed cases generated by ny_data_scraper.py into
COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv
"""
import datetime
import os
import logging

import pandas

COUNTIES_EX_NYC = [
    'Albany', 'Allegany', 'Broome', 'Cattaraugus', 'Cayuga', 'Chautauqua',
    'Chemung', 'Chenango', 'Clinton', 'Columbia', 'Cortland', 'Delaware',
    'Dutchess', 'Erie', 'Essex', 'Franklin', 'Fulton', 'Genesee', 'Greene',
    'Hamilton', 'Herkimer', 'Jefferson', 'Lewis', 'Livingston', 'Madison',
    'Monroe', 'Montgomery', 'Nassau', 'Niagara', 'Oneida', 'Onondaga',
    'Ontario', 'Orange', 'Orleans', 'Oswego', 'Otsego', 'Putnam', 'Rensselaer',
    'Rockland', 'St. Lawrence', 'Saratoga', 'Schenectady', 'Schoharie',
    'Schuyler', 'Seneca', 'Steuben', 'Suffolk', 'Sullivan', 'Tioga',
    'Tompkins', 'Ulster', 'Warren', 'Washington', 'Wayne', 'Westchester',
    'Wyoming', 'Yates'
]
NYC_COUNTIES = ['Bronx', 'New York', 'Richmond', 'Kings', 'Queens']

LOGGER = logging.getLogger('merge_in_confirmed_cases')

INPUT_CSV_FILE_NAME = os.path.join(
    os.path.dirname(__file__), 'ny_confirmed_cases.csv'
)
OUTPUT_CSV_FILE_NAME = os.path.join(
    os.path.dirname(__file__), 'COVID-19',
    'csse_covid_19_data', 'csse_covid_19_time_series',
    'time_series_19-covid-Confirmed.csv'
)


def setup_logger():
    """Set up the logger"""
    logging.basicConfig(
        level=logging.NOTSET, format='%(asctime) %(message)s'
    )


def validate_and_correct_counties(data):
    """Make sure there are no spurious counties. Make corrections if
    possible."""
    # Broom -> Broome typo
    data.replace('Broom', 'Broome', inplace=True)
    # New York City counties are not counted individually for some reason
    counties = COUNTIES_EX_NYC + ['New York City']
    for county in data['Location'].drop_duplicates():
        assert county in counties, county+': Invalid county!'
        assert county not in NYC_COUNTIES, county+(
            ': NYC counties are grouped together as "New York City"'
        )


def get_input_data():
    """Get the input data :-)"""
    input_data = pandas.read_csv(INPUT_CSV_FILE_NAME, parse_dates=[2]).sort_values(
        ['Location', 'Timestamp']
    )
    # Remove time portion
    input_data['Timestamp'] = input_data['Timestamp'].dt.date
    # Remove total
    input_data = input_data[~input_data['Location'].str.startswith('Total')]
    # Keep only the latest data for each date
    input_data.drop_duplicates(
        ['Timestamp', 'Location'], keep='last', inplace=True
    )
    validate_and_correct_counties(input_data)
    return input_data


def get_output_data():
    """Get the output data :-)"""
    return pandas.read_csv(OUTPUT_CSV_FILE_NAME)


def merge_in_confirmed_cases():
    """Merge in confirmed cases"""
    input_data = get_input_data()
    output_data = get_output_data()
    output_ny_data = (
        output_data[
            (output_data['Country/Region'] == 'US') &
            (output_data['Province/State'].str.contains(', NY'))
        ]
    )
    for row in input_data.itertuples():
        county = row.Location+' County, NY'
        cases = row.Count
        formatted_date = (
            '{dt.month}/{dt.day}/{dt:%y}'.format(dt=row.Timestamp)
        )
        output_row = output_ny_data[
            output_ny_data['Province/State'] == county
        ]
        if output_row.empty:
            continue
        print(output_row[formatted_date])
    print(output_ny_data)

def main():
    """Set up the logger and merge in the file"""
    setup_logger()
    merge_in_confirmed_cases()


if __name__ == '__main__':
    main()
