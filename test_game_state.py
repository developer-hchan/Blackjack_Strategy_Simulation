import unittest

from game_state import GameState
from cards import Card
from cards import Hand

class TestCreateDeck(unittest.TestCase):
    def test_create_deck(self):    
        game = GameState()
        test_list = [
            2,3,4,5,6,7,8,9,10,10,10,10,11,
            2,3,4,5,6,7,8,9,10,10,10,10,11,
            2,3,4,5,6,7,8,9,10,10,10,10,11,
            2,3,4,5,6,7,8,9,10,10,10,10,11,

            2,3,4,5,6,7,8,9,10,10,10,10,11,
            2,3,4,5,6,7,8,9,10,10,10,10,11,
            2,3,4,5,6,7,8,9,10,10,10,10,11,
            2,3,4,5,6,7,8,9,10,10,10,10,11
            ]
        
        game.create_deck(deck_length=2)
        self.assertEqual(game.deck, test_list)


    def test_raise_error(self):
        game = GameState()
        with self.assertRaises(Exception):
            game.create_deck(0)

class TestRemoveHandsFromDeck(unittest.TestCase):
    def test_remove_hands_from_deck(self):
        game = GameState()
        game.deck = [
            2,3,4,5,6,7,8,9,10,10,10,10,11,
            2,3,4,5,6,7,8,9,10,10,10,10,11
            ]

        player_hand = Hand()
        dealer_hand = Hand()
        player_hand.hand_list = [Card(11, 'heart'), Card(11, 'spade')]
        dealer_hand.hand_list = [Card(7, 'club'), Card(3, 'spade')]

        game.player_hands.append(player_hand)
        game.dealer_hand = dealer_hand

        game.remove_hands_from_deck()

        expected_result = [
            2,4,5,6,8,9,10,10,10,10,
            2,3,4,5,6,7,8,9,10,10,10,10
            ]

        self.assertEqual(game.deck, expected_result)


class TestKill(unittest.TestCase):
    pass


class TestDraw(unittest.TestCase):
    def test_draw(self):
        game = GameState()
        game.deck = [2,3,4,5,6,7,8,9,10,10,10,11]

        player_hand = Hand()
        dealer_hand = Hand()
        player_hand.hand_list = [Card(11, 'heart'), Card(11, 'spade')]
        dealer_hand.hand_list = [Card(7, 'club'), Card(3, 'spade')]

        game.draw(player_hand)
        game.draw(dealer_hand)
        game.draw(dealer_hand)

        self.assertEqual(14, player_hand.total)
        self.assertEqual(3, len(player_hand.hand_list))
        self.assertEqual(17, dealer_hand.total)
        self.assertEqual(4, len(dealer_hand.hand_list))
        self.assertEqual(game.deck, [5,6,7,8,9,10,10,10,11])


class TestSplit(unittest.TestCase):
    def test_split(self):
        game = GameState()
        game.deck = [6,9]

        player_hand = Hand()
        dealer_hand = Hand()
        player_hand.hand_list = [Card(4, 'heart'), Card(4, 'spade')]
        dealer_hand.hand_list = [Card(7, 'club'), Card(3, 'spade')]

        game.player_hands.append(player_hand)
        game.dealer_hand = dealer_hand

        game.create_deck(7)

        game.split(game.player_hands[0])

        self.assertEqual(game.player_hands[0].hand_list[0].number, 4)
        self.assertEqual(game.player_hands[0].hand_list[1].number, 6)

        self.assertEqual(game.player_hands[1].hand_list[0].number, 4)
        self.assertEqual(game.player_hands[1].hand_list[1].number, 9)

        self.assertEqual(2, len(game.player_hands))


    def test_split_then_front_split(self):
        game = GameState()
        game.deck = [4,5,3,11]

        player_hand = Hand()
        dealer_hand = Hand()
        player_hand.hand_list = [Card(4, 'heart'), Card(4, 'spade')]
        dealer_hand.hand_list = [Card(7, 'club'), Card(3, 'spade')]

        game.player_hands.append(player_hand)
        game.dealer_hand = dealer_hand

        game.create_deck(7)

        game.split(game.player_hands[0])
        game.split(game.player_hands[0])

        self.assertEqual(game.player_hands[0].hand_list[0].number, 4)
        self.assertEqual(game.player_hands[0].hand_list[1].number, 3)

        self.assertEqual(game.player_hands[1].hand_list[0].number, 4)
        self.assertEqual(game.player_hands[1].hand_list[1].number, 5)

        self.assertEqual(game.player_hands[2].hand_list[0].number, 4)
        self.assertEqual(game.player_hands[2].hand_list[1].number, 11)

        self.assertEqual(3, len(game.player_hands))


    def test_split_then_back_split(self):
        game = GameState()
        game.deck = [5,4,3,11]

        player_hand = Hand()
        dealer_hand = Hand()
        player_hand.hand_list = [Card(4, 'heart'), Card(4, 'spade')]
        dealer_hand.hand_list = [Card(7, 'club'), Card(3, 'spade')]

        game.player_hands.append(player_hand)
        game.dealer_hand = dealer_hand

        game.create_deck(7)

        game.split(game.player_hands[0])
        game.split(game.player_hands[1])

        self.assertEqual(game.player_hands[0].hand_list[0].number, 4)
        self.assertEqual(game.player_hands[0].hand_list[1].number, 5)

        self.assertEqual(game.player_hands[1].hand_list[0].number, 4)
        self.assertEqual(game.player_hands[1].hand_list[1].number, 3)

        self.assertEqual(game.player_hands[2].hand_list[0].number, 4)
        self.assertEqual(game.player_hands[2].hand_list[1].number, 11)

        self.assertEqual(3, len(game.player_hands))

    





if __name__ == '__main__':
    unittest.main()