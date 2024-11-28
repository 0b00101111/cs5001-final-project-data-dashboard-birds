import pandas as pd

class SnowyOwlTrend:
    """
    Represent the data of the trend of the amount of snowy owls in
    Canada.
    """
    def __init__(self, dataframe):
        self.data = dataframe


    def peek_the_data(self, n=10):
        """
        Display the top n entries of the dataframe.
        """
        try:
            peek_data = self.data.head(n)
            print(f"Displaying the top {n} entries of the dataframe.")
            print(peek_data)
            return peek_data
        except Exception as e:
            print(f"Error while peeking the data: {e}")
            return pd.DataFrame()


    def get_descriptive_summary(self):
        """
        Return a descriptive summary of the dataframe.
        """
        return self.data.describe()


