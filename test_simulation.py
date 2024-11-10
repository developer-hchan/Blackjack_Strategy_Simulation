import unittest
from simulation import *
import random

class TestSimulation(unittest.TestCase):
    def test_generate_hard_hand(self):
        # a hard hand can only have a total between 4 and 21
        random_total = random.randint(4,21)
        hand = generate_hand(random_total,'hard')

        print(f"\nTEST_GENERATE_HARD_HAND: ")
        for card in hand.hand_list:
            print(card)

        self.assertEqual(random_total, hand.total)
        self.assertEqual(2, len(hand.hand_list))
    
    def test_generate_soft_hand(self):
        # a soft hand can only have a total between 12 and 21
        random_total = random.randint(12,21)
        hand = generate_hand(random_total,'soft')

        print(f"\nTEST_GENERATE_SOFT_HAND: ")
        for card in hand.hand_list:
            print(card)

        self.assertEqual(random_total,hand.total)
        self.assertEqual(2, len(hand.hand_list))


if __name__ == "__main__":
    unittest.main()