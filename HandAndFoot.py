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
        self.playedCards = []
        self.foot = []
        self.footAccess = False
        self.name = name

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
        Round1 = Round(50, self.p1, self.p2)
        Round1.play_round()
        print(Round1)
        Round2 = Round(90, self.p1, self.p2)
        Round2.play_round()
        Round3 = Round(120, self.p1, self.p2)
        Round3.play_round()
        Round4 = Round(150, self.p1, self.p2)
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
        self.p1.points = 0
        self.p1.footAccess = False
        self.p1.playedCards = []
        print(self.p1)
        self.p2.hand = [self.deck.rm_card() for i in range(11)]
        self.p2.foot = [self.deck.rm_card() for i in range(11)]
        self.p2.points = 0
        self.p2.footAccess = False
        self.p2.playedCards = []
        print(self.p2)

    def play_round(self):
        #each player has turns as long as no one goes out and the deck has cards in it
        self.start_round()
        print(self)
    def __repr__(self):
        v = "Player One has " + str(self.p1.points) + " points in this round. \nPlayer Two has " + str(self.p2.points) + " points in this round.\nThe deck contains " + str(self.deck.num_in_deck()) + " cards.\nThe train contains " + str(len(self.train)) + " cards."
        return v

class Play:
    def __init__(self, player):
        self.player = player #should be of type player
        if self.player.footAccess == False:
            self.initialHand = self.player.hand
        else:
            self.initialHand = self.player.foot
        self.initialLaid = self.player.playedCards

game1 = Game()
game1.play_game()
