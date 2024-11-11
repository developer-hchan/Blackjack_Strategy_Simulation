# TODO: IMPLEMENT
class TestSplit(unittest.TestCase):
    def test_ace_split(self):
        player_hand = Hand()
        player_hand.hand_list.append(Card(1,'heart'))
        player_hand.hand_list.append(Card(1,'diamond'))

        dealer_hand = Hand()
        dealer_hand.hand_list.append(Card(8,'club'))
        dealer_hand.hand_list.append(Card(7,'spade'))

        random.seed(2)
        expected_value = run_match(player_hand= player_hand,dealer_hand= dealer_hand, bet= 25.00, player_first_choice= 'split', dealer_hit_soft_17= True)

        print(f'\nTEST_ACE_SPLIT.. player hand: ')
        for card in player_hand.hand_list:
            print(card)

        print(f'\nTEST_ACE_SPLIT.. dealer hand: ')
        for card in dealer_hand.hand_list:
            print(card)
        
        print(expected_value)
        self.assertTrue(True)



