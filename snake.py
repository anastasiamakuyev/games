import threading
import time
import sys
import termios
import tty
import select
import os
import random

class Snake:
    def __init__(self): #mess with these if you wanna start with a long snake, or make the game easier/harder
        self.snake_length = 2
        self.food_amount = 10
        self.food_coors = []
        self.direction = 'd'
        self.coors = [(5,5), (5,4)]  # head, tail
        self.box_height = 25
        self.box_width = 45
        self.box = self.create_box()
        self.winning = False
        self.losing = False
        self.win_length = 1000

    def game_over(self):
        if self.winning or self.losing:
            return True

    def make_one_food(self):
        down = random.uniform(1, self.box_height - 2)
        right = random.uniform(1, self.box_width - 2)
        food_coor = (round(down), round(right))
        return food_coor

    def maintain_all_food(self):
        while len(self.food_coors) < self.food_amount:
            next_food = self.make_one_food()
            i, j = next_food
            if self.box[i][j] != 'O' and next_food not in self.food_coors:
                self.food_coors.append(next_food)

    def change_direction(self, new_direction):
        if new_direction:
            transitions_not_allowed1 = ['w', 's']
            transitions_not_allowed2 = ['a', 'd']
            # only allow a change that is perpendicular to the current direction. no about-face
            if (self.direction in transitions_not_allowed1 and new_direction in transitions_not_allowed2) or \
               (self.direction in transitions_not_allowed2 and new_direction in transitions_not_allowed1):
                self.direction = new_direction

    def create_box(self):
        top = [['X' for g in range(self.box_width)]]
        middle = [['X'] + [' ' for i in range(self.box_width - 2)] + ['X'] for j in range(self.box_height - 2)]
        self.box = top + middle + top
        for i, j in self.coors:
            self.box[i][j] = "O"
        self.maintain_all_food()
        for i, j in self.food_coors:
            self.box[i][j] = "*"
        return self.box

    def move_snake(self):
        dirs = {'w': (-1, 0), 'a': (0, -1), 's': (1, 0), 'd': (0, 1)}
        head = self.coors[0]
        movement = dirs[self.direction]
        new_head = (movement[0] + head[0], movement[1] + head[1])
        i, j = new_head
        # check boundaries and self-collision.
        if i < 1 or i > self.box_height - 2 or j < 1 or j > self.box_width - 2 or self.box[i][j] == 'O':
            self.losing = True
        if self.snake_length >= self.win_length:
            self.winning = True
        if new_head not in self.food_coors:
            self.coors.pop()  # remove tail if not eating food. since we're always adding the head.
        else:
            self.food_coors.remove(new_head)
            self.snake_length += 1
        self.coors.insert(0, new_head)

    def get_box(self):
        printMe = ""
        for i in range(len(self.box)):
            row = self.box[i]
            for j in range(len(row)):
                printMe += (row[j])
            printMe += ("\n")
        return printMe

    def play(self):
        if not self.game_over():
            self.maintain_all_food()
            # rebuild the box with the current snake and food positions.
            self.create_box()
            self.move_snake()
            return self.get_box()
        else:
            if self.winning:
                return "You won! Your snake reached a length of " + str(self.win_length)
            else:
                return "Game over. You lose."
            


            

def get_key(timeout=0.1):
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setcbreak(fd)
        r, _, _ = select.select([sys.stdin], [], [], timeout)
        if r:
            return sys.stdin.read(1).lower()
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return None

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def periodic_output(snake):
    while not snake.game_over():
        time.sleep(0.05)
        clear_screen()
        # print current state of game.
        print(snake.play())

    clear_screen()
    print(snake.play())

def run_game():
    snake = Snake()  # create new Snake instance for each game.
    # start background thread for periodic output.
    thread = threading.Thread(target=periodic_output, args=(snake,), daemon=True)
    thread.start()

    # main loop keeps capturing WASD keystrokes until the game is over.
    while not snake.game_over():
        key = get_key()
        if key and key in ['w', 'a', 's', 'd']:
            snake.change_direction(key)
        # tiny nap to prevent busy loop.
        time.sleep(0.0001)
    # bigger nap. 
    time.sleep(1)

def main():
    while True:
        ready = input("Are you ready to play Snake? (y/n): ").strip().lower()
        if ready == 'y':
            run_game()
            # after game end, ask if u wanna play again
            again = input("Play again? (y/n): ").strip().lower()
            if again != 'y':
                print("Goodbye!")
                break
        elif ready == 'n':
            print("Goodbye!")
            break
        else:
            print("Please enter 'y' or 'n'.")

if __name__ == '__main__':
    main()