#!/usr/bin/env python3

import sys
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
    def get_value(self):
        return self.values[self.value]
class Deck:
    #constructor:
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
    def num_in_deck(self):
        return len(self.cards)
    def rm_card(self):
        if len(self.cards) == 0:
            #returns None if there are no more cards in the deck list
            return
        return self.cards.pop()
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
        for card in self.playedCards:
            stringPlayed = stringPlayed + str(card) + ", "
        if self.footAccess == False:
            for card in self.hand:
                playerCards = playerCards + str(card) + ', '
            v = self.name + " has " + str(self.points) + " points. \nTheir hand contains the cards:\n" + playerCards + "and they have played the cards:\n " + stringPlayed
        else:
            for card in self.foot:
                playerCards = playerCards + card
            v = self.name + " has " + str(self.points) + " points. \nTheir foot contains the cards:\n" + playerCards + "and they have played the cards:\n " + stringPlayed
        return(v)
class Game:
    #game constructor:
    def __init__(self):
        name1 = input("Player One Name: ")
        name2 = input("Player Two Name: ")
        numberOfDecks = 5
        self.deck = Deck(numberOfDecks)
        self.p1 = Player(name1)
        self.p2 = Player(name2)



    def play_game(self):
        print("Round 1: ")
        Round1 = Round(50, self.p1, self.p2)
        Round1.play_round()
        print(Round1)
        print("Round 2: ")
        Round2 = Round(90, self.p2, self.p1)
        Round2.play_round()
        print("Round 3: ")
        Round3 = Round(120, self.p1, self.p2)
        Round3.play_round()
        print("Round 4: ")
        Round4 = Round(150, self.p2, self.p1)
        Round4.play_round()
class Round:
    def __init__(self, pointsNeeded, p1, p2):
        self.pointsNeeded = pointsNeeded
        self.deck = Deck(5)
        self.train = []
        self.p1 = p1
        self.p2 = p2
    def start_round(self):
        #deals 11 cards from the deck and removes these cards from the deck
        self.p1.hand = [self.deck.rm_card() for i in range(11)]
        self.p1.foot = [self.deck.rm_card() for i in range(11)]
        self.p1.points = 50
        self.p1.footAccess = False
        self.p1.playedCards = []
        print(self.p1)
        self.p2.hand = [self.deck.rm_card() for i in range(11)]
        self.p2.foot = [self.deck.rm_card() for i in range(11)]
        self.p2.points = 50
        self.p2.footAccess = False
        self.p2.playedCards = []
        print(self.p2)

    def display_train(self):
        print("Current Train: ")
        for num, card in enumerate(self.train):
            print(str(num) + " " + str(card))

    def play_round(self):
        #each player has turns as long as no one goes out and the deck has cards in it
        currPlayer = self.p1
        self.start_round()
        while True:
            if str(input("If you would like to quit the game press q, otherwise hit enter")) == str('q'):
                break
            print(self)
            self.display_train()
            play1 = Play(currPlayer, self)
            play1.play()
            self.display_train()
            print(self)
            if currPlayer == self.p1:
                currPlayer = self.p2
            else:
                currPlayer = self.p1

    def __repr__(self):
        v = self.p1.name + " has " + str(self.p1.points) + " points in this round. \n" + self.p2.name + " has " + str(self.p2.points) + " points in this round.\nThe deck contains " + str(self.deck.num_in_deck()) + " cards.\nThe train contains " + str(len(self.train)) + " cards."
        return v

class Play:
    def __init__(self, player, round):
        self.player = player #should be of type player
        if self.player.footAccess == False:
            self.initialHand = self.player.hand
        else:
            self.initialHand = self.player.foot
        self.initialLaid = self.player.playedCards
        self.round = round

    def play(self):
        print(self.player)
        validMove = False
        while validMove == False:
            draw = input("Would you like to draw two cards (y/n): ")
            if draw == 'n':
                validMove = self.pickUpTrain()
            else:
                validMove = self.drawTwo()
        validDiscard = False
        while validDiscard == False:
            validDiscard = self.discard()
    def discard(self):
        discardString = input("What card would you like to discard? ")
        cardRemoved = False
        if self.player.footAccess == False:
            for card in self.player.hand:
                if card.checkEquivalence(discardString) == True:
                    self.round.train.append(card)
                    self.player.hand.remove(card)
                    cardRemoved = True
                    break
        else:
            for card in self.player.foot:
                if card.checkEquivalence(discardString) == True:
                    self.round.train.append(card)
                    self.player.foot.remove(card)
                    cardRemoved = True
                    break
        if cardRemoved == True:
            return True
        else:
            return False

    def drawTwo(self):
        newCard1 = self.round.deck.rm_card()
        newCard2 = self.round.deck.rm_card()
        print("New Cards: ")
        print(newCard1)
        print(newCard2)
        if self.player.footAccess == False:
            self.player.hand.append(newCard1)
            self.player.hand.append(newCard2)

        else:
            self.player.foot.append(newCard1)
            self.player.foot.append(newCard2)
        return True

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
            print(isValid)
            if len(self.round.train) < int(index):
                print("Index out of range. Try Again.")
                isValid = False
        index = int(index)
        #If the player is trying to pick up the last card on the train:
        if index == len(self.round.train) - 1:
            if self.player.footAccess == False:
                self.player.hand.append(self.round.train[index])
                self.round.train.remove(self.round.train[index])
            else:
                self.player.foot.append(self.round.train[index])
                self.round.train.remove(self.round.train[index])
            return True
        if str(self.round.train[index].value) == str(3):
            print("You cannot pick up from a 3")
            return False
        if str(self.round.train[index].value) == str(2):
            print("You cannot pick up from a 2")
            return False
        if str(self.round.train[index].value) == "Joker":
            print("You cannot pick up from a Joker")
            return False
        if self.player.footAccess == False:
            for card in self.player.hand:
                if card.value == self.round.train[index].value:
                    cardCount = cardCount + 1
            if cardCount >= 2:
                print("Taking from Train...")
                for card in self.round.train[index:]:
                    self.player.hand.append(card)
                    self.round.train.remove(card)
            else:
                print("You do not have enough " + str(self.round.train[index].get_value()))
                return False
        else:
            for card in self.player.foot:
                if card.value == self.round.train[index].value:
                    cardCount = cardCount + 1
            if cardCount >= 2:
                print("Taking from Train...")
                for card in self.round.train[index:]:
                    self.player.foot.append(card)
                    self.round.train.remove(card)
            else:
                print("You do not have enough " + str(self.round.train[index].get_value()))
                return False
        return True


game1 = Game()
game1.play_game()
