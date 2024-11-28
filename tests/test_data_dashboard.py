import unittest
import pandas as pd

from data_dashboard import (
    download_csv,
    parse_csv,
    load_csv_into_dataframe,
    clean_data_for_observation,
    clean_data_for_population,
    analyze_correlation,
    interpret_correlation
    )

from ..classes.bird_observation import BirdObservation
from ..classes.snowy_owl_trend import SnowyOwlTrend


class TestDataDashboardFunctions(unittest.TestCase):
    def test_download_csv(self):
        # Use the iris dataset to test it
        url = "https://raw.githubusercontent.com/uiuc-cse/data-fa14/gh-pages/data/iris.csv"
        result = download_csv(url)
        self.assertIsNotNone(result)
        self.assertIn("sepal_length", result)


    def test_download_csv_failure(self):
        # Use an invalid URL to test failure
        url = 'http://nonexistentdomain.abc/invalid.csv'
        result = download_csv(url)
        self.assertIsNone(result)


    def test_parse_csv(self):
        csv_content = ('col1,col2,col3,col4\nval1,val2,val3,'
                       'val4\nval5,val6,val7,val8')
        expected = [
                {'col1': 'val1', 'col2': 'val2', 'col3': 'val3', 'col4': 'val4'},
                {'col1': 'val5', 'col2': 'val6', 'col3': 'val7', 'col4': 'val8'},
                ]
        result = parse_csv(csv_content)
        self.assertEqual(expected, result)


    def test_parse_csv_empty(self):
        csv_content = ''
        expected = []
        result = parse_csv(csv_content)
        self.assertEqual(expected, result)


    def test_load_csv_into_dataframe(self):
        data_list = [
                {'col1': 'val1', 'col2': 'val2', 'col3': 'val3'},
                {'col1': 'val4', 'col2': 'val5', 'col3': 'val6'}
                ]
        result = load_csv_into_dataframe(data_list)
        expected_pf = pd.DataFrame(data_list)
        pd.testing.assert_frame_equal(result, expected_pf)


    def test_clean_data_for_observation(self):
        df = pd.DataFrame({
            'OBSERVATION COUNT': ['1', '2', 'X', 'invalid']
        })
        result = clean_data_for_observation(df)
        expected_df = pd.DataFrame({
            'OBSERVATION COUNT': [1.0, 2.0, 1.0, None]
        })
        pd.testing.assert_frame_equal(result.reset_index(drop=True), expected_df)


    def test_clean_data_for_population(self):
        df = pd.DataFrame({
            'Year': ['2000', '2001', '2002', '2003'],
            'Index': ['10', '20', '30', None],
            'Lower CI': ['5', None, '15', '25'],
            'Upper CI': ['15', '25', '35', 'invalid']
        })
        result = clean_data_for_population(df)
        expected_df = pd.DataFrame({
            'Year': [2000, 2002],
            'Index': [10.0, 30.0],
            'Lower CI': [5.0, 15.0],
            'Upper CI': [15.0, 35.0]
        })
        pd.testing.assert_frame_equal(result.reset_index(drop=True), expected_df)


    def test_interpret_correlation(self):
        self.assertEqual(interpret_correlation(0.8), 'strong positive')
        self.assertEqual(interpret_correlation(0.5), 'moderate positive')
        self.assertEqual(interpret_correlation(0.2), 'weak positive')
        self.assertEqual(interpret_correlation(-0.2), 'weak negative')
        self.assertEqual(interpret_correlation(-0.5), 'moderate negative')
        self.assertEqual(interpret_correlation(-0.8), 'strong negative')


    def test_analyze_correlation(self):
        observation_data = pd.DataFrame({
            'OBSERVATION DATE': ['2000-01-01', '2001-01-01', '2002-01-01'],
            'OBSERVATION COUNT': [10, 20, 30]
        })
        bird_observation = BirdObservation(observation_data)

        # Clean and aggregate
        bird_observation.data['OBSERVATION COUNT'] = pd.to_numeric(
            bird_observation.data['OBSERVATION COUNT'], errors='coerce')
        bird_observation.data['Year'] = pd.to_datetime(
            bird_observation.data['OBSERVATION DATE'], errors='coerce').dt.year

        trend_data = pd.DataFrame({
            'Year': [2000, 2001, 2002],
            'Index': [100, 200, 300],
            'Lower CI': [90, 190, 290],
            'Upper CI': [110, 210, 310]
        })
        snowy_owl_trend = SnowyOwlTrend(trend_data)

        result = analyze_correlation(bird_observation, snowy_owl_trend)
        expected_interpretation = interpret_correlation(1.0)
        expected_result = {
            'Correlation Coefficient': 1.0,
            'Interpretation': expected_interpretation
        }
        self.assertEqual(result, expected_result)

class TestBirdObservation(unittest.TestCase):
    def setUp(self):
        self.data = pd.DataFrame({
            'OBSERVATION DATE': ['2000-01-01', '2000-01-02', '2000-01-03'],
            'OBSERVATION COUNT': [1, 2, 3]
        })
        self.bird_observation = BirdObservation(self.data)

    def test_peek_the_data(self):
        result = self.bird_observation.peek_the_data(n=2)
        expected = self.data.head(2)
        pd.testing.assert_frame_equal(result.reset_index(drop=True), expected.reset_index(drop=True))

    def test_get_descriptive_summary(self):
        result = self.bird_observation.get_descriptive_summary()
        expected = self.data.describe()
        pd.testing.assert_frame_equal(result, expected)

    def test_aggregate_observations_by_year(self):
        result = self.bird_observation.aggregate_observations_by_year()
        expected = pd.DataFrame({
            'Year': [2000],
            'OBSERVATION COUNT': [6]
        })
        # Convert 'Year' columns to int64
        result['Year'] = result['Year'].astype('int64')
        expected['Year'] = expected['Year'].astype('int64')

        pd.testing.assert_frame_equal(result.reset_index(drop=True), expected.reset_index(drop=True))

    def test_aggregate_observations_by_location(self):
        self.data['STATE'] = ['State1', 'State1', 'State2']
        self.data['COUNTY'] = ['County1', 'County2', 'County1']
        self.bird_observation.data = self.data
        result = self.bird_observation.aggregate_observations_by_location()
        expected = self.data.groupby(['STATE', 'COUNTY'])['OBSERVATION COUNT'].sum().reset_index()
        pd.testing.assert_frame_equal(result, expected)

    def test_get_data_by_state_found(self):
        self.data['STATE'] = ['State1', 'State2', 'State1']
        self.bird_observation.data = self.data
        result = self.bird_observation.get_data_by_state('State1')
        expected = self.data[self.data['STATE'].str.lower() == 'state1'.lower()]
        pd.testing.assert_frame_equal(result.reset_index(drop=True), expected.reset_index(drop=True))

    def test_get_data_by_state_not_found(self):
        self.data['STATE'] = ['State1', 'State2', 'State1']
        self.bird_observation.data = self.data
        result = self.bird_observation.get_data_by_state('State3')
        self.assertTrue(result.empty)

    def test_aggregate_observations_by_year_missing_date(self):
        # Remove 'OBSERVATION DATE' column to simulate error
        self.data = self.data.drop(columns=['OBSERVATION DATE'])
        self.bird_observation.data = self.data
        result = self.bird_observation.aggregate_observations_by_year()
        self.assertTrue(result.empty)

class TestSnowyOwlTrend(unittest.TestCase):

    def setUp(self):
        self.data = pd.DataFrame({
            'Year': [2000, 2001, 2002],
            'Index': [100, 200, 300],
            'Lower CI': [90, 190, 290],
            'Upper CI': [110, 210, 310]
        })
        self.snowy_owl_trend = SnowyOwlTrend(self.data)

    def test_peek_the_data(self):
        result = self.snowy_owl_trend.peek_the_data(n=2)
        expected = self.data.head(2)
        pd.testing.assert_frame_equal(result.reset_index(drop=True), expected.reset_index(drop=True))

    def test_get_descriptive_summary(self):
        result = self.snowy_owl_trend.get_descriptive_summary()
        expected = self.data.describe()
        pd.testing.assert_frame_equal(result, expected)


if __name__ == '__main__':
    unittest.main()