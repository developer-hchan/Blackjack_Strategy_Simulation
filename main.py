import csv
import concurrent.futures
from functools import partial

from tqdm import tqdm

from simulation import expected_payout
from simulation import split_expected_payout
from simulation import data_dictionary
from simulation import split_dictionary
from chart_generation import generate_chart


def main():
###############################################################################
# Simulation Config #
###############################################################################

    # this dicionary is used to adjust the settings of the simulation
    config = {
        'number_of_sims': 25000,
        'decisions': ('stand','hit','double','surrender'),
        'deck_length': 7,
        'shuffle': True,
        'kill': True,
        'bet': 25.00,
        'blackjack_bonus': 1.5,
        'dealer_hit_soft_17': True,
        'double_after_split': True
        }


    if ('stand' not in config['decisions']) or ('hit' not in config['decisions']):
        raise ValueError("config['decisions'] must include the decisions 'stand' and 'hit'")

    ###############################################################################
    # Starting the Simulation #
    ###############################################################################

    # simulation cases NOTE: DO NOT ADJUST
    dealer_face_ups = [11,10,9,8,7,6,5,4,3,2]

    player_hand_matrix = [(20,'hard'),
                        (19,'hard'),
                        (18,'hard'),
                        (17,'hard'),
                        (16,'hard'), 
                        (15,'hard'),
                        (14,'hard'), 
                        (13,'hard'), 
                        (12,'hard'), 
                        (11,'hard'), 
                        (10,'hard'),

                        (20,'soft'),
                        (19,'soft'),
                        (18,'soft'),
                        (17,'soft'),
                        (16,'soft'),
                        (15,'soft'),
                        (14,'soft'),
                        (13,'soft'),
                        (12,'soft'),

                        (9,'hard'),
                        (8,'hard'), 
                        (7,'hard'),
                        (6,'hard'),
                        (5,'hard'),
                        (4,'hard')                 
        ]


    # The actual simulation code that does the magic
    for dealer_face_up in tqdm(dealer_face_ups, 'PROCESS 1/2...'):
        for tup in player_hand_matrix:
            player_starting_hand_total = tup[0]
            player_starting_hand_texture = tup[1]
            
            # making a temporary partial function, where it's only input is 'choice', in order to make it easier to pass into concurrent.futures.ThreadPoolExecutor()
            expected_payout_partial = partial(expected_payout, config, player_starting_hand_total, player_starting_hand_texture, dealer_face_up, data_dictionary)

            '''
            The idea is to have threads work on the different player decisions for otherwise the same case. For example, the partial case where
            (player_starting_hand_total = 17, player_starting_hand_texture = 'hard', dealer_face_up = 8, ...) has four variations (unless it is decided the player has less options):
            1. (17, 'hard', 8, 'stand')
            2. (17, 'hard', 8, 'hit')
            3. (17, 'hard', 8, 'double')
            4. (17, 'hard', 8, 'surrender')
            The idea is that different threads can work on these four variations concurrently.
            Also, we DO NOT want to work on different cases concurrently because it possible to miss the optimal decision for a previous case if that thread fails to finish before the current
            one has to search past cases. Player choice variations are NOT going to search internally for an optimal decision. I.e. none of the (17 'hard' vs 8) variations are searching 17 cases for
            the optimal decision, hence it is safe to run them concurrently.
            '''

            # Using a with statement so the threads join after all decision variations finish
            with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.map(expected_payout_partial, config['decisions'])


    # simulation calculating the expected value for the 'split' cases
    split_list = [20,18,16,14,12,10,8,6,4,2]
    for dealer_face_up in tqdm(dealer_face_ups, 'PROCESS 2/2...'):
        for player_starting_hand_total in split_list:
            split_expected_payout(configuration=config, player_starting_hand_total=player_starting_hand_total, dealer_face_up=dealer_face_up, output=split_dictionary)


    # writing DATA_DICTIONARY to csv_file
    with open('data.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        # this row is the header for the csv file
        writer.writerow(['player hand total','player hand texture','dealer face up','player choice','expected value'])
        for key, value in data_dictionary.items():
            writer.writerow([*key, value])


    # writing SPLIT_DICTIONARY to csv_file
    with open('data_split.csv', 'w') as csv_file2:
        writer = csv.writer(csv_file2)
        # this row is the header for the csv file
        writer.writerow(['player hand total','player hand texture','dealer face up','player choice','expected value'])
        for key, value in split_dictionary.items():
            writer.writerow([*key, value])


    # creating the html basic stragey charts
    success = generate_chart(configuration=config)
    if success == None:
        print('Error in creating basic_strategy_chart.html')
    else:
        print(f'\n{success}')


if __name__ == "__main__":
    main()