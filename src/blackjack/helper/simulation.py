from blackjack.helper.game_state import GameState


class SimulationCases:
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

    split_list = [20,18,16,14,12,10,8,6,4,2]


    def __init__(self, settings: dict) -> None:
        # generator for all the cases that need to be simulated; via generator comprehension
        self.regular_cases_generator = ((card_setting[0], card_setting[1], face_up, choice) 
                                           for face_up in self.dealer_face_ups 
                                           for card_setting in self.player_hand_matrix
                                           for choice in settings['decisions']
        )

        # generator for split cases
        self.split_cases_generator = ((splittable_total, "split", face_up, "split") 
                                           for face_up in self.dealer_face_ups 
                                           for splittable_total in self.split_list
        )

        self.number_of_regular_cases: int = len(self.dealer_face_ups) * len(self.player_hand_matrix) * len(settings['decisions'])


def calculate_expected_value(sim_case: tuple, toml_settings: dict) -> dict:
    """
    calculates the expected value for 1 case and appends it to the global_data_dictionary
    A case is a tuple with the following information: (player hand total, player hand texture, dealer face up, player choice)
    """

    # Creating a singular game object for all this simulation
    game = GameState(**toml_settings)

    # Adding the expected value for each sim_case in the global data dictionary
    output_dict = {}

    # run a game for the number of sims specified in the "settings.toml" file
    for _ in range(toml_settings["number_of_sims"]):
        game.run_game(sim_case=sim_case)

    # creating a dictionary with a single entry and returning
    output_dict[(sim_case)] = (round(game.value / toml_settings["number_of_sims"], 2))

    return output_dict
    