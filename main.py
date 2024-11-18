import csv

from tqdm import tqdm

from simulation import expected_payout, DATA_DICTIONARY, SPLIT_DICTIONARY
from chart_generation import generate_chart

# how many simulations should be run for each situation
# default: 10000
sims: int = 100000

# these are the decisions the player can make
# NOTE: WARNING! USE ONE OF THE DECISION CASES LISTED BELOW
# default: ('hit','stand','double','surrender')
decision: tuple[str] = ('hit','stand','double','surrender')

# how much to bet on each hand
# default: 25.00
bet: float = 25.00

# does the dealer hit a soft 17?
# default: True
# alternative: False
dealer_hit_soft_17: bool = True

###############################################################################
# Starting the Simulation #
###############################################################################

print('\nSIMULATION RULES:')
print(f'\nNumber of Simulations per case: {sims}\nPlayer Available Decisions: {decision}\nBet Per Hand: {bet}\nDealer Hit on 17?: {str(dealer_hit_soft_17)}\n')

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
        expected_payout(player_starting_hand_total= player_starting_hand_total, player_starting_hand_texture= player_starting_hand_texture, dealer_face_up= dealer_face_up, bet= bet,number_of_matches= sims, choices= decision, dealer_hit_soft_17= dealer_hit_soft_17, output= DATA_DICTIONARY)


# simulation calculating the expected value for the 'split' option
split_list = [20,18,16,14,12,10,8,6,4,2]
for dealer_face_up in tqdm(dealer_face_ups, 'PROCESS 2/2...'):
    for player_starting_hand_total in split_list:
        expected_payout(player_starting_hand_total= player_starting_hand_total, player_starting_hand_texture= 'hard', dealer_face_up= dealer_face_up, bet= bet,number_of_matches= sims, choices= ['split'], dealer_hit_soft_17= dealer_hit_soft_17, output= SPLIT_DICTIONARY)


# for k, v in DATA_DICTIONARY.items():
#     print(f'{k}: {v}')


# writing DATA_DICTIONARY to csv_file
with open('data.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    # this row is the header for the csv file
    writer.writerow(['player hand total','player hand texture','dealer face up','player choice','expected value'])
    for key, value in DATA_DICTIONARY.items():
       writer.writerow([*key, value])


# writing SPLIT_DICTIONARY to csv_file
with open('data_split.csv', 'w') as csv_file2:
    writer = csv.writer(csv_file2)
    # this row is the header for the csv file
    writer.writerow(['player hand total','player hand texture','dealer face up','player choice','expected value'])
    for key, value in SPLIT_DICTIONARY.items():
       writer.writerow([*key, value])


# creating the html basic stragey charts
success = generate_chart([str(sims),str(decision),str(bet),str(dealer_hit_soft_17)])
if success == None:
    print('Error in creating basic_strategy_chart.html')
else:
    print(f'\n{success}')