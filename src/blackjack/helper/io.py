from pathlib import Path
import csv

import pandas as pd

SRC_PACKAGE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = SRC_PACKAGE_DIR / "data"
OUTPUT_DIR = SRC_PACKAGE_DIR / "output"


def data_path_io(file_name: str, dictionary: dict):
    write_path = DATA_DIR / file_name
    with write_path.open('w') as csv_file:
        writer = csv.writer(csv_file)
        # this row is the header for the csv file
        writer.writerow(['player hand total','player hand texture','dealer face up','player choice','expected value'])
        for key, value in dictionary.items():
            writer.writerow([*key, value])


def chart_generation_io(file_name: str, hard_styled: pd.DataFrame, soft_styled: pd.DataFrame, split_styled: pd.DataFrame, rules_styled: pd.DataFrame):
    write_path = OUTPUT_DIR / file_name
    # finally writing the 4 dataframes to an html file and saving it in the working directory
    with write_path.open('w') as chart:
        chart.write('<h3>Hard Hand Decision Matrix</h3>'
                    + hard_styled.to_html()
                    + '<br>'
                    + '<h3>Soft Hand Decision Matrix</h3>'
                    + soft_styled.to_html() 
                    + '<br>'
                    + '<h3>Split Hand Decision Matrix</h3>'
                    + split_styled.to_html()
                    + '<br>'
                    + '<h3>Simulation Rules</h3>'
                    + rules_styled.to_html()
                    )
