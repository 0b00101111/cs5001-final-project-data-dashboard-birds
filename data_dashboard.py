import pandas as pd
import requests
import csv
from classes.bird_observation import BirdObservation
from classes.snowy_owl_trend import SnowyOwlTrend
import tkinter as tk

from visualizations import (
    plot_observations_by_year,
    plot_correlation,
    plot_monthly_observations,
    interpret_correlation,
    plot_population_trend
    )

from gui import DataDashboardGUI


# Download, parse and load data.
def download_csv(url):
    """
    Download the csv file from given url.
    """
    try:
        response = requests.get(url)
        csv_content = response.content.decode('utf-8')
        print(f"Data downloaded successfully from {url}.")
        return csv_content
    except requests.exceptions.RequestException as e:
        print(f"Error while downloading data from {url}: {e}")
        return None


def parse_csv(csv_content):
    """
    Parse the csv file to a list of dictionaries.
    """
    try:
        csv_lines = csv_content.strip().split('\n')
        reader = csv.DictReader(csv_lines)
        data_list = [row for row in reader]
        return data_list
    except csv.Error as e:
        print(f"CSV parsing error: {e}")
        return []
    except TypeError as te:
        print(f"Type error while parsing CSV: {te}")
        return []
    except Exception as e:
        print(f"Unexpected error while parsing CSV: {e}")
        return []


def load_csv_into_dataframe(data_list):
    try:
        df = pd.DataFrame(data_list)
        # strip whitespace from column names
        df.columns = df.columns.str.strip()
        return df
    except TypeError as te:
        print(f"Type error while loading data into DataFrame: {te}")
        return None
    except ValueError as ve:
        print(f"Value error while loading data into DataFrame: {ve}")
        return None
    except Exception as e:
        print(
            f"Unexpected error while loading data into DataFrame: {e}")
        return None


# Clean the data
def clean_data_for_observation(bird_observations_df):
    """
    Clean the data to get correct data types.
    """
    try:
        # Replace 'X' with 1 in 'OBSERVATION COUNT' and convert to numeric
        bird_observations_df['OBSERVATION COUNT'] = bird_observations_df['OBSERVATION COUNT'].replace('X', 1)
        bird_observations_df['OBSERVATION COUNT'] = pd.to_numeric(
                bird_observations_df['OBSERVATION COUNT'], errors='coerce')

        # Convert 'OBSERVATION DATE' to datetime format
        bird_observations_df['OBSERVATION DATE'] = pd.to_datetime(
                bird_observations_df['OBSERVATION DATE'],
                errors='coerce'
                )

        # Drop rows with invalid 'OBSERVATION DATE'
        bird_observations_df = bird_observations_df.dropna(
            subset=['OBSERVATION DATE']).reset_index(drop=True)

        # Extract 'Year', 'Month', and 'Day' from 'OBSERVATION DATE'
        bird_observations_df['Year'] = bird_observations_df[
            'OBSERVATION DATE'].dt.year
        bird_observations_df['Month'] = bird_observations_df[
            'OBSERVATION DATE'].dt.month
        bird_observations_df['Day'] = bird_observations_df[
            'OBSERVATION DATE'].dt.day

        return bird_observations_df

    except KeyError as ke:
        print(f"Key error while cleaning data: {ke}")
        return bird_observations_df
    except ValueError as ve:
        print(f"Value error while cleaning data: {ve}")
        return bird_observations_df
    except Exception as e:
        print(f"Unexpected error while cleaning data: {e}")
        return bird_observations_df


def clean_data_for_population(population_trend_df):
    """
    Clean the population trend data by removing rows with missing or
    invalid data in 'Index', 'Lower CI', or 'Upper CI'.
    """
    try:
        # Convert columns to numeric values
        population_trend_df['Year'] = pd.to_numeric(
                population_trend_df['Year'], errors='coerce')
        population_trend_df['Index'] = pd.to_numeric(
                population_trend_df['Index'], errors='coerce')
        population_trend_df['Lower CI'] = pd.to_numeric(
                population_trend_df['Lower CI'], errors='coerce')
        population_trend_df['Upper CI'] = pd.to_numeric(
                population_trend_df['Upper CI'], errors='coerce')

        # Sort the data by year
        population_trend_df = population_trend_df.sort_values(
            'Year').reset_index(drop=True)

        # Drop any row with missing value.
        population_trend_df = population_trend_df.dropna(
                subset=['Index', 'Lower CI', 'Upper CI']
                )
        population_trend_df = population_trend_df.reset_index(drop=True)
        return population_trend_df

    except KeyError as ke:
        print(f"Key error while cleaning population data: {ke}")
        return population_trend_df
    except ValueError as ve:
        print(f"Value error while cleaning population data: {ve}")
        return population_trend_df
    except Exception as e:
        print(f"Unexpected error while cleaning population data: {e}")
        return population_trend_df


# Analyse data
def analyze_correlation(bird_observation, snowy_owl_trend):
    """
    Analyzes the correlation between bird observations and snowy
    owl population trend.
    """
    try:
        observations_per_year = bird_observation.aggregate_observations_by_year()
        trend_data = snowy_owl_trend.data.copy()
        if ('Year' not in trend_data.columns or 'Index' not in
                trend_data.columns):
            return {}


        merged_data = pd.merge(observations_per_year, trend_data,
                               on='Year', how='inner')
        if merged_data.empty:
            print("No data of mutual years for analysis.")
            return {}

        correlation_coefficient = merged_data[('OBSERVATION '
                                               'COUNT')].corr(
                merged_data['Index'], method='pearson')
        print(f"Pearson correlation coefficient: {correlation_coefficient}")

        interpretation = interpret_correlation(correlation_coefficient)

        correlation_results = {
                'Correlation Coefficient': correlation_coefficient,
                'Interpretation': interpretation
                }

        return correlation_results

    except KeyError as ke:
        print(f"Key error while analyzing correlation: {ke}")
        return {}
    except ValueError as ve:
        print(f"Value error while analyzing correlation: {ve}")
        return {}
    except Exception as e:
        print(f"Unexpected error while analyzing correlation: {e}")
        return {}


def main():
    """
    Download, load and analyze the correlation between bird
    observations and the population trend of snowy owl.
    """
    bird_observation_url = 'https://raw.githubusercontent.com/0b00101111/cs5001-final-project-data-dashboard-birds/refs/heads/main/snowy_owl_record.csv'
    population_trend_url = 'https://raw.githubusercontent.com/0b00101111/cs5001-final-project-data-dashboard-birds/refs/heads/main/snowy_owl_trend.csv'

    # download the data
    bird_observations_csv = download_csv(bird_observation_url)
    population_trend_csv = download_csv(population_trend_url)

    # Parse and load the data into DataFrames
    bird_data_list = parse_csv(bird_observations_csv)
    bird_observations_df = load_csv_into_dataframe(bird_data_list)

    population_data_list = parse_csv(population_trend_csv)
    population_trend_df = load_csv_into_dataframe(population_data_list)

    # Clean the data
    bird_observations_df = clean_data_for_observation(bird_observations_df)
    population_trend_df = clean_data_for_population(population_trend_df)

    # initialize the class of the observation data
    bird_observation = BirdObservation(bird_observations_df)

    # Peek the observation data
    bird_observation_peek = bird_observation.peek_the_data()
    print(bird_observation_peek)

    # Provide a descriptive summary for observation data.
    descriptive_summary_observation = bird_observation.get_descriptive_summary()
    print(descriptive_summary_observation)

    # initialize the class of the population trend data
    snowy_owl_trend = SnowyOwlTrend(population_trend_df)

    # Peek the population trend data
    population_trend_peek = snowy_owl_trend.peek_the_data()
    print(population_trend_peek)

    # Provide a descriptive summary for population data.
    descriptive_summary_population = snowy_owl_trend.get_descriptive_summary()
    print(descriptive_summary_population)

    # Analyse the correction of observation and population
    correlation_results = analyze_correlation(bird_observation, snowy_owl_trend)
    print(correlation_results)

    # Plot the visualizations (commented out when run the GUI)
    # plot_observations_by_year(bird_observation)
    # plot_monthly_observations(bird_observation)
    # plot_population_trend(snowy_owl_trend)  # Add this line if you want to plot automatically
    # plot_correlation(bird_observation, snowy_owl_trend)

    # Init and run the GUI
    root = tk.Tk()
    app = DataDashboardGUI(root, bird_observation, snowy_owl_trend)
    app.run()

if __name__ == '__main__':
    main()

