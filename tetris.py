import threading
import time
import sys
import termios
import tty
import select
import os
import random

class Tetris:
    def __init__(self): #feel free to mess with these if u want a bigger/smaller tetris board, or you hate a certain squiggly shape
        self.current_shape_coors = []
        self.filled_coors = []
        self.box_height = 25
        self.box_width = 12
        self.box = self.create_box()
        self.winning = False
        self.losing = False
        self.win_length = 22
        self.center_coors = (2, 6)
        self.current_shape = "I"

        self.shapes = {"I": [(2, 0), (1,0), (0,0), (-1, 0)], 
                       "J": [(-1, -1), (-1,0), (-1,1), (0,1)],  
                       "L": [(0, -1), (0,0), (0,1), (-1,1)], 
                       "O": [(0, 1), (-1,0), (-1,1), (0,0)], 
                       "S": [(-1, 0), (0,0), (0,1), (1, 1)], 
                       "Z": [(-1, 1), (0,0), (0,1), (1, 0)], 
                       "T": [(-1,0), (0, 0), (-1, -1), (-1, 1)]}
        
        self.current_shift = self.shapes[self.current_shape]

    def game_over(self):
        if self.winning or self.losing:
            return True
        

    #if you CAN move, move. if you cant move, say so, and we'll put a new shape. 
    #if you cant put a new shape, you lose.

    def try_move(self, tentative_new_center = None, tentative_new_shift= None):
        center = tentative_new_center if tentative_new_center else self.center_coors
        shift = tentative_new_shift if tentative_new_shift else self.shapes[self.current_shape]
        #get the tentative new coordinates
        tentative_new_coors = []
        g,h = center
        for i,j in shift:
            new_coor = (i+g, h+j)
            tentative_new_coors.append(new_coor)
        for move in tentative_new_coors:
            if move in self.filled_coors: #if there is already a shape there
                return False
            a,b = move
            if a>self.box_height-2 or b>self.box_width-2 or b<1:
                return False
        #update center, current shift.
        self.center_coors = center
        self.current_shift = shift
        self.current_shape_coors = tentative_new_coors
        return True

    def rotate_shape(self):
        #keep center the same. move all the "shifts around the center" math, muthafuckaaaaaaa
        new_shifts = []
        for i,j in self.current_shift:
            next_shift = (-j, i)
            new_shifts.append(next_shift)
        old_center = self.center_coors
        return self.try_move(old_center, new_shifts)
    
    def slide(self, direction = None): #can slide left, right, or down
        dirs = {'a':(0,-1), 'd':(0,1), 's':(1, 0)}
        dir = direction if direction else 's'
        movement = dirs[dir]
        i,j = self.center_coors
        g,h = movement
        new_center = (i+g, j+h)
        return self.try_move(new_center,self.current_shift)
    
    def slide_down(self):
        if not self.slide('s'):
            self.next_shape()
            return False
        return True
    
    def user_move(self, key):
        if key == 's':
            downwards = True
            while downwards:
                downwards = self.slide_down()
        elif key == 'w':
            self.rotate_shape()
        else:
            self.slide(key)

    def create_box(self):
        #make the box
        top = [['X' for g in range(self.box_width)]]
        middle = [['X'] + [' ' for i in range(self.box_width - 2)] + ['X'] for j in range(self.box_height - 2)]
        self.box = top + middle + top

        #fill in current shape
        for i,j in self.current_shape_coors:
            self.box[i][j] = "□"
    
        #fill in existing shapes
        for i,j in self.filled_coors:
            self.box[i][j] = "□"
        return self.box

    def get_box(self):
        printMe = ""
        for i in range(len(self.box)):
            row = self.box[i]
            oneLine = "|"
            for j in range(len(row)):
                oneLine += (row[j]) + "|"
            printMe += oneLine + ("\n")
        return printMe
    
    def next_shape(self):
        #save the current shape to be permanent
        self.clear_rows()
        self.filled_coors = self.filled_coors + self.current_shape_coors

        #reassign which shape randomly
        myList = list(self.shapes.keys())
        numOptions = len(myList)
        pickOne = round(random.uniform(0,numOptions-1))
        theShape = myList[pickOne]
        self.current_shape = theShape

        self.current_shift= self.shapes[self.current_shape]

        #reset center coordinate
        self.center_coors = (2, 6)

        if not self.try_move():
            self.losing = True

    def clear_rows(self):
        for i in (range(len(self.box))):
            self.create_box()
            row = self.box[i]
            row_full = True if row.count('□') == (self.box_width-2) else False
            if row_full:
                #print("crying shitting screaming")
                # Filter filled_coors first:
                new_filled_coors = []
                for each in self.filled_coors:
                    rowFilled = each[0]
                    if rowFilled < i:
                        h,k = each
                        new_filled_coors.append((h+1,k))
                    elif rowFilled >i:
                        h,k = each
                        new_filled_coors.append((h,k))
                self.filled_coors = new_filled_coors

                # then filter current_shape_coors:
                new_shape_coors = []
                for each in self.current_shape_coors:
                    rowUnFilled = each[0]
                    if rowUnFilled < i:
                        a,b = each
                        new_shape_coors.append((a+1, b))  

                    elif rowUnFilled < i:
                        a,b = each
                        new_shape_coors.append((a, b)) 
                self.current_shape_coors = new_shape_coors
                #print(self.box.pop(i))
                #self.box.insert(1, (['X'] + [' ' for i in range(self.box_width - 2)] + ['X']))


    def play(self):
        if not self.game_over():
            self.slide_down()
            self.create_box()
            return self.get_box()
        else:
            if self.winning:
                return "You won! "
            else:
                return "Game over. You lose."
            




#---------------------------------------------------------------------------------------------------------------
            

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

def periodic_output(tetris):
    while not tetris.game_over():
        time.sleep(.7)
        clear_screen()
        # print current state of game.
        print(tetris.play())
    clear_screen()
    print(tetris.play())

def run_game():
    tetris = Tetris()  # create new Snake instance for each game.
    # start background thread for periodic output.
    thread = threading.Thread(target=periodic_output, args=(tetris,), daemon=True)
    thread.start()

    # main loop keeps capturing WASD keystrokes until the game is over.
    while not tetris.game_over():
        key = get_key()
        if key and key in ['w', 'a', 's', 'd']:
            tetris.user_move(key)
        # tiny nap to prevent busy loop.
        time.sleep(0.0001)
    # bigger nap. honk shoo honk shoo.
    time.sleep(.8)

def main():
    while True:

        ready = input("Are you ready to play Tetris? (y/n): ").strip().lower()
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