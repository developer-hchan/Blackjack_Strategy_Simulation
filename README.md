# Title

## Table of Contents
[Example of a Generated Blackjack Decision Chart and How to Use It](#Example-of-a-Generated-Blackjack-Decision-Chart-and-How-to-Use-It)\
[What Are the Rules to Blackjack](#What-Are-the-Rules-to-Blackjack)\
[General Rules](#General-Rules)\
[Other Things You Should Know](#Other-Things-You-Should-Know)\
[Common Casino Rules and Their Variations](#Common-Casino-Rules-and-Their-Variations)\
[So, How Are You Finding The Optimal Strategy?](#so-how-are-you-finding-the-optimal-strategy)\
[Ok, But What is The Code Doing?](#ok-but-what-is-the-code-doing)\
[Ok Again, But What if I Want to See the Exact Expected Values for Every Decision?](#ok-again-but-what-if-i-want-to-see-the-exact-expected-values-for-every-decision)\
[How Do I Run My Own Simulations Using This Code?](#how-do-i-run-my-own-simulations-using-this-code)

## Example of a Generated Blackjack Decision Chart and How to Use It

![example-basic-strategy-chart](https://github.com/user-attachments/assets/5dc11703-19b1-411a-9464-ed425e960292)

## What Are the Rules to Blackjack?
These are the rules for how blackjack is played in casinos, with the player(s) playing against the dealer

I recommend either reading the article or watching the listed youtube video below for a full overview of the rules; however, I will go over the basics in the [General Rules](#general-rules) section.

<insert an article to read>
<insert a youtube video>

#### General Rules
The ultimate goal of blackjack is beat the dealer. You do this by ending with a higher hand than the dealer without going over
a hand total of 21.\
Within a single deck of cards, there 4 sets of the following cards: \
2, 3, 4, 5, 6, 7, 8, 9, 10, Jack, Queen, King, Ace\
All the cards are represented by their face value except Jack, Queen, and King which each have a value of 10.\
An Ace has a value of 1 or 11, whichever is more helpful for the individual that has it. Though, this just boils down to an Ace switching its value to
1 if having it as an 11 would put the player's hand total above 21.

Here are some example hands:
* 7 + 6 = hand total of 13
* 7 + 10 + 9 = hand total of 26
* Ace + 9 = hand total of 20
* Ace + 9 + 3 = hand total of 13
* Ace + 9 + Ace = hand total of 21

A single game of blackjack consists of 3 main phases:
1. The cards are dealt to the player and the dealer
2. The player gets their turn
3. The dealer gets their turn

Both the player and the dealer get dealt two cards initially. Both of the player's cards are face-up and only one of the dealer's cards are
face up. So, a start of a blackjack game may look like this:\
player hand: 7 + 10, dealer hand: Q + ?

The dealer's second card is only revealed during the dealer's turn after the player(s) finish.

**Importantly**, the dealer cannot player however they want. They must follow a set rule. This rule can have small variations from casino to casino, but
generally a dealer will keep drawing cards until they get to at least a hand total of 17. Whenever the dealer gets a hand total of 17 or higher, they must
stop drawing cards and end their turn. This includes if they went over 21 (which we call 'busting').

The player has 4 main actions they can do, and sometimes a 5th if the casino allows. These actions are 'stand', 'hit', 'double', 'split', and 'surrender.'
* 'stand' means the player ends their turn
* 'hit' means the player takes a card from the deck
  * after a 'hit', the player can no longer do anything else other than 'hit' or 'stand'
* 'double' means the player agrees to only take one card from the deck, having to end their turn (for that hand) immediately afterwards. In exchange, they
can double their starting bet. (the player can still win or lose their bet, it is just doubled)
* 'split' can only be done if the player has two cards (and only two cards) in their hand that have the same numberical value. For example, if you had a
hand with an 8 + 8, you could split your hand into two hands:
  * original_hand = 8_of_hearts, 8_of_spades -> new_hand_1 = 8_of_hearts + ?, new_hand_2 = 8_of_spades + ?\
    the ? are then filled in by drawing cards from the deck, so you're new hands might look like new_hand_1 = 8_of_hearts + 10_of_clubs, new_hand_2 = 8_of_spades + 3_of_diamonds
* 'surrender' is not a decision always offered to players, but when offered it allows the player to 'give up' their hand in exchange for losing half of their original bet.

What is betting?\
So, before any cards are dealt you need to bet money. Technically you need to bet money for each hand you want to play, but this simulation just assumes your going to play one hand to start (it does take into consideration that you may end up with more hands later in the game if you split).

For example, If you start by betting $25.00:
* if you 'double' you would need to wager an additional $25.00 to double your bet to $50.00
* if you 'split', because you gain an additional hand, the additional hand also needs a bet associated with it. This new bet ends up matching the bet of the pre-split hand
    * so if you intend to split, it costs the same as 'double'
* if you 'surrender' you would forfeit your hand and receive $12.5 back

If the player beats the dealer they recieve however much they bet on the hand from the dealer.
* If you originally bet $25.00 on a hand and that hand beats a dealer, then you keep your own $25.00 and take an $25.00 from the dealer

If the player loses, they lose the original bet they put on the hand.

Every hand individually completes with the dealer's hand, so it is possible to have one hand win vs. the dealer while the other loses... again for our purposes, this would only occur if the player had previously split their hands.

How betting works makes 'double' and 'split' equally lucrative and risky, though as we'll see from the simulation, their are times when it is to your advantage to 'double' or 'split'.

Finally, a blackjack is when the player or dealer get a hand total of 21 with their first two cards i.e. 10,Ace; Jack,Ace; Queen,Ace; King,Ace
* If the player gets a blackjack they get paid out a bonus! This usually equates to 1.5*the_original_bet, but it can vary by casino
* If the dealer gets a blackjack it immediately ends the game. Unless the player also has a blackjack, the player immediately loses their bet
* If both player and dealer have a blackjack, it is called a 'push', which is just a fancy way to say tie; the player does not gain or lose money

Those are the basics of blackjack, I'll list a few additional things that are helpful to know below.

#### Other Things You Should Know
* Any hand that contains an Ace, who's value is 11, is considered a **soft hand**
  * Called 'soft' because the Ace can still turn into a 1 in the case the player/dealer needs it to
  * If a hand has an Ace but the ace's value is 1, it is **NOT** considered a **soft hand** anymore
* Any hand that is not **soft** is considered a **hard hand**
* When splitting Aces or 10s, it is possible for one of the resulting hands to get a blackjack. We call this an "unnatural." Unfortunately, it is not considered a blackjack and the player will not be paid out a bonus

#### Common Casino Rules and Their Variations
* Dealer Hits on Soft 17: usually, casinos have dealer's hit on **soft 17** in order to potentially get a better hand
  * Sometimes you'll see "dealer stands on **soft 17**" which means the dealer will not hit but end their turn
* Available Player Decisions: 'stand','hit','double','split'
  * Sometimes 'surrender' is also allowed
  * Sometimes casino's will not allow a player to 'double' after they have 'split'
* Deck Length: refers to the number of decks a casino is using at a blackjack table. They usually use ~7 to form a massive deck.
* Blackjack Bonus: is usually 1.5*the_original_bet --a.k.a as "blackjack pays 3:2"
  * Sometimes this varies, another common ratio is "blackjack pays 6:5", which is 1.1*the_original_bet

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
Player splittable hands can only have the following hard hand totals: (20, 18, 16, 14, 12, 10, 8, 6, 4, 2, 12*)
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
There is a Jupyter notebook included within the github files called **chart_generation_notebook.ipynb**. It reads in the .csv files with the simulation data generated by **main.py** and organizes it into dataframes. The following dataframes contain the following information:
* dataframe 1
* dataframe 2
* dataframe 3
* dataframe 4

## How Do I Run My Own Simulations Using This Code?
1. Open a terminal and navigate to the location where you want the repository downloaded to

3. Type the command below into the terminal to clone the repository
    ```console
    git clone https://github.com/developer-hchan/Blackjack_Strategy_Simulation
    ```
4. Use the terminal to navigate into the repository you just downloaded
5. I would recommend using a virtual environment to install the required packages for the program. Here is how to make one with Python's builtin venv
Here is the link on how to create and activate a Python environemnt using Python's builtin venv: https://docs.python.org/3/library/venv.html

6. After activating your venv, run the following command in the terminal to download all the required packages.
    ```console
    pip install -r ./requirements.txt
    ```

7. If you just want to run the simulation with default settings then you can just type the following command:
    ```console
    python main.py
    ```

8. After running the program the following will happen:
    * a .csv file containing all the hard hand and soft hand cases will be generated. It is called data.csv
    * a .csv file containing all the splittable hand cases will be generated. It is called data_split.csv
    * The basic strategy chart will be generated as a .html file. It is called basic_strategy_chart.html
      * you can open basic_strategy_chart.html with any modern web browser i.e. Microsoft Edge, Chrome, Firefox, etc...

9. If you want to adjust the settings for the simulation, open main.py in your favorite code editor. At the top you'll see a dictionary named "config" that contains all the adjustable settings. All the settings and their valid inputs are listed below.

![config-screenshot](https://github.com/user-attachments/assets/47996fdb-231c-4828-9486-540c4838f6a4)

* 'number_of_sims' refers to how many times a blackjack case is simulated. It takes any int as a valid input
* 'decisions' refers to the available decisions a player can make during their turn. The valid inputs are listed below
    * ('stand','hit','double','surrender')
    * ('stand','hit','double')
    * ('stand','hit','surrender')
    * ('stand','hit')
* 'deck_length' refers to how many regular decks (52 decks) are in the game deck. It takes any int as a valid input
* 'shuffle' refers to if the deck is shuffled before play begins (the deck is only really not shuffled for testing purposes). Valid inputs are 'True' and 'False'.
* 'kill' refers to randomizing how much of the deck has been played prior to the current simulation. Valid inputs are 'True' and 'False'
* 'bet' refers to how much money is bet for each hand in every game. Valid inputs are floats rounded to the 2nd decimal place.
* 'blackjack_bonus' refers to the % bonus applied to a player's bet if they get a blackjack. Valid inputs are floats rounded to the 2nd decimal place.
    * the can be typed in like: 1.5
    * or: round(3/2, 2)
* 'dealer_hits_soft_17' refers to whether or not the dealer hits on soft 17. Valid inputs are 'True' and 'False'.
* 'double_after_split' refers to whether the player is allowed to 'double' after a 'split'. Valid inputs are 'True' and 'False'


