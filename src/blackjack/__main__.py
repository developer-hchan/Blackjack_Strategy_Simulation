import concurrent.futures
from functools import partial
from pathlib import Path
import tomllib

from blackjack.helper.chart_generation import generate_chart
from blackjack.helper.io import data_path_io
from blackjack.helper.simulation import run_game
from blackjack.helper.simulation import SimulationCases
from blackjack import global_data_dictionary
from blackjack import global_split_dictionary

from tqdm import tqdm

BASE_DIR = Path(__file__).resolve().parent.parent.parent


def main():
    # loading setting.toml
    with open(BASE_DIR / "settings.toml", "rb") as f:
        loaded_settings = tomllib.load(f)

    # raising an error for impossible simulation configurations
    if ('stand' not in loaded_settings['decisions']) or ('hit' not in loaded_settings['decisions']):
        raise ValueError("loaded_settings['decisions'] must include the decisions 'stand' and 'hit'")

    # creating simulation cases generators
    regular_cases_generator = SimulationCases(settings=loaded_settings).regular_cases_generator
    split_cases_generator = SimulationCases(settings=loaded_settings).split_cases_generator

    # Adding the expected value for each case in the global data dictionary
    for case in tqdm(regular_cases_generator, "PROCESS 1/2... "):
        expected_value = 0
        for _ in range(loaded_settings["number_of_sims"]):
            expected_value += run_game(toml_settings=loaded_settings, sim_case=case)
        
        global_data_dictionary[(case)] = ( round(expected_value / loaded_settings["number_of_sims"], 2) )
    

    # simulation calculating the expected value for the 'split' cases
    for case in tqdm(split_cases_generator, "PROCESS 2/2... "):
        expected_value = 0
        for _ in range(loaded_settings["number_of_sims"]):
            expected_value += run_game(toml_settings=loaded_settings, sim_case=case)
        
        global_split_dictionary[(case)] = ( round(expected_value / loaded_settings["number_of_sims"], 2) )


    # writing global data_dictionary to csv_file
    data_path_io(file_name="data.csv", dictionary=global_data_dictionary)

    # writing global_split_dictionary to csv_file
    data_path_io(file_name="data_split.csv", dictionary=global_split_dictionary)

    # creating the html basic stragey charts
    success = generate_chart(configuration=loaded_settings)
    if success is None:
        print('Error in creating basic_strategy_chart.html')
    else:
        print(f'\n{success}')


if __name__ == "__main__":
    main()