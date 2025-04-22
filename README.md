terminal games 🎮

wasn’t too comfortable doing OOP in python. didn’t understand threading.
i understand it now. and do oop in python at work. cool.

simple games — you can run these right in your terminal and play knock-off tetris or snake.
no fancy graphics. no setup. just run the script and use wasd.

you can also configure the __init__ in both to customize gameplay.
make the games faster, slower, harder/easier to win.
give the snake more food. only give yourself zigzag pieces in tetris. fun.

⸻

🟩 tetris.py
	•	made my own shapes (defined by shifts from a center block)
	•	uses threading to update the game in the background while you move
	•	game board is a 2D array of strings (list of lists)
	•	checks collisions manually — no libraries or helpers
	•	pieces rotate. lines clear. game ends when new piece can’t fit
	•	press a to move left, d to move right, s to go down fast, w to rotate

you can tweak these if you want:

self.box_height = 25
self.box_width = 12
self.win_length = 22
self.current_shape = "I"



⸻

🐍 snake.py
	•	also terminal-based. also threaded
	•	uses same 2D grid approach — but with food and a growing snake
	•	default start length is 2. game ends on wall collision or self collision
	•	food is random. snake grows when it eats
	•	you can win if the snake gets long enough

you can change:

self.snake_length = 2        # starting size
self.food_amount = 10        # how much food on the screen
self.win_length = 1000       # what counts as winning

controls are the same:
w = up
a = left
s = down
d = right
(can’t reverse directions. that’s cheating.)

⸻

▶️ to play:

python3 tetris.py

or

python3 snake.py



⸻

both games use termios, tty, and select to get raw input without hitting enter.
works best on mac/linux. windows might need tweaks. don’t ask me what they are.

⸻
