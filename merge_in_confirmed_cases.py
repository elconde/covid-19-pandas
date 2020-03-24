"""Merge the confirmed cases generated by ny_data_scraper.py into
COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv
"""
import csv
import os
import logging
import tempfile

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
    return pandas.read_csv(
        OUTPUT_CSV_FILE_NAME, dtype={'Lat': str, 'Long': str}
    )


def merge_in_confirmed_cases():
    """Merge in confirmed cases"""
    input_data = get_input_data()
    output_data = get_output_data()
    for row in input_data.itertuples():
        if row.Location != 'New York City':
            province = row.Location+' County, NY'
        else:
            # New York County means all five boroughs!
            province = 'New York County, NY'
        cases = row.Count.replace(',', '')
        formatted_date = (
            '{dt.month}/{dt.day}/{dt:%y}'.format(dt=row.Timestamp)
        )
        existing_dataframe = output_data.loc[
            (output_data['Country/Region'] == 'US') &
            (output_data['Province/State'] == province)
        ]
        if existing_dataframe.empty:
            continue
        output_data.at[existing_dataframe.index[0], formatted_date] = cases
    output_data.to_csv(OUTPUT_CSV_FILE_NAME, index=False)
    post_process()


def post_process_row(row, field_names):
    """Clean up this one row"""
    # Last column should be integer
    last_column_value = row[field_names[-1]]
    if last_column_value:
        row[field_names[-1]] = int(float(last_column_value))
    return row


def post_process():
    """Clean up the output file"""
    with open(OUTPUT_CSV_FILE_NAME) as output_csv_file:
        reader = csv.DictReader(output_csv_file)
        rows = [row for row in reader]
        field_names = reader.fieldnames
    tmp_handle, tmp_full_name = tempfile.mkstemp(suffix='.csv')
    os.close(tmp_handle)
    with open(OUTPUT_CSV_FILE_NAME, 'w') as tmp_file:
        writer = csv.DictWriter(tmp_file, field_names)
        writer.writeheader()
        for row in rows:
            writer.writerow(post_process_row(row, field_names))


def main():
    """Set up the logger and merge in the file"""
    setup_logger()
    merge_in_confirmed_cases()


if __name__ == '__main__':
    main()
