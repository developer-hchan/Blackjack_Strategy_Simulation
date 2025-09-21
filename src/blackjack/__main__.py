from multiprocessing import Pool, Manager
from functools import partial
from pathlib import Path
import tomllib

from tqdm import tqdm

from blackjack.helper.chart_generation import generate_chart
from blackjack.helper.io import data_path_io
from blackjack.helper.simulation import calculate_expected_value
from blackjack.helper.simulation import SimulationCases
from blackjack import global_data_dictionary
from blackjack import global_split_dictionary

BASE_DIR = Path(__file__).resolve().parent.parent.parent


def main():
    # loading setting.toml
    with open(BASE_DIR / "settings.toml", "rb") as f:
        loaded_settings = tomllib.load(f)

    # raising an error for impossible simulation configurations
    if ('stand' not in loaded_settings['decisions']) or ('hit' not in loaded_settings['decisions']):
        raise ValueError("loaded_settings['decisions'] must include the decisions 'stand' and 'hit'")

    # creating simulation object that has Simulation Cases Generators 
    simulation = SimulationCases(settings=loaded_settings)

    # creating a functools partial function; loading toml settings into calculate_expected_value()
    loaded_calculate_expected_value = partial(calculate_expected_value, toml_settings=loaded_settings)

    # multiprocessing for regular simulation cases
    for _ in tqdm(range(int(simulation.number_of_regular_cases / len(loaded_settings["decisions"])))):
        # case queue pulls the number of cases that can be worked on simultaneously from the simulation generator
        case_queue = []
        for _ in loaded_settings["decisions"]:
            case_queue.append(next(simulation.regular_cases_generator))

        # multiprocessing.Manager() allows us to create shared resources for processes
        with Manager() as manager:
            # creating shared dictionary for processes to append to
            d = manager.dict()
            # creating the mulitple processes and adding to shared dictionary
            # NOTE: limiting amount processes equivalent to number of available decisions
            with Pool(processes=len(loaded_settings["decisions"])) as p:
                list_of_dicts = p.map(loaded_calculate_expected_value, case_queue)
                for dict in list_of_dicts:
                    d.update(dict)
            
            # passing shared dictionary into global dictionary
            global_data_dictionary.update(d)
    
    # not multiprocessing *yet* for split simulation cases
    for case in tqdm(simulation.split_cases_generator):
        global_split_dictionary.update(calculate_expected_value(sim_case=case, toml_settings=loaded_settings))

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