import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import pandas as pd


def plot_observations_by_year(bird_observation):
    """
    Generate a bar chart of Snowy Owl observations by year.

    Parameters:
    bird_observation (BirdObservation): An instance of BirdObservation class.

    Returns:
    matplotlib.figure.Figure: The generated plot figure.
    """
    try:
        # Get aggregated data
        observations_per_year = bird_observation.aggregate_observations_by_year()

        # Drop years with missing data and convert 'Year' to integers
        observations_per_year = observations_per_year.dropna(subset=['Year'])
        observations_per_year['Year'] = observations_per_year['Year'].astype(int)

        # Sort data by 'Year'
        observations_per_year = observations_per_year.sort_values('Year')

        # Create the figure and axis
        fig, ax = plt.subplots(figsize=(4, 2))
        fig.tight_layout()

        # Set background color to match GUI
        fig.patch.set_facecolor('#ECECEC')
        ax.set_facecolor('#ECECEC')

        # Create the bar chart
        ax.bar(
            observations_per_year['Year'],
            observations_per_year['OBSERVATION COUNT'],
            color='skyblue'
        )
        ax.set_xlabel('Year', fontsize=10)
        ax.set_ylabel('Total Observations', fontsize=10)
        ax.set_title('Snowy Owl Observations by Year', fontsize=12)
        ax.tick_params(axis='x', rotation=45)
        ax.grid(axis='y', linestyle='--', alpha=0.5)

        return fig

    except Exception as e:
        print(f"Error while plotting observations by year: {e}")
        return None


def plot_monthly_observations(bird_observation):
    """
    Generate a line chart of Snowy Owl observations by month.

    Parameters:
    bird_observation (BirdObservation): An instance of BirdObservation class.

    Returns:
    matplotlib.figure.Figure: The generated plot figure.
    """
    try:
        # Ensure date components are extracted
        if 'Month' not in bird_observation.data.columns:
            bird_observation.data['Month'] = bird_observation.data['OBSERVATION DATE'].dt.month

        # Aggregate observations by month
        observations_per_month = bird_observation.data.groupby('Month')['OBSERVATION COUNT'].sum().reset_index()

        # Sort by Month
        observations_per_month = observations_per_month.sort_values('Month')

        # Create the figure and axis
        fig, ax = plt.subplots(figsize=(4, 2))

        # Set background color to match GUI
        fig.patch.set_facecolor('#ECECEC')
        ax.set_facecolor('#ECECEC')

        # Plotting
        ax.plot(
            observations_per_month['Month'],
            observations_per_month['OBSERVATION COUNT'],
            marker='o',
            linestyle='-',
            color='seagreen'
        )
        ax.set_xlabel('Month', fontsize=10)
        ax.set_ylabel('Total Observations', fontsize=10)
        ax.set_title('Snowy Owl Observations by Month', fontsize=12)
        ax.set_xticks(range(1, 13))
        ax.grid(True, linestyle='--', alpha=0.5)

        return fig

    except Exception as e:
        print(f"Error while plotting monthly observations: {e}")
        return None


def plot_population_trend(snowy_owl_trend):
    """
    Generate a line chart of the Population Index trend with confidence intervals.

    Parameters:
    snowy_owl_trend (SnowyOwlTrend): An instance of SnowyOwlTrend class.

    Returns:
    matplotlib.figure.Figure: The generated plot figure.
    """
    try:
        # Extract relevant data
        trend_data = snowy_owl_trend.data.copy()

        # Ensure data is sorted by Year
        trend_data = trend_data.sort_values('Year')

        # Create the figure and axis
        fig, ax = plt.subplots(figsize=(4, 2))
        fig.tight_layout()

        # Set background color to match GUI
        fig.patch.set_facecolor('#ECECEC')
        ax.set_facecolor('#ECECEC')

        # Plot Population Index
        ax.plot(trend_data['Year'], trend_data['Index'], color='indianred',
                marker='o', label='Population Index')

        # Plot Confidence Interval
        ax.fill_between(trend_data['Year'],
                        trend_data['Lower CI'],
                        trend_data['Upper CI'],
                        color='mistyrose',
                        alpha=0.5,
                        label='Confidence Interval')

        # Set labels and title
        ax.set_xlabel('Year', fontsize=10)
        ax.set_ylabel('Population Index', fontsize=10)
        ax.set_title('Snowy Owl Population Index Trend Over Years', fontsize=12)
        ax.legend(fontsize=8)
        ax.grid(True, linestyle='--', alpha=0.5)

        return fig

    except Exception as e:
        print(f"Error while plotting population trend: {e}")
        return None


def interpret_correlation(coefficient):
    """
    Provide an interpretation of the correlation coefficient.

    Parameters:
    coefficient (float): The Pearson correlation coefficient.

    Returns:
    str: Interpretation of the correlation strength and direction.
    """
    if coefficient > 0.7:
        return "strong positive"
    elif 0.3 < coefficient <= 0.7:
        return "moderate positive"
    elif 0 < coefficient <= 0.3:
        return "weak positive"
    elif -0.3 <= coefficient < 0:
        return "weak negative"
    elif -0.7 <= coefficient < -0.3:
        return "moderate negative"
    else:
        return "strong negative"


def plot_correlation(bird_observation, snowy_owl_trend):
    """
    Generate a correlation plot between observations and population index.

    Parameters:
    bird_observation (BirdObservation): An instance of BirdObservation class.
    snowy_owl_trend (SnowyOwlTrend): An instance of SnowyOwlTrend class.

    Returns:
    matplotlib.figure.Figure: The generated plot figure.
    """
    try:
        # Merge data on 'Year'
        observations_per_year = bird_observation.aggregate_observations_by_year()
        trend_data = snowy_owl_trend.data.copy()

        merged_data = pd.merge(observations_per_year, trend_data, on='Year', how='inner')
        if merged_data.empty:
            print("No common years between datasets for plotting.")
            return None

        # Calculate correlation coefficient
        correlation_coefficient = merged_data['OBSERVATION COUNT'].corr(merged_data['Index'], method='pearson')

        # Get interpretation
        interpretation = interpret_correlation(correlation_coefficient)

        # Create the figure and axis
        fig, ax1 = plt.subplots(figsize=(4, 2))
        fig.tight_layout()

        # Set background color to match GUI
        fig.patch.set_facecolor('#ECECEC')
        ax1.set_facecolor('#ECECEC')

        # Plot Observations as bars
        ax1.bar(merged_data['Year'], merged_data['OBSERVATION COUNT'], color='orchid', label='Observations')
        ax1.set_xlabel('Year', fontsize=10)
        ax1.set_ylabel('Observation Count', color='purple', fontsize=10)
        ax1.tick_params(axis='y', labelcolor='purple')

        # Plot Population Index as a line
        ax2 = ax1.twinx()
        ax2.plot(merged_data['Year'], merged_data['Index'], color='darkorange',
                 marker='o', label='Population Index')
        ax2.set_ylabel('Population Index', color='darkorange', fontsize=10)
        ax2.tick_params(axis='y', labelcolor='darkorange')

        # Set title
        plt.title('Correlation Between Observations and Population Index Over Years', fontsize=12)

        # Add correlation details as text
        textstr = f"Pearson Correlation Coefficient: {correlation_coefficient:.2f}\nInterpretation: {interpretation}"
        plt.text(
            0.05, 0.60,  # Adjusted position to lower part of the plot
            textstr,
            transform=plt.gca().transAxes,
            fontsize=8,
            verticalalignment='bottom',
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.5)
        )

        # Adjust legends for both axes
        ax1.legend(loc='upper left', fontsize=8)
        ax2.legend(loc='upper right', fontsize=8)

        # Adjust grid lines for subtlety
        ax1.grid(True, linestyle='--', alpha=0.5)

        return fig

    except Exception as e:
        print(f"Error while plotting correlation: {e}")
        return None