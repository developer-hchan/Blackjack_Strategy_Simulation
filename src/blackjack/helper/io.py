from pathlib import Path
import csv
from typing import TextIO

import pandas as pd

SRC_PACKAGE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_DATA_OUTPUT_PATH = SRC_PACKAGE_DIR / "data" / "data.csv"
DEFAULT_DATA_SPLIT_OUTPUT_PATH = SRC_PACKAGE_DIR / "data" / "data_split.csv"
DEFAULT_CHART_OUTPUT_PATH = SRC_PACKAGE_DIR / "output" / "basic_strategy_chart.html"


def taking_generated_data_path(file_path: Path, dictionary: dict):
    """
    Taking the file path for where the generated data should be saved.
    """
    
    with file_path.open("w") as file:
        writing_generated_data_path(file=file, dictionary=dictionary)


def writing_generated_data_path(file: TextIO, dictionary: dict):
    """
    Saves generated data (data.csv and data_split.csv) to specified file location.
    This function will save the data as a csv file.
    """

    writer = csv.writer(file)
    # This row is the header for the csv file
    writer.writerow(["player hand total","player hand texture","dealer face up","player choice","expected value"])
    for key, value in dictionary.items():
        writer.writerow([*key, value])


def taking_generated_chart_path(file_path: Path, hard_styled: pd.DataFrame, soft_styled: pd.DataFrame, split_styled: pd.DataFrame, rules_styled: pd.DataFrame):
    """
    Taking the file path for where the generated chart should be saved
    """

    with file_path.open("w") as chart:
        writing_generated_chart_path(chart=chart, hard_styled=hard_styled, soft_styled=soft_styled, split_styled=split_styled, rules_styled=rules_styled)


def writing_generated_chart_path(chart: TextIO, hard_styled: pd.DataFrame, soft_styled: pd.DataFrame, split_styled: pd.DataFrame, rules_styled: pd.DataFrame):
    """
    Saves generated strategy chart (basic_strategy_chart.html) to file location.
    """

    # Finally writing the 4 dataframes to an html file and saving it in the working directory
    chart.write("<h3>Hard Hand Decision Matrix</h3>"
                + hard_styled.to_html()
                + "<br>"
                + "<h3>Soft Hand Decision Matrix</h3>"
                + soft_styled.to_html() 
                + "<br>"
                + "<h3>Split Hand Decision Matrix</h3>"
                + split_styled.to_html()
                + "<br>"
                + "<h3>Simulation Rules</h3>"
                + rules_styled.to_html()
    )