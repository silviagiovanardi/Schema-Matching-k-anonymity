import pandas as pd


def generalize_year_to_decade(year):
    if pd.isna(year):
        return "Unknown"
    decade = (int(year) // 10) * 10
    return f"{decade}-{decade+9}"
