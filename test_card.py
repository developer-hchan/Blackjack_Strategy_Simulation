import unittest

from cards import Card, Hand, add

class TestCard(unittest.TestCase):
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
    

    def test_texture(self):
        hand_object_1 = Hand()
        hand_object_2 = Hand()
        hand_object_3 = Hand()

        hand_object_1.hand_list = [Card(7,'Spade'), Card(8,'Heart')]
        hand_object_2.hand_list = [Card(11,'Spade'), Card(6,'Heart'), Card(7, 'Diamond')]
        hand_object_3.hand_list = [Card(11,'Spade'), Card(6,'Heart')]

        self.assertEqual(hand_object_1.texture,'hard')
        self.assertEqual(hand_object_2.texture,'hard')
        self.assertEqual(hand_object_3.texture,'soft')


if __name__ == "__main__":
    unittest.main()

