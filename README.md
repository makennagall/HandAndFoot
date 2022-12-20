# HandAndFoot
Implementation of the card game Hand and Foot

<b>Card Class</b> contains a constructor and representation function. Each card has variables for the color of the card, the value of the card, and the number of points the card is worth.

<b>Deck Class</b> contains a constructor and a function that removes a card from the deck. self.cards is a list of the cards in the deck.

<b>Player Class</b> contains a constructor that takes in the name of the player as an input. The Hand and foot variables are initialized to an empty list. footAccess is initialized to False because the player cannot access their foot cards until they play all cards from their hand. Points is initialized to zero because the player does not have any points until they play cards. playedCards represents the cards the player has put down. These cards contribute to their point totals.

<b>Game Class</b> contains a constructor function that initializes a deck, train and two players. Functions:
draw: draws two cards and appends them to either the hand or foot depending on the footAccess variable.

take train: checks if the player has the two cards they claim, if the two cards are in the train, and if the player has laid down points. then it appends the train from that card down to the players hand or foot depending on the footAccess variable.

lay down new set: checks if player has played cards of that type. takes in a list of sets that the player wants to lay down. removes cards from the hand or foot and adds it to the laid down cards list for that player. adds to the number of points the player has. Cannot lay down 3s. Must lay down 3 cards in each set. Sets must contain cards of the same value or wild cards. Wild cards cannot equal or out number value cards.

add to set: asks which set the player would like to add the card to. if the value matches then add card, else if the card is a wild card checks if there are not more wild cards than value cards. Updates point total.

discard: if player has the selected card in their hand (or foot) then remove it from their hand (or foot) and append it to the train list.

switch to foot: if hand set is empty, change footAccess to True.

end game: if a set contains 7 cards that are only value cards and a set contains 7 cards including a wild card and len(foot) == 0: end game

play game:
NOTES: need to figure out a way to keep track of what cards have been laid down in the round
<br>player determines whether they want to draw or pick up from the train.
if they want to pick up from the train and have 0 points prompt laying down cards
check if cards they have to lay down is greater than round point minimum, if yes lay down, else reprompt pick up from train or draw
<br>if points == 0
<br>&emsp; give opportunity to lay down
<br>&emsp; give opportunity to add to sets
<br>else:
<br>&emsp; give opportunity to add to sets
<br>if footAccess == False:
<br>&emsp; check switch to foot
<br>else:
<br>&emsp; check end game
<br>if footAccess == True:
<br>&emsp; if len(foot) == 0 and no natural and unnatural:
<br>&emsp; prompt undo of plays
<br>prompt discard
<br>if footAccess == False:
<br>&emsp; check switch to foot
<br>else:
<br>&emsp; check end game
<br>change player


Sources:
https://thecleverprogrammer.com/2020/10/04/card-game-with-python/
