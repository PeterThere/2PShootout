import threading
import random
import msvcrt
import curses

coords = [[6, 29], [10, 20], [14, 29], [10, 39], [6, 89], [10, 80], [14, 89], [10, 99]]
keys = ['w', 'a', 's', 'd', 'i', 'j', 'k', 'l']

def getch():
    return msvcrt.getch().decode('utf-8')

def generate_key1(screen):
    key = random.randint(0, 3)
    screen.addstr(coords[key][0], coords[key][1] , "🦆")
    screen.refresh()
    return key

def generate_key2(screen):
    key = random.randint(4, 7)
    screen.addstr(coords[key][0], coords[key][1], "🦆")
    screen.refresh()
    return key

class Game:
    def __init__(self):
        self.player1_score = 0
        self.player2_score = 0
        self.game_over_event = threading.Event()

    def start(self):
        screen = curses.initscr()
        num_rows, num_cols = screen.getmaxyx()
        screen.addstr(0, 55, "Duck hunt!🦆🔫")
        screen.addstr(10, 20, "A     Player 1     D")
        screen.addstr(10, 80, "J     Player 2     L")
        screen.addstr(6, 29, "W")
        screen.addstr(14, 29, "S")
        screen.addstr(6, 89, "I")
        screen.addstr(14, 89, "K")
        screen.addstr(3, 20, "Score: ")
        screen.addstr(3, 80, "Score: ")

        screen.refresh()

        thread1 = threading.Thread(target=self.play, args=(1, self.game_over_event, screen))
        thread2 = threading.Thread(target=self.play, args=(2, self.game_over_event, screen))
        thread1.start()
        thread2.start()

    def play(self, player_number, game_over_event, screen):
        score1 = 27
        score2 = 87
        while not game_over_event.is_set():
            if player_number == 1:
                key = generate_key1(screen)
            else:
                key = generate_key2(screen)
            while (True and (not game_over_event.is_set())):
                if getch() == keys[key]:
                    if player_number == 1:
                        self.player1_score += 1
                        screen.addstr(3, score1, "🍗")
                        score1 +=2
                        screen.addstr(coords[key][0], coords[key][1], (keys[key]).upper() + " ")
                        screen.refresh()
                        if self.player1_score == 5:
                            screen.clear()
                            game_over_event.set() 
                    else:
                        self.player2_score += 1
                        screen.addstr(3, score2, "🍗")
                        score2+=2
                        screen.addstr(coords[key][0], coords[key][1], (keys[key]).upper() + " ")   
                        screen.refresh()
                        if self.player2_score == 5:
                            screen.clear()
                            game_over_event.set() 
                    break
        if self.player1_score == 5:
            screen.addstr(15, 50, "🏆Player 1 won!🏆")
        else:
            screen.addstr(15, 50, "🏆Player 2 won!🏆")
        screen.refresh()
        curses.napms(6000)
        curses.endwin()
game = Game()
game.start()