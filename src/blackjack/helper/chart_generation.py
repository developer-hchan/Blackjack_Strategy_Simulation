import copy
from pathlib import Path

import pandas as pd

from blackjack.helper.io import taking_generated_chart_path
from blackjack.helper.io import DEFAULT_CHART_OUTPUT_PATH
from blackjack.helper.io import DEFAULT_DATA_OUTPUT_PATH
from blackjack.helper.io import DEFAULT_DATA_SPLIT_OUTPUT_PATH


def generate_chart(configuration: dict) -> str: # Also generates an html file that is saved to the working directory
    dataframe = pd.read_csv(DEFAULT_DATA_OUTPUT_PATH)
    hard_dataframe = copy.deepcopy(dataframe)
    soft_dataframe = copy.deepcopy(dataframe)
    split = pd.read_csv(DEFAULT_DATA_SPLIT_OUTPUT_PATH)
    
    # creating the rules dataframe
    rules_df = pd.DataFrame.from_dict(configuration, orient='index', columns=[''])
    rules_df = rules_df.rename(index=lambda name: name.replace('_', ' '))

    # creating the hard dataframe matrix NOTE: for more details on what these commands are doing please see data_analysis.ipynb
    hard_dataframe = hard_dataframe[hard_dataframe["player hand texture"] == "hard"]
    hard_dataframe_1 = hard_dataframe.groupby(by=["player hand total","dealer face up"], as_index=False).max("average expected value")
    hard_dataframe_2 = pd.merge(left=hard_dataframe,right=hard_dataframe_1,how='inner').drop_duplicates(["player hand total","dealer face up"])
    hard_decision_matrix = hard_dataframe_2.pivot(index='player hand total',columns='dealer face up',values='player choice')
    hard_decision_matrix.index.names = ['Player Hard Total']
    hard_decision_matrix.columns.names = ['Dealer Face Up']
    hard_decision_matrix.rename(columns={11: 'A'}, inplace=True)

    # creating the soft dataframe matrix NOTE: for more details on what these commands are doing please see data_analysis.ipynb
    soft_dataframe = soft_dataframe[soft_dataframe["player hand texture"] == "soft"]
    soft_dataframe_1 = soft_dataframe.groupby(by=["player hand total","dealer face up"], as_index=False).max("average expected value")
    soft_dataframe_2 = pd.merge(left=soft_dataframe,right=soft_dataframe_1,how='inner').drop_duplicates(["player hand total","dealer face up"])
    soft_decision_matrix = soft_dataframe_2.pivot(index='player hand total',columns='dealer face up',values='player choice')
    soft_decision_matrix.rename(index={12: 'A,A', 13: 'A,2', 14: 'A,3', 15: 'A,4', 16: 'A,5', 17: 'A,6', 18: 'A,7', 19: 'A,8', 20: 'A,9'}, inplace= True)
    soft_decision_matrix.index.names = ['Player Hand']
    soft_decision_matrix.columns.names = ['Dealer Face Up']
    soft_decision_matrix.rename(columns={11: 'A'}, inplace=True)

    # creating the split decision matrix NOTE: for more details on what these commands are doing please see data_analysis.ipynb
    def hard_search(player_hand_total, dealer_face_up) -> float:
        search = hard_dataframe_2.loc[(hard_dataframe_2['player hand total'] == player_hand_total) & (hard_dataframe_2['dealer face up'] == dealer_face_up), "expected value"]
        return search

    def split_search(player_hand_total, dealer_face_up) -> float:
        search = split.loc[(split['player hand total'] == player_hand_total) & (split['dealer face up'] == dealer_face_up), "expected value"]
        return search

    def soft_search(player_hand_total, dealer_face_up) -> float:
        search = soft_dataframe_2.loc[(soft_dataframe_2['player hand total'] == player_hand_total) & (soft_dataframe_2['dealer face up'] == dealer_face_up), "expected value"]
        return search
    
    split_numbers = [20,18,16,14,12,10,8,6,4]
    dealer_numbers = [11,10,9,8,7,6,5,4,3,2]
    split_yes_no = []

    # comparing the max values from the hard-textured-max dataframe and the split dataframe. Making a new dataframe that lists if the split expected value is higher
    for x in dealer_numbers:
        for y in split_numbers:
            if float(split_search(y,x).iloc[0]) > float(hard_search(y,x).iloc[0]):
                split_yes_no.append((y,x,'yes'))
            else:
                split_yes_no.append((y,x,'no'))

    # same comparison as above but checking the soft 12 case from the soft-textured-max; soft 12 is A,A... the A,A case is not in the hard database
    for z in dealer_numbers:
        # in split, case A,A is represented by a player hand of 2; in soft, case A,A is represented by 12
        if float(split_search(player_hand_total=2,dealer_face_up=z).iloc[0]) > float(soft_search(player_hand_total=12,dealer_face_up=z).iloc[0]):
            split_yes_no.append((2,z,'yes'))
        else:
            split_yes_no.append((2,z,'no'))
    
    split_yes_no_df = pd.DataFrame(split_yes_no, columns=["player hand total","dealer face up","split?"])
    split_decision_matrix = pd.pivot(split_yes_no_df, index=['player hand total'], columns=['dealer face up'], values=['split?'])

    split_decision_matrix.rename(index={2: 'A,A', 4: '2,2', 6: '3,3', 8: '4,4', 10: '5,5', 12: '6,6', 14: '7,7', 16: '8,8', 18: '9,9', 20: '10,10'}, inplace= True)
    split_decision_matrix.index.names = ['Player Hand']
    split_decision_matrix.rename(columns={11: 'A'}, inplace=True)

    # for some reason this removes the ugly 'split?' header caption; I suppose it is technically slicing, but whatever
    split_decision_matrix = split_decision_matrix['split?']
    split_decision_matrix.columns.names = ['Dealer Face Up']

    # styling all the dataframes
    hard_styled = hard_decision_matrix.style.map(color_choice).set_table_attributes('style="border-collapse:collapse"').set_table_styles([
                                                          {"selector": "th",
                                                           "props": [("background-color","#d5eeff"), ("text-align","center"), ('color','black'), ('border','none')]},

                                                          {"selector": "td",
                                                           "props": [("text-align","center"), ('color','black'), ('border','none'), ('width', '75px')]}
    ])

    soft_styled = soft_decision_matrix.style.map(color_choice).set_table_attributes('style="border-collapse:collapse"').set_table_styles([
                                                          {"selector": "th",
                                                           "props": [("background-color","#d5eeff"), ("text-align","center"), ('color','black'), ('border','none')]},

                                                          {"selector": "td",
                                                           "props": [("text-align","center"), ('color','black'), ('border','none'), ('width', '75px')]}
    ])

    split_styled = split_decision_matrix.style.map(split_color_choice).set_table_attributes('style="border-collapse:collapse"').set_table_styles([
                                                          {"selector": "th",
                                                           "props": [("background-color","#d5eeff"), ("text-align","center"), ('color','black'), ('border','none')]},

                                                          {"selector": "td",
                                                           "props": [("text-align","center"), ('color','black'), ('border','none'), ('width', '75px')]}
    ])

    rules_styled = rules_df.style.set_table_attributes('style="border-collapse:collapse"').set_table_styles([
                                                          {"selector": "th.row_heading",
                                                           "props": [("background-color","#d5eeff"), ("text-align","center"), ('color','black'), ('border','none')]},

                                                          {"selector": "th.col_heading",
                                                           "props": [("background-color","#FFFFFF"), ("text-align","center"), ('color','black'), ('border','none')]},

                                                          {"selector": "td",
                                                           "props": [("background-color","#edb1f1"), ("text-align","center"), ('color','black'), ('border','none'), ('width','225px')]}
    ])

    taking_generated_chart_path(file_path=DEFAULT_CHART_OUTPUT_PATH, hard_styled=hard_styled, soft_styled=soft_styled, split_styled=split_styled, rules_styled=rules_styled)

    return 'successfully generated html'


# this function colors all the player options 'hit','stand','double','surrender'
def color_choice(value):
    color = None
    if value == 'hit':
        color = '#9896f1'
    elif value == 'stand':
        color = '#d59bf6'
    elif value == 'double':
        color = '#edb1f1'
    elif value == 'surrender':
        color = '#6643b5'
    
    return f'background-color: {color}'


# this function colors all the player options 'hit','stand','double','surrender'
def split_color_choice(value):
    color = None
    if value == 'no':
        color = '#d59bf6'
    elif value == 'yes':
        color = '#edb1f1'
    
    return f'background-color: {color}'

