debug=0 #debug is set to off
#-------------------------modules-------------------------
import os, random, time, sys, math, cmath, numpy as np; from colorama import init as cinit, Fore
cinit()

#--------------------------setup--------------------------


#-----------------------function(s)-----------------------
def check(card1, card2): #function to check if card play is valid
    return card1.colour == "W" or card1.colour == card2.colour or card1.value == card2.value #if valid then return true else return false

#-------------------------classes-------------------------
class Card: 
    def __init__(self, suit, value):
        self.suit=suit
        self.value=value

    def format(self):
        return f"{self.suit} {self.value}" 
        "" 
    "" #base class for cards, contains attribues common to most card games

class UnoCard(Card):
    power_dict={0:"PC", 1:"+4", 10:"+2", 11:"Re", 12:"Sk"} #translates numbers to special cards, 0 and 1 applying to Wild cards only
    """ Uno Rules
        108 cards as follows
        19 Blue cards – 0-9 
        19 Green cards – 0-9 
        19 Red cards – 0-9 
        19 Yellow cards – 0-9
        8 Draw Two cards – 2 each in blue, green, red, and yellow
        8 Reverse cards – 2 each in blue, green, red, and yellow
        8 Skip cards – 2 each in blue, green, red, and yellow
        4 Wild cards 
        4 Wild Draw Four cards 
    """
    def __init__(self, colour="R", value=4, debug=""):
        if debug=="":
            debug=f"{colour} {value}"
        if not (colour:=colour.upper()) in ["R", "B", "Y", "G", "W"]: raise ValueError(f"{debug}, {colour} is an invalid colour!")
        if not (value in [i for i in range(13)] if colour!="W" else value in [0, 1]): raise ValueError(
        f"""{debug}
    {value} is an invalid value for this colour!
    Accepted for {colour}: {(', '.join([str(i) for i in range(13)]) if colour!='W' else '0, 1')}""")
        super().__init__(colour, value)
        self.colour=colour
        self.value=value
        self.db=debug

    def format(self):
        return (rf"[{self.suit}"
            .replace("B", Fore.BLUE+"B")
            .replace("R", Fore.RED+"R")
            .replace("G", Fore.GREEN+"G")
            .replace("Y", Fore.YELLOW+"Y")
            .replace("W", Fore.CYAN+"W")
            +rf" {Fore.MAGENTA+(' '+str(self.value) if self.value<10 and self.colour!='W' else self.power_dict[self.value])+Fore.RESET}]")

class Player:
    def __init__(self, name, score=0):
        self.name=name
        self.hand=[]
        self.score=score

    def show_hand(self):
        return ("[ "+(" | ".join([i.format() for i in self.hand]))+" ]")

    def draw(self, deck, show=False, amount=1):
        for i in range(amount):
            self.hand.append(_:=deck.pop(0))
            if show: print(f"{_.format()} was drawn.")
        return deck

    def play(self, game, card_num):
        if check(self.hand[card_num], game.top):
            print(f"Card {self.hand[card_num].format()} was played.\n")
            game.top=self.hand.pop(card_num)
        else:
            print(f"You must play {game.top.colour} or {game.top.value}.\n")
            return False
        return True

    def turn(self, game):
        print("Hand:", self.show_hand())
        try:
            was_valid=0
            while not was_valid:
                if (entered:=input("What number card to play? ")).lower()=="draw":
                    self.draw(game.deck, True)
                    print("\nHand:", self.show_hand())
                    continue
                assert (card_to_play:=int(entered)-1) in range(0, len(self.hand))
                if debug: print(self.hand[card_to_play].format())
                was_valid = self.play(game, card_to_play)               
        except Exception as e:
            print(f"Invalid input! Please enter an integer between 1 and {len(self.hand)}.\n")
            return self.turn(game)
        if len(self.hand)==0:
            return False
        return True

class Game:
    def __init__(self, list_of_players=[Player("default")], deck=[UnoCard("r", 8)]):
        self.ogdeck=deck
        self.deck=deck
        self.players=(list_of_players if type(list_of_players) in [tuple, list] else [list_of_players])
        self.turn=0
        
    def all_draw(self, amount=7):
        for x in range(amount):
            for e in self.players:
                deck=e.draw(self.deck)
        return deck
    
    def round(self):
        self.deck=self.ogdeck
        self.all_draw()
        self.top=self.deck.pop(0)
        game_over=0
        i=-1
        while not game_over:
            print(f"The current card is {self.top.format()}.\n")
            i+=1
            game_over=self.players[i].turn(self)

#--------------------------setup--------------------------


#------------------------main line------------------------
temp, deck={}, []
temp[0]=[[UnoCard(c, math.ceil(n/2)) for c in "RGBY"] for n in range(19)]
temp[1]=[[UnoCard(c, math.ceil(n/2)) for c in "RGBY"] for n in range(19, 25)]
temp[2]=[[UnoCard("W", math.ceil(n/4)) for n in range(-3, 5)]]
for i in temp: 
    for a in temp[i]: 
        for b in a: deck.append(b)

for x in range(random.randint(1, 10)):
    random.shuffle(deck)
game=Game((ved:=Player("ved"), g:=Player("tan")), deck)
if debug: print(" | ".join([i.format() for i in game.deck]))

if debug: print(f"\n".join([f"{game.players[i].name}: {game.players[i].show_hand()}" for i in range(2)]))
if debug: print(" | ".join([i.format() for i in game.deck]))

game.round()

input("Press Enter to exit the script...")
