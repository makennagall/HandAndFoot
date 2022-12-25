#!/usr/bin/env python3

import sys
import os
from random import shuffle

class Card:
    values = ["Joker", "2", "3", "4", "5", "6", "7", "8", "9", "10",
              "Jack", "Queen", "King", "Ace"]
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
    def get_color(self):
        return self.colors[self.color]
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
            for i in range(1,14):
                for j in range(2):
                    #create 5 point cards:
                    if i >= 3 and i <= 7:
                        self.cards.append(Card(i,j,1))
                        self.cards.append(Card(i,j,1))
                    #create 10 point cards:
                    elif (i >= 8 and i <= 12):
                        self.cards.append(Card(i,j,2))
                        self.cards.append(Card(i,j,2))
                    #create 20 point cards (Aces and 2s):
                    elif (i == 1 or i == 13):
                        self.cards.append(Card(i,j,3))
                        self.cards.append(Card(i,j,3))
                    #create 3s
                    elif i == 2:
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
            self.cards.append(Card(0,2,4))
            self.cards.append(Card(0,2,4))
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
        self.hand = {}
        values = ["Joker", "2", "3", "4", "5", "6", "7", "8", "9", "10",
                  "Jack", "Queen", "King", "Ace"]
        for value in values:
            self.hand[value] = []
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
        for value in self.hand:
            if len(self.hand[value]) > 0:
                playerCards = playerCards + str(value) + "(" + str(len(self.hand[value])) + "): "
                for num, card in enumerate(self.hand[value]):
                    playerCards = playerCards + str(card)
                    if num < len(self.hand[value]) - 1:
                        playerCards = playerCards + ", "
                playerCards = playerCards + "\n"
        v = self.name + " has " + str(self.points) + " points. \nTheir hand contains the cards:\n" + playerCards + "\nand they have played the cards:\n " + stringPlayed
        return(v)
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
        playerCards = self.name + "\'s hand:\n"
        for value in self.hand:
            if len(self.hand[value]) > 0:
                playerCards = playerCards + str(value) + "(" + str(len(self.hand[value])) + "): "
                for num, card in enumerate(self.hand[value]):
                    playerCards = playerCards + str(card)
                    if num < len(self.hand[value]) - 1:
                        playerCards = playerCards + ", "
                playerCards = playerCards + "\n"
        return playerCards
    #Used to calculate points including points from books and negatives at the end of the round:
    def calculatePoints(self):
        totalPoints = 0
        #Calculate negatives:
        for value in self.hand:
            for card in self.hand[value]:
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
        #Add cards to hand dictionary for p1:
        for i in range(11):
            newCard = self.deck.rm_card()
            self.p1.hand[newCard.get_value()].append(newCard)
        self.p1.foot = [self.deck.rm_card() for i in range(11)]
        self.p1.points = 0
        self.p1.footAccess = False
        self.p1.playedCards = {}
        self.p1.sort_foot()
        #Add cards to hand dictionary for p2:
        for i in range(11):
            newCard = self.deck.rm_card()
            self.p2.hand[newCard.get_value()].append(newCard)
        self.p2.foot = [self.deck.rm_card() for i in range(11)]
        self.p2.points = 0
        self.p2.footAccess = False
        self.p2.playedCards = {}
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
        print("Playable points: " + str(self.playable_points()))
        addSets = input("Would you like to add sets (y/n)? ")
        while 'y' not in addSets and 'n' not in addSets:
            addSets = input("Would you like to add sets (y/n)? ")
        if str('y') in str(addSets):
            self.playSets()
            self.player.updatePoints()
            if self.player.points < self.round.pointsNeeded:
                print("You do not have enough points to lay down.")
                self.player.hand = self.initialHand
                print(self.player.display_hand())
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
        if len(discardString.split(' ')) != 2:
            return False
        stringColor = discardString.split(' ')[0]
        stringValue = discardString.split(' ')[1]
        if stringValue in self.player.hand:
            if len(self.player.hand[stringValue]) > 0:
                for num, card in enumerate(self.player.hand[stringValue]):
                    if card.get_color() == stringColor:
                        self.round.train.append(card)
                        self.player.hand[stringValue].pop(num)
                        cardRemoved = True
                        break
        else:
            return False
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
        self.player.hand[newCard1.get_value()].append(newCard1)
        self.player.hand[newCard2.get_value()].append(newCard2)
        print(self.player.display_hand())
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
            self.player.hand[self.round.train[index].get_value()].append(self.round.train[index])
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
                self.player.hand[card.get_value()].append(card)
                self.round.train.remove(card)
            print(self.player.display_hand())
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
        if value not in self.player.hand:
            print("invalid input: did not enter a valid value")
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
        addedCards = []
        if str(value) == str(3):
            print("You cannot make a set of 3s")
            return False
        newHand = self.player.hand.copy()
        if len(newHand[value]) < number:
            print("You do not have that many " + value + "s.")
            return False
        else:
            for num in range(number):
                addedCards.append(newHand[value].pop())
        if len(newHand['2']) < twos:
            print("You do not have that many twos.")
            return False
        else:
            for num in range(twos):
                addedCards.append(newHand['2'].pop())
        if len(newHand['Joker']) < jokers:
            print("You do not have that many jokers.")
            return False
        else:
            for num in range(jokers):
                addedCards.append(newHand['Joker'].pop())

        if value not in self.player.playedCards:
            newList = addedCards
        else:
            newList = self.player.playedCards[value]
            for card in addedCards:
                newList.append(card)

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
        self.player.hand = newHand
        print(self.player.display_hand())
    #Checks if the player goes into their foot or if the round is over:
    def checks(self):
        if self.player.footAccess == False:
            noHandCards = True
            for value in self.player.hand:
                if len(self.player.hand[value]) != True:
                    noHandCards = False
                    break
                #If they player has 0 cards in their hand, then their hand is set equal to their foot.
            if noHandCards == True:
                print("You are now in your foot")
                self.player.footAccess == True
                for card in self.player.foot:
                    self.player.hand[card.get_value].append(card)
                print(self.player.display_hand())
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

    def playable_points(self):
        print("You can play:")
        NumEng = {1:"One", 2:"Two", 3:"Three", 4:"Four", 5:"Five", 6:"Six", 7:"Seven", 8:"Eight", 9:"Nine", 10:"Ten", 11:"Eleven", 12:"Twelve", 13:"Thirteen", 14:"Fourteen", 15:"Fifteen", 16:"Sixteen", 17:"Seventeen", 18:"Eighteen", 19:"Nineteen", 20:"Twenty"}
        points = 0
        wilds = 0
        twoList = []
        greaterThree = 0
        wildList = []
        for value in self.player.hand:
            if value == "2" or value == "Joker":
                if len(self.player.hand[value]) > 0:
                    for card in self.player.hand[value]:
                        wildList.append(card)
            elif value == '3':
                continue
            else:
                #Can lay down set of cards:
                if len(self.player.hand[value]) >= 3:
                    greaterThree += 1
                    newPoints = (self.player.hand[value][0].get_points() * len(self.player.hand[value]))
                    print(NumEng[len(self.player.hand[value])] +  " " + str(value) + "s to add " + str(newPoints) + " points.")
                    points += newPoints
                elif len(self.player.hand[value]) == 2:
                    twoList.append(self.player.hand[value][0])
        twoList.sort(key=lambda x: x.point, reverse=True)
        wildList.sort(key=lambda x: x.point, reverse=True)
        while len(wildList) > 0 and len(twoList) > 0:
            newPoints = (twoList[0].get_points() * 2)
            print("Points from twoList: " + str(newPoints))
            newPoints += wildList[0].get_points()
            print("Two " + twoList[0].get_value() + "s and one " + wildList[0].get_value() + " to add " + str(newPoints) + " points.")
            points += newPoints
            wildList.pop(0)
            twoList.pop(0)
        if len(wildList) > 0:
            if greaterThree > 0:
                for card in wildList:
                    newPoints = card.get_points()
                    print("Play " + card.get_value() + " with other set to add " + str(newPoints) + " points.")
                    points += newPoints
        return points


game1 = Game()
game1.play_game()
