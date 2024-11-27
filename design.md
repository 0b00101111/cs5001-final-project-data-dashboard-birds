# Data Dashboard Project Design

## Data Sources

1. **Snowy Owl Records Dataset**
   - **Source:** eBird Basic Dataset
   - **Description:** Contains detailed records of Snowy Owl sightings, including geographic coordinates, observation counts, dates, and observer information.
   - **Citation:**
     ```
     eBird Basic Dataset. Version: EBD_relOct-2024. Cornell Lab of Ornithology, Ithaca, New York. Oct 2024.
     ```
   - **URL:** [https://github.com/0b00101111/cs5001-final-project-data-dashboard-birds/blob/8044a4dd0e3248f5f97f90872a1eb55cfd90e0e3/snowy_owl_record.csv](https://github.com/your-username/data-dashboard-project/raw/main/snowy_owl_record.csv)

2. **Snowy Owl Trend Dataset**
   - **Source:** NatureCounts
   - **Description:** Provides annual trends in Snowy Owl populations, including population estimates, migration patterns, and habitat changes.
   - **Citation:**
     ```
     NatureCounts. (2024). Snowy Owl Trend Data. Retrieved from https://naturecounts.ca/nc/socb-epoc/species.jsp?sp=snoowl1
     ```
   - **URL:** [https://github.com/0b00101111/cs5001-final-project-data-dashboard-birds/blob/8044a4dd0e3248f5f97f90872a1eb55cfd90e0e3/snowy_owl_trend.csv](https://github.com/your-username/data-dashboard-project/raw/main/snowy_owl_trend.csv)

## Object-Oriented Design

I will create two primary classes: `BirdObservation` and `SnowyOwlTrend`. The `BirdObservation` class will encapsulate details of each Snowy Owl sighting, including identifiers, common and scientific names, geographic coordinates, observation dates, observer IDs, and counts. The `SnowyOwlTrend` class will represent annual trend data, capturing the year, population estimates, migration patterns, and habitat changes. These classes will facilitate structured data storage and enable seamless data manipulation and analysis.

## Data Analysis

The analysis will focus on correlating Snowy Owl observation counts from the eBird dataset with the annual population trends from NatureCounts. Specifically, I will:

1. **Calculate Total Observations per Year:** Aggregate the number of Snowy Owl sightings from the eBird dataset for each year.
2. **Analyze Population Trends:** Examine the population estimates and migration patterns from the NatureCounts dataset.
3. **Correlate Observations with Trends:** Investigate how the number of sightings relates to population changes and migration patterns over the years.

The results will be stored in dictionaries for easy access and further processing, enabling the identification of potential patterns or anomalies in Snowy Owl populations.

## User Interaction and Visualization

In Milestone 2, I plan to develop a graphical user interface (GUI) using `Tkinter` that allows users to interact with the data. Users will be able to select specific years or ranges to visualize trends in Snowy Owl observations alongside environmental metrics. The visualization will include a **hotspot graph** generated with `matplotlib`, highlighting areas with high concentrations of observations. Interactive elements like buttons or sliders will enable users to dynamically filter data, making the dashboard both informative and user-friendly.