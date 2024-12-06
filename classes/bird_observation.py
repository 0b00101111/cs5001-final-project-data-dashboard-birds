import pandas as pd

class BirdObservation:
    """
    Represent the observation records of Snowy Owls from ebird.
    """
    def __init__(self, dataframe: pd.DataFrame):
        """
        Initialize an instance  with a dataframe and load the data.
        """
        if not isinstance(dataframe, pd.DataFrame):
            raise TypeError(
                "The provided data must be a pandas DataFrame.")

        self.data = dataframe

    def peek_the_data(self, n=10):
        """
        Display the top 'n' entries of the records.
        """
        try:
            peek_data = self.data.head(n)
            print(f"Displaying the top {n} entries of the records...")
            print(peek_data)
            return peek_data
        except Exception as e:
            print(f"Error while peeking the records: {e}")
            return pd.DataFrame()

    def get_descriptive_summary(self):
        """
        Return a descriptive summary of the data.
        """
        return self.data.describe()

    def aggregate_observations_by_year(self):
        """
        Aggregate the observation records by year.
        """
        try:
            # convert the observation date to a datetime format and
            # get the year.
            self.data['Year'] = pd.to_datetime(self.data[
                                                   'OBSERVATION '
                                                   'DATE'],
                                               errors='coerce').dt.year
            observations_per_year = self.data.groupby('Year')[
                'OBSERVATION COUNT'].sum().reset_index()
            return observations_per_year
        except Exception as e:
            print(f"Error while aggregating observations: {e}")
            return pd.DataFrame()

    def aggregate_observations_by_location(self):
        """
        Aggregate the observation records by location, grouped by
        states and counties.
        """
        try:
            aggregation = self.data.groupby(['STATE', 'COUNTY'])[
                'OBSERVATION COUNT'].sum().reset_index()
            return aggregation
        except Exception as e:
            print(f"Error while aggregating observations: {e}")
            return pd.DataFrame()


    def get_data_by_state(self, state):
        """
        Retrieve records for a certain state.
        """
        try:
            state_data = self.data[
                self.data['STATE'].str.lower() == state.lower()]
            if state_data.empty:
                print(f"State '{state}' not found.")
            else:
                print(f"Retrieved data for state: {state}")
            return state_data
        except Exception as e:
            print(f"Error while retrieving data: {e}")

