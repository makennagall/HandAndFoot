#!/usr/bin/env python3

import sys
import os
from random import shuffle

class Card:
    values = ["2", "3", "4", "5", "6", "7", "8", "9", "10",
              "Jack", "Queen", "King", "Ace", "Joker"]
    colors = ["Red", "Black", "Wild"]
    points = [0, 5, 10, 20, 50, 500]

    #constructor:
    def __init__(self, v, c, p):
        self.value = v
        self.color = c
        self.point = p

    #returns a string that represents the card for print functions:
    def __repr__(self):
        v = self.colors[self.color] + " " + self.values[self.value]
        return v
    #returns a string that represents the card when passed through the str() function:
    def __str__(self):
        v = self.colors[self.color] + " " + self.values[self.value]
        return v
    #determines equivalence:
    def checkEquivalence(self, aString):
        if len(aString.split(' ')) != 2:
            return False
        stringColor = aString.split(' ')[0]
        stringValue = aString.split(' ')[1]
        if str(self.colors[self.color]) == stringColor and str((self.values[self.value])) == stringValue:
            return True
        else:
            return False
    #Returns the card's value:
    def get_value(self):
        return self.values[self.value]
    #Returns the card's point value:
    def get_points(self):
        return self.points[self.point]
    #Used for sorting:
    def __lt__(self, other):
        return self.values[self.value] < other.values[self.value]
    def __gt__(self, other):
        return self.values[self.value] > other.values[self.value]
    def __eq__(self, other):
        return self.values[self.value] == other.values[self.value]
class Deck:
    #Constructor:
    def __init__(self, numDecks):
        self.cards = []
        #add the appropriate number of decks to the list
        for deck in range(numDecks):
            for i in range(0,13):
                for j in range(2):
                    #create 5 point cards:
                    if i >= 2 and i <= 6:
                        self.cards.append(Card(i,j,1))
                        self.cards.append(Card(i,j,1))
                    #create 10 point cards:
                    elif (i >= 7 and i <= 11):
                        self.cards.append(Card(i,j,2))
                        self.cards.append(Card(i,j,2))
                    #create 20 point cards (Aces and 2s):
                    elif (i == 0 or i == 12):
                        self.cards.append(Card(i,j,3))
                        self.cards.append(Card(i,j,3))
                    #create 3s
                    elif i == 1:
                        #red 3s:
                        if j == 0:
                            self.cards.append(Card(i,j,5))
                            self.cards.append(Card(i,j,5))
                        #black 3s:
                        else:
                            self.cards.append(Card(i,j,0))
                            self.cards.append(Card(i,j,0))
                    else:
                        print("error: i is " + str(i))

            #add the jokers to the deck:
            self.cards.append(Card(13,2,4))
            self.cards.append(Card(13,2,4))
        shuffle(self.cards)
    #Returns the number of cards in the deck currently:
    def num_in_deck(self):
        return len(self.cards)
    #Removes a card from the deck:
    def rm_card(self):
        if len(self.cards) == 0:
            #returns None if there are no more cards in the deck list
            return
        return self.cards.pop()
    #Used to print all the cards in the deck with the print function:
    def __repr__(self):
        v = ''
        for card in self.cards:
            v = v + card
        return v
class Player:
    #player constructor:
    def __init__(self, name):
        self.points = 0
        self.hand = []
        self.playedCards = {}
        self.foot = []
        self.footAccess = False
        self.name = str(name)

    #function that allows a Player to be printed
    def __repr__(self):
        playerCards = ''
        stringPlayed = ''
        for value in self.playedCards:
            stringPlayed = stringPlayed + str(value) + ": "
            for card in self.playedCards[value]:
                stringPlayed = stringPlayed + str(card)
            stringPlayed = stringPlayed + "\n"
        for card in self.hand:
            playerCards = playerCards + str(card) + ', '
        v = self.name + " has " + str(self.points) + " points. \nTheir hand contains the cards:\n" + playerCards + "and they have played the cards:\n " + stringPlayed
        return(v)
    #Sorts the hand based on the value:
    def sort_hand(self):
        self.hand.sort(key=lambda x: x.value)
    #Sorts the foot based on the value:
    def sort_foot(self):
        self.foot.sort(key=lambda x: x.value)
    #Updates the points the player has laid down:
    def updatePoints(self):
        points = 0
        for key in self.playedCards:
            for card in self.playedCards[key]:
                points = points + int(card.get_points())
        self.points =  points
    #Displays the player's hand:
    def display_hand(self):
        displayString = ''
        for num, card in enumerate(self.hand):
            displayString = displayString + str(card)
            if num < len(self.hand) - 1:
                displayString = displayString + ", "
        print(displayString)
    #Used to calculate points including points from books and negatives at the end of the round:
    def calculatePoints(self):
        totalPoints = 0
        #Calculate negatives:
        for card in self.hand:
            totalPoints = totalPoints - card.get_points()
        #If the player is not in their foot, those cards count as negative:
        if self.footAccess == False:
            for card in self.foot:
                totalPoints = totalPoints - card.get_points()
        unnaturals, naturals = self.check_books()
        totalPoints = totalPoints + (unnaturals * 300)
        totalPoints = totalPoints + (naturals * 500)
        totalPoints = totalPoints + self.points
        return totalPoints

    #Used to find how many naturals and unnaturals a player has:
    def check_books(self):
        unnaturals = 0
        naturals = 0
        for key in self.playedCards:
            if len(self.playedCards[key]) >= 7:
                wildPresent = False
                for card in self.playedCards[key]:
                    if card.get_value() == '2' or card.get_value() == 'Joker':
                        wildPresent = True
                if wildPresent == True:
                    unnaturals += 1
                else:
                    naturals += 1
        return unnaturals, naturals

class Game:
    #game constructor:
    def __init__(self):
        name1 = input("Player One Name: ")
        name2 = input("Player Two Name: ")
        numberOfDecks = 5
        self.deck = Deck(numberOfDecks)
        self.p1 = Player(name1)
        self.p2 = Player(name2)
    #Function that starts each round
    def play_game(self):
        Player1Points = 0
        Player2Points = 0
        print("Round 1: ")
        Round1 = Round(50, self.p1, self.p2)
        Round1.play_round()
        Player1Points += self.p1.calculatePoints()
        Player2Points += self.p2.calculatePoints()
        print("Round 2: ")
        Round2 = Round(90, self.p2, self.p1)
        Round2.play_round()
        Player1Points += self.p1.calculatePoints()
        Player2Points += self.p2.calculatePoints()
        print("Round 3: ")
        Round3 = Round(120, self.p1, self.p2)
        Round3.play_round()
        Player1Points += self.p1.calculatePoints()
        Player2Points += self.p2.calculatePoints()
        print("Round 4: ")
        Round4 = Round(150, self.p2, self.p1)
        Round4.play_round()
        Player1Points += self.p1.calculatePoints()
        Player2Points += self.p2.calculatePoints()
class Round:
    #Round Constructor:
    def __init__(self, pointsNeeded, p1, p2):
        self.pointsNeeded = pointsNeeded
        self.deck = Deck(5)
        self.train = []
        self.p1 = p1
        self.p2 = p2
    #Initializes values at the start of each round:
    def start_round(self):
        #deals 11 cards from the deck and removes these cards from the deck
        self.p1.hand = [self.deck.rm_card() for i in range(11)]
        self.p1.foot = [self.deck.rm_card() for i in range(11)]
        self.p1.points = 0
        self.p1.footAccess = False
        self.p1.playedCards = {}
        self.p1.sort_hand()
        self.p1.sort_foot()
        self.p2.hand = [self.deck.rm_card() for i in range(11)]
        self.p2.foot = [self.deck.rm_card() for i in range(11)]
        self.p2.points = 0
        self.p2.footAccess = False
        self.p2.playedCards = {}
        self.p2.sort_hand()
        self.p2.sort_foot()
    #Displays the train with indexes:
    def display_train(self):
        print("Current Train: ")
        if len(self.train) == 0:
            print("Empty")
        else:
            for num, card in enumerate(self.train):
                print(str(num) + " " + str(card))
    #Switches back and forth between player and allows them to play:
    def play_round(self):
        #each player has turns as long as no one goes out and the deck has cards in it
        currPlayer = self.p1
        self.start_round()
        GameOver = False
        while GameOver == False:
            #Clear the screen:
            os.system("clear")
            newPlay = Play(currPlayer, self)
            GameOver = newPlay.play()
            currPlayer.updatePoints()
            if currPlayer == self.p1:
                currPlayer = self.p2
            else:
                currPlayer = self.p1
    #Print a Round using the print() function:
    def __repr__(self):
        v = self.p1.name + " has " + str(self.p1.points) + " points in this round. \n" + self.p2.name + " has " + str(self.p2.points) + " points in this round.\nThe deck contains " + str(self.deck.num_in_deck()) + " cards.\nThe train contains " + str(len(self.train)) + " cards."
        return v

class Play:
    #Play Constructor:
    def __init__(self, player, round):
        self.player = player #should be of type player
        self.initialHand = self.player.hand.copy()
        self.initialFoot = self.player.foot.copy()
        self.initialLaid = self.player.playedCards.copy()
        self.round = round
    #MAIN Function:
    def play(self):
        print(self.player)
        self.round.display_train()
        validMove = False
        while validMove == False:
            draw = input("Would you like to draw two cards (y/n): ")
            if not('n' in str(draw)) and not('y'in str(draw)):
                print("Please enter either y or n. You entered: " + str(draw))
                validMove = False
                continue
            if 'n' in str(draw):
                if self.player.points < self.round.pointsNeeded:
                    print("You must lay down cards to pick up from the train")
                    self.playSets()
                    self.player.updatePoints()
                if self.player.points > self.round.pointsNeeded:
                    validMove = self.pickUpTrain()
                else:
                    print("You still do not have enough points.")
                    self.player.hand = self.initialHand
                    self.player.playedCards = self.initialLaid
                    validMove = self.drawTwo()
            else:
                validMove = self.drawTwo()
        addSets = input("Would you like to add sets (y/n)? ")
        while 'y' not in addSets and 'n' not in addSets:
            addSets = input("Would you like to add sets (y/n)? ")
        if str('y') in str(addSets):
            self.playSets()
            self.player.updatePoints()
            if self.player.points < self.round.pointsNeeded:
                print("You do not have enough points to lay down.")
                self.player.hand = self.initialHand
                self.player.display_hand()
                self.player.playedCards = self.initialLaid
                self.player.updatePoints()
            #Game over = True
        if self.checks() == True:
            return True
        validDiscard = False
        while validDiscard == False:
            validDiscard = self.discard()
        print("Discarded")
        #Game over = True
        if self.checks() == True:
            print("Game Over")
            return True
        else:
        #Game over = False
            print("Game Not Over")
            return False
    #Allows the player to play multiple sets:
    def playSets(self):
        self.playSet()
        keepPlaying = input("Would you like to lay down more cards(y/n)? ")
        while 'y' not in keepPlaying and 'n' not in keepPlaying:
            keepPlaying = input("Would you like to lay down more cards(y/n)? ")
        while keepPlaying == 'y':
            self.checks()
            self.playSet()
            self.player.updatePoints()
            print("You have " + str(self.player.points) + " points.")
            keepPlaying = input("Would you like to lay down more cards(y/n)? ")
            while 'y' not in keepPlaying and 'n' not in keepPlaying:
                keepPlaying = input("Would you like to lay down more cards(y/n)? ")
    #Allows the player to discard one card at the end of the turn:
    def discard(self):
        discardString = input("What card would you like to discard? ")
        cardRemoved = False
        for num, card in enumerate(self.player.hand):
            if card.checkEquivalence(discardString) == True:
                self.round.train.append(card)
                self.player.hand.pop(num)
                cardRemoved = True
                break
        if cardRemoved == True:
            return True
        else:
            return False
    #Allows the player to draw two cards at the beginning of the turn:
    def drawTwo(self):
        newCard1 = self.round.deck.rm_card()
        newCard2 = self.round.deck.rm_card()
        print("New Cards: ")
        print(newCard1)
        print(newCard2)
        self.player.hand.append(newCard1)
        self.player.hand.append(newCard2)
        self.player.sort_hand()
        self.player.display_hand()
        self.initialHand = self.player.hand.copy()
        return True
    #Allows the player to pick up the train if they have two of that same card in their hand:
    def pickUpTrain(self):
        cardCount = 0
        if self.player.points < self.round.pointsNeeded:
            print("You do not have enough points.")
            return False
        if len(self.round.train) == 0:
            print("The train is empty.")
            return False
        isValid = False
        while isValid == False:
            index = input("What index would you like to pick up the train from? ")
            isValid = index.isdigit()
        index = int(index)
        if len(self.round.train) < index:
            print("Index out of range. Try Again.")
            return False
        #If the player is trying to pick up the last card on the train:
        if index == len(self.round.train) - 1:
            self.player.hand.append(self.round.train[index])
            self.round.train.remove(self.round.train[index])
            return True
        if str(self.round.train[index].get_value()) == str(3):
            print("You cannot pick up from a 3")
            return False
        if str(self.round.train[index].get_value()) == str(2):
            print("You cannot pick up from a 2")
            return False
        if str(self.round.train[index].get_value()) == "Joker":
            print("You cannot pick up from a Joker")
            return False
        for card in self.initialHand:
            if card.value == self.round.train[index].value:
                cardCount = cardCount + 1
        if cardCount >= 2:
            print("Taking from Train...")
            for card in self.round.train[index:]:
                self.player.hand.append(card)
                self.round.train.remove(card)
            self.player.sort_hand()
            self.player.display_hand()
        else:
            print("You do not have enough " + str(self.round.train[index].get_value()))
            return False
        return True
    #Allows the player to play cards of a single value and add wilds to that set:
    def playSet(self):
        value = input("What card value would you like to lay down? ")
        number = input("How many of that value would you like to lay down? ")
        jokers = input("How many jokers would you like to lay down with your set? ")
        twos = input("How many twos would you like to lay down with your set? ")
        if number.isdigit() == False:
            print("invalid input: did not enter a number")
            return False
        if jokers.isdigit() == False:
            print("invalid input: did not enter a number")
            return False
        if twos.isdigit() == False:
            print("invalid input: did not enter a number")
            return False
        number = int(number)
        jokers = int(jokers)
        twos = int(twos)
        cardList = []
        newHF = []
        if str(value) == str(3):
            print("You cannot make a set of 3s")
            return False
        changeList = self.player.hand.copy()
        numInPlayerCards = 0
        numJokers = 0
        numTwos = 0
        for card in changeList:
            added = False
            if numInPlayerCards != number:
                if card.get_value() == value:
                    cardList.append(card)
                    numInPlayerCards += 1
                    added = True
            if numJokers != jokers:
                if card.get_value() == 'Joker':
                    cardList.append(card)
                    numJokers += 1
                    added = True
            if numTwos != twos:
                if card.get_value() == '2':
                    cardList.append(card)
                    numTwos += 1
                    added = True
            if added == False:
                newHF.append(card)

        if numInPlayerCards < number:
            print("You do not have that many " + value + "s.")
            return False
        if numJokers < jokers:
            print("You do not have that many jokers.")
            return False
        if numTwos < twos:
            print("You do not have that many twos.")
            return False
        if value not in self.player.playedCards:
            self.player.playedCards[value] = []
        for card in cardList:
            newList = self.player.playedCards[value].append(card)
        if len(newList) < 3:
            print("Not enough cards in set")
            return False
        wildsInSet = 0
        for card in newList:
            if card.get_value() == '2' or card.get_value() == 'Joker':
                wildsInSet += 1
        if wildsInSet >= len(newList):
            print("You do not have enough value cards for your number of wilds")
            return False
        #update player's playedCards and hand
        self.player.playedCards[value] = newList
        self.player.hand = newHF
        self.player.display_hand()
    #Checks if the player goes into their foot or if the round is over:
    def checks(self):
        if self.player.footAccess == False:
            if len(self.player.hand) == 0:
                #If they player has 0 cards in their hand, then their hand is set equal to their foot.
                print("You are now in your foot")
                self.player.footAccess == True
                self.player.hand = self.player.foot
                self.player.display_hand()
        else:
            if len(self.player.hand) == 0:
                unnaturals, naturals = self.player.check_books()
                if unnaturals >= 1 and naturals >= 1:
                    #Game Over = True
                    print("Round Over")
                    return True
                else:
                    #The player does not have enough books to go out:
                    print("You need to retain cards in your hand in order to discard.")
                    self.player.hand = self.initialHand
                    self.player.playedCards = self.initialLaid
                    print("Your initial hand and played cards have been restored.")
        #Game over = False
        return False

game1 = Game()
game1.play_game()
