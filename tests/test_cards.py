import unittest
import random

from blackjack.helper.cards import Card
from blackjack.helper.cards import Hand
from blackjack.helper.cards import add
from blackjack.helper.cards import generate_hand
from blackjack.helper.cards import generate_dealer_hand

class TestAdd(unittest.TestCase):
    def test_add(self):
        # testing basic addition
        hand_1: list[Card] = [Card(7,'Spade'), Card(8,'Heart')]
        hand_total_1 = add(hand_1)
        self.assertEqual(hand_total_1,15)

        # testing soft ace addition
        hand_2: list[Card] = [Card(11,'Spade'), Card(8,'Heart')]
        hand_total_2 = add(hand_2)
        self.assertEqual(hand_total_2,19)

        # testing if a single hard ace is added correctly
        hand_3: list[Card] = [Card(11,'Spade'), Card(6,'Heart'), Card(7, 'Diamond')]
        hand_total_3 = add(hand_3)
        self.assertEqual(hand_total_3,14)

        # testing if 2 aces are added correctly, one needing to be hard, the other needing to be soft
        hand_4: list[Card] = [Card(11,'Spade'), Card(2, 'Club'), Card(11,'Heart'), Card(6, 'Diamond')]
        hand_total_4 = add(hand_4)
        self.assertEqual(hand_total_4,20)

        # testing if 3 aces are added correctly, two needing to be hard, the other two needing to be soft
        hand_5: list[Card] = [Card(11,'Spade'), Card(8, 'Club'), Card(11,'Heart'), Card(11, 'Diamond')]
        hand_total_5 = add(hand_5)
        self.assertEqual(hand_total_5,21)

        # testing if 4 aces are added correctly, with all 4 aces needing to be soft
        hand_6: list[Card] = [Card(11,'Spade'), Card(11,'Heart'), Card(11, 'Diamond'), Card(11, 'Club'), Card(10, 'Spade')]
        hand_total_6 = add(hand_6)
        self.assertEqual(hand_total_6,14)


class TestTexture(unittest.TestCase):
    def test_texture(self):
        hand_object_1 = Hand()
        hand_object_2 = Hand()
        hand_object_3 = Hand()
        hand_object_4 = Hand()

        hand_object_1.hand_list = [Card(7,'Spade'), Card(8,'Heart')]
        hand_object_2.hand_list = [Card(11,'Spade'), Card(6,'Heart'), Card(7, 'Diamond')]
        hand_object_3.hand_list = [Card(11,'Spade'), Card(6,'Heart')]
        hand_object_4.hand_list = [Card(11,'Spade'), Card(11,'Heart')]

        self.assertEqual(hand_object_1.texture,'hard')
        self.assertEqual(hand_object_2.texture,'hard')
        self.assertEqual(hand_object_3.texture,'soft')
        self.assertEqual(hand_object_4.texture,'soft')


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


if __name__ == '__main__':
    unittest.main()