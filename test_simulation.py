import unittest
import random

from game_state import GameState
from cards import Card
from cards import Hand
import simulation as sim
from simulation import dealer_turn
from simulation import generate_hand
from simulation import generate_dealer_hand
from simulation import check_4_blackjack
from simulation import player_turn
from simulation import split_phase


class TestGenerateHands(unittest.TestCase):
    def test_generate_hand_hard(self):
        random_total = random.randint(4,20)
        hand = generate_hand(random_total, 'hard')

        self.assertEqual(random_total, hand.total)
        self.assertEqual('hard', hand.texture)
        self.assertEqual(2, len(hand.hand_list))


    def test_generate_hand_soft_1(self):
        random_total = random.randint(12,21)
        hand = generate_hand(random_total, 'soft')

        self.assertEqual(random_total, hand.total)
        self.assertEqual('soft', hand.texture)
        self.assertEqual(2, len(hand.hand_list))


    def test_generate_hand_soft_2(self):
        hand = generate_hand(12, 'soft')

        self.assertEqual(12, hand.total)
        self.assertEqual('soft', hand.texture)
        self.assertEqual(2, len(hand.hand_list))


    def test_generate_hand_soft_1(self):
        hand = generate_hand(21, 'soft')
        
        self.assertEqual(21, hand.total)
        self.assertEqual('soft', hand.texture)
        self.assertEqual(2, len(hand.hand_list))


    def test_generate_hand_split(self):
        hand = generate_hand(6, 'split')

        self.assertEqual(3, hand.hand_list[0].number)
        self.assertEqual(3, hand.hand_list[1].number)
        self.assertEqual(2, len(hand.hand_list))


    def test_generate_hand_split_2(self):
        hand = generate_hand(2, 'split')

        self.assertEqual(1, hand.hand_list[0].number)
        self.assertEqual(1, hand.hand_list[1].number)
        self.assertEqual(2, len(hand.hand_list))


    def test_generate_dealer_hand(self):
        dealer_hand = generate_dealer_hand(2)

        self.assertGreater(dealer_hand.total, 2+1)
        self.assertLess(dealer_hand.total, 22)
        self.assertEqual(2, len(dealer_hand.hand_list))


class TestCheck4Blackjack(unittest.TestCase):
    def test_player_blackjack(self):
        game = GameState()
        game.deck = []
        
        player_hand = Hand()
        player_hand.hand_list = [Card(10,'diamond'), Card(11,'diamond')]
        game.player_hands.append(player_hand)
        game.dealer_hand.hand_list = [Card(6, 'heart'), Card(11, 'heart')]

        check_4_blackjack(game)

        self.assertEqual(game.bet*game.blackjack_bonus, game.value)

    def test_dealer_blackjack(self):
        game = GameState()
        game.deck = []

        player_hand = Hand()
        player_hand.hand_list = [Card(7,'diamond'), Card(4,'diamond')]
        game.player_hands.append(player_hand)
        game.dealer_hand.hand_list = [Card(11, 'heart'), Card(10, 'heart')]

        check_4_blackjack(game)

        self.assertEqual(-game.bet, game.value)

    def test_tie_blackjack(self):
        game = GameState()
        game.deck = []

        player_hand = Hand()
        player_hand.hand_list = [Card(10,'diamond'), Card(11,'diamond')]
        game.player_hands.append(player_hand)
        game.dealer_hand.hand_list = [Card(10, 'heart'), Card(11, 'heart')]

        check_4_blackjack(game)

        self.assertEqual(0, game.value)


class TestPlayerTurn(unittest.TestCase):
    def test_hit(self):
        pass

    def test_stand(self):
        game = GameState()
        game.deck = []

        player_hand = Hand()
        player_hand.hand_list = [Card(7,'diamond'), Card(8,'diamond')]
        game.player_hands.append(player_hand)
        game.dealer_hand.hand_list = [Card(4, 'heart'), Card(9, 'heart')]

        player_turn(game=game, player_first_choice='stand', dealer_face_up=4)

        self.assertEqual(game.player_hands[0].total, 15)


    def test_double(self):
        pass

    def test_surrender(self):
        game = GameState()
        game.deck = []

        player_hand = Hand()
        player_hand.hand_list = [Card(10,'diamond'), Card(8,'diamond')]
        game.player_hands.append(player_hand)
        game.dealer_hand.hand_list = [Card(8, 'heart'), Card(9, 'heart')]

        player_turn(game=game, player_first_choice='surrender', dealer_face_up=8)

        self.assertEqual(game.player_hands[0].total, 18)
        self.assertEqual(game.dealer_hand.total, 17)
        self.assertEqual(game.value, -0.5*game.bet)


    def test_split_aces(self):
        game = GameState()
        game.deck = [7, 10]

        player_hand = Hand()
        player_hand.hand_list = [Card(11,'diamond'), Card(11,'diamond')]
        game.player_hands.append(player_hand)
        game.dealer_hand.hand_list = [Card(8, 'heart'), Card(9, 'heart')]

        player_turn(game=game, player_first_choice='split', dealer_face_up=8)

        self.assertEqual(len(game.player_hands), 2)
        self.assertEqual(18, game.player_hands[0].total)
        self.assertEqual(21, game.player_hands[1].total)


    def test_split_aces_2(self):
        game = GameState()
        game.deck = [7, 10]

        player_hand = Hand()
        player_hand.hand_list = [Card(1,'diamond'), Card(11,'diamond')]
        game.player_hands.append(player_hand)
        game.dealer_hand.hand_list = [Card(8, 'heart'), Card(9, 'heart')]

        player_turn(game=game, player_first_choice='split', dealer_face_up=8)

        self.assertEqual(len(game.player_hands), 2)
        self.assertEqual(18, game.player_hands[0].total)
        self.assertEqual(21, game.player_hands[1].total)


    def test_split_aces_3(self):
        game = GameState()
        game.deck = [7, 10]

        player_hand = Hand()
        player_hand.hand_list = [Card(1,'diamond'), Card(1,'diamond')]
        game.player_hands.append(player_hand)
        game.dealer_hand.hand_list = [Card(8, 'heart'), Card(9, 'heart')]

        player_turn(game=game, player_first_choice='split', dealer_face_up=8)

        self.assertEqual(len(game.player_hands), 2)
        self.assertEqual(18, game.player_hands[0].total)
        self.assertEqual(21, game.player_hands[1].total)


class TestSplitPhase(unittest.TestCase):
    def test_split_phase(self):
        game = GameState()
        game.deck = [4, 10]

        player_hand = Hand()
        player_hand.hand_list = [Card(7,'diamond'), Card(7,'diamond')]
        game.player_hands.append(player_hand)
        game.dealer_hand.hand_list = [Card(8, 'heart'), Card(9, 'heart')]

        split_phase(game)

        self.assertEqual(len(game.player_hands), 2)
        self.assertEqual(11, game.player_hands[0].total)
        self.assertEqual(17, game.player_hands[1].total)

    def test_split_phase_then_back_split(self):
        game = GameState()
        game.deck = [4, 7, 9, 8]

        player_hand = Hand()
        player_hand.hand_list = [Card(7,'diamond'), Card(7,'diamond')]
        game.player_hands.append(player_hand)
        game.dealer_hand.hand_list = [Card(8, 'heart'), Card(9, 'heart')]

        split_phase(game)

        self.assertEqual(len(game.player_hands), 3)
        self.assertEqual(11, game.player_hands[0].total)
        self.assertEqual(16, game.player_hands[1].total)
        self.assertEqual(15, game.player_hands[2].total)


    def test_split_phase_then_front_split(self):
        game = GameState()
        game.deck = [7, 4, 2, 11]

        player_hand = Hand()
        player_hand.hand_list = [Card(7,'diamond'), Card(7,'diamond')]
        game.player_hands.append(player_hand)
        game.dealer_hand.hand_list = [Card(8, 'heart'), Card(9, 'heart')]

        split_phase(game)

        self.assertEqual(len(game.player_hands), 3)
        self.assertEqual(9, game.player_hands[0].total)
        self.assertEqual(11, game.player_hands[1].total)
        self.assertEqual(18, game.player_hands[2].total)

class TestPlayerTurnAdvance(unittest.TestCase):
    def test_player_turn_advance(self):
        pass


class TestDealerTurn(unittest.TestCase):
    def test_hit_on_soft_17(self):
        game = GameState()
        game.dealer_hit_soft_17 = True
        game.deck = [11]

        game.dealer_hand.hand_list = [Card(6, 'heart'), Card(11, 'heart')]
        dealer_turn(game)

        self.assertEqual(18, game.dealer_hand.total)

    def test_stand_on_soft_17(self):
        game = GameState()
        game.dealer_hit_soft_17 = False
        game.deck = [11]

        game.dealer_hand.hand_list = [Card(6, 'heart'), Card(11, 'heart')]
        dealer_turn(game)

        self.assertEqual(17, game.dealer_hand.total)

    def test_hit_on_soft_17_multiple_cards(self):
        game = GameState()
        game.dealer_hit_soft_17 = True
        game.deck = [2]

        game.dealer_hand.hand_list = [Card(4, 'heart'), Card(11, 'heart'), Card(2, 'heart')]
        dealer_turn(game)

        self.assertEqual(19, game.dealer_hand.total)


class TestEvaluate(unittest.TestCase):
    def test_evaluate(self):
        pass


if __name__ == '__main__':
    unittest.main()