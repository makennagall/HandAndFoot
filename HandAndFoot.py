#!/usr/bin/env python3

import sys
from random import shuffle

class Card:
    values = ["2", "3", "4", "5", "6", "7", "8", "9", "10",
              "Jack", "Queen", "King", "Ace", "Joker"]
    color = ["red", "black", "wild"]
    points = [0, 5, 10, 20, 50, -300]

    #constructor:
    def __init__(self, v, c, p):
        self.value = v
        self.color = c
        self.point = p

    #returns a string that represents the card:
    def __repr__(self):
        v = self.values[self.value] + " of " + self.suits[self.suit]
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
                    if i >= 8 and i <= 11:
                        self.cards.append(Card(i,j,2))
                        self.cards.append(Card(i,j,2))
                    #create 20 point cards (Aces and 2s):
                    if i == 0 or i == 12:
                        self.cards.append(Card(i,j,3))
                        self.cards.append(Card(i,j,3))
                    #create 3s
                    if i == 1:
                        #red 3s:
                        if j == 0:
                            self.cards.append(Card(i,j,5))
                            self.cards.append(Card(i,j,5))
                        #black 3s:
                        else:
                            self.cards.append(Card(i,j,0))
                            self.cards.append(Card(i,j,0))
            #add the jokers to the deck:
            self.cards.append(Card(13,3,4))
            self.cards.append(Card(13,3,4))

    def rm_card(self):
        if len(self.cards) == 0:
            #returns None if there are no more cards in the deck list
            return
        return self.cards.pop()
    def shuffle(self):
        random.shuffle(self.deck)
class Player:
    #player constructor:
    def __init__(self, name):
        self.points = 0
        self.hand = []
        self.foot = []
        self.name = name
class Game:
    #game constructor:
    def __init__(self):
        name1 = input("Player One Name: ")
        name2 = input("Player Two Name: ")
        numberOfDecks = input("Number of Decks: ")
        self.deck = Deck(numberOfDecks)
        self.p1 = Player(name1)
        self.p2 = Player(name2)

    def draw(self, player):
