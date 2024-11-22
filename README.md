# Title

## Example of a Generated Blackjack Decision Chart and How to Use It

## What Are the Rules to Blackjack?

#### Other Things You Should Know
* What is a hard or soft hand
* What is blackjack
* unnatural 21 does not count as blackjack

#### Common Casino Rules

## So, How Are You Finding The Optimal Strategy?
First, we work off the assumption that we have no / little information regarding the cards we are going to draw from the deck.
* **As a note,** This is unlike card counting in which we are actively tracking the ratio of strong / weak cards remaining in the deck.
So, why not just write an algorithm for card counting? Well, what we are doing is referred to as "basic strategy," which is the foundation for
many card counting strategies --It is important to understand basic strategy prior to understanding card counting. But yes, there will
be a card counting update in the future.

Next, We simulate games for each possible case in blackjack: A single case being...\
(a player hand total, the player's hand type, a dealer face up card, and a player's initial decision).\
We run a case a few thousand times and find out the average expected value (how much money you're expected to win or lose) for that case.

There are three categories of player hands we need to find the expected values for: Hard hands, soft hands, and splittable hands.\
Player hard hands can have a hand total ranging from 4 - 20\
Player soft hands can have a hand total ranging from 12 - 21 (blackjack)\
Player splittable hands can only have the following hard hand totals: (20, 18, 16, 14, 12, 10, 8, 6, 4, 2, 12*)\
* 12* represents A,A , which is technically a soft 12

We start by generating the expected value for the player decisions that can be performed on a **hard 20**.
* Decisions usually include 'stand', 'hit', 'double', and 'surrender', but the decisions available to the player can be adjusted in the simulation settings. See <insert link here>

Example expected values generated for a player's **hard 20** against a **dealer face up Ace**:
* Stand = 2.96
* Hit = -22.46
* Double = -37.67
* Surrender = -16.33

We similarly generate the rest of the expected values for the **hard 20** case against the rest of the possible dealer face ups\
Which are: (10, 9, 8, 7, 6, 5, 4, 3, 2)

We the coninute the process with the **hard 19** case; however, now there is the potential for us to draw an Ace. That would give the player a **hard 20** hand.\
At this point, we would look back at the expected values generated in the **hard 20** case and instruct the algorithm to choose the optimal decision.

For example, say we have a **hard 19** and we draw an ace giving us a **hard 20**. We look and see that the dealer has a **face up Ace**. We search for the optimal strategy for
the follwing case: (player has a hand total of 20, player has a hard hand, dealer has a face up Ace). To which the algorithm will return 'stand' as that has the highest expected value of all the possible
player decisions. So, in the case we have a **hard 19**, draw an Ace, and the dealer has a **face up Ace**, the algorithm will choose the optimal decision of 'stand'.

After all the cases for **hard 19** are generated, we repeat the process with **hard 18**. But now we know the optimal strategies for **hard 19** and **hard 20**, so in case our
18 draws into either of those hands, we can choose the optimal strategy.

We repeat this process until **hard 10** because starting at a **hard 9** it becomes possible for to draw into a soft hand.\
9 + Ace = **soft 20**\
The reason **hard 10** is not included is because drawing 10 + Ace = 21, and that ends the player turn (at least for that hand if the player has multiple hands).

Starting at **hard 9**, we can no longer search previous cases for the optimal decison because we draw into a soft hand. So, starting here, we generate the optimal decisions for
all of the soft hands (20 - 12) a.k.a (A9, A8, A7, A6, A5, A4, A3, A2, AA)\
Luckily, the minimum hard hand that can be created from a soft hand is **hard 12**, a.k.a Ace + Ace or Ace + 9 + 2 or similar combination\
so, we have no problem searching for the optimal decisions for all the soft hand cases; we start with simulating from the **soft 20** case and go down to **soft 12**

Now that we have the optimal decisions for **hard 20** -> **hard 10** and all the soft cases, we can finish simulating the rest of the hard cases: **hard 9** -> **hard 4**

Still here? Awesome. Now we have to simulate the splittable hands.

Calculating the splittable hand expected values is relatively easy in theory, as we have all the optimal strategies for both the hard and soft hands. So, we create a splittable hand
like 7 + 7. Split it to get two player hands, lets say 7+10 and 7+9. Finally, we run the simulation the same way we have above for both newly created hands.

But... What about if we draw another splittable hand? Excellent question. I think technically the most accurate way to address this issue is to create a mini-monte-carlo tree for
each additional splittable hand; the reasoning being that when you get a splittable hand, what is the best thing to do? I will illustrate this approach below:

hand_A of 7+7 -> hand_B of 7+10 and hand_C of 7+7.\
We know the optimal strategy for hand_B, but what about hand_C?\
* **As a note**, we don't know yet if splitting 7+7 is the optimal choice --We were trying to find that answer by splitting hand_A.\
Ideally, we would simulate all the possible options for hand_C, which would usually be 'split', 'stand', 'hit', 'double', and 'surrender.' We would then perform the optimal decision on
hand_C.\
But what if the optimal decison for hand_C is to 'split' and hand_C splits into -> hand_D of 7+7 and hand_E of 7+9...\
We would need to do the same simulation for hand_D... which could eventually turn into a computational nightmare.

My compromise has been that if another splittable hand appears from a split hand, to just split the new hand as well. I believe it would be akin to gathering a few extra data points on the 
'split' player decision.

I would like to state that this simulation currently allows infinite splits. The rules on how many times you can split hands varies from casino to casino; however,
I am treating splittable hands as 'more' data for the simulation. The simulation also use a deck, so actually splitting an infinite amount of times is impossible; however, I will likely
include a split limit as a toggalable simulation setting in a future update.

Congratulations, you just finished generating the optimal decisions for the game of blackjack!

## Ok, But What is The Code Doing?

## Ok Again, But What if I Want to See the Exact Expected Values for Every Decision?

## How Do I Run My Own Simulations Using This Code?

## Well, I'm Something of a Data Scientist Myself

## Buy Me (Not You Me, but Me Me) a Coffee?
Nah, just donate to your local animal shelter

