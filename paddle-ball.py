from Tkinter import *
import time
import random

#Make sure to Play some Mujik!
#You can add water or spikes below as reference for game over
#You can put a image instead of a ball, make the face weid on hitting a wall
#--------
#Add some Asteroids on hitting them Increment the points not on hitting the paddle(But do it first)
#And Zombies, HeadShot!
#Make the ball a Fireball... A gif...

level = 3
ball_speed = level
paddle_speed = 1 + level

#Ball Class:
class Ball:

	def __init__(self, canvas, paddle, color):

		self.canvas = canvas
		self.paddle = paddle
		self.id = canvas.create_oval(10, 10, 25, 25, fill = color, outline = color)
		self.canvas.move(self.id, 245, 100)
		#Score:
		self.score = 0
		self.score_board = canvas.create_text(440, 40, text = self.score, fill = 'red', font = ('04b08', 20))
		#Random Starting speeds, aplllicable only the first time, abs(3) is the top speed
		starts = [-3, -2, -1, 1, 2, 3]
		random.shuffle(starts)
		self.x = starts[0]
		self.y = -level
		self.canvas_height = self.canvas.winfo_height()
		self.canvas_width = self.canvas.winfo_width()
		self.game_over = False

	def draw(self):

		self.canvas.move(self.id, self.x, self.y)
		pos = self.canvas.coords(self.id)
		paddle_pos = self.canvas.coords(self.paddle.id)
		#Setting the final speed for both X and Y as 1!
		if pos[1] <= 0:
			self.y = ball_speed
		if pos[3] >= self.canvas_height:
			self.y = -ball_speed
		if pos[0] <= 0:
			self.x = ball_speed
		if pos[2] >= self.canvas_width:
			self.x = -ball_speed
		#On hitting the paddle
		if self.hit_paddle(pos) == True:
			self.y = -ball_speed
			self.score = self.score + 1
			self.canvas.itemconfig(self.score_board, text = self.score)
		#Game Over...adding 10 just so it would go down farther 10px
		if pos[3] >= self.canvas_height:
			self.game_over = True
			self.canvas.create_text(245, 100, text='GAME OVER', font=('04b08', 30), fill='red')

	def hit_paddle(self, pos):
		
		paddle_pos = self.canvas.coords(self.paddle.id)
		if pos[2] >= paddle_pos[0] and pos[0]	<= paddle_pos[2]:
			if pos[3] >= paddle_pos[1] and pos[3]	<= paddle_pos[3]:
				return True
		return False


#Paddle Class
class Paddle:
		
	def __init__(self, canvas, color):

		self.canvas = canvas
		self.id = canvas.create_rectangle(0, 0, 100, 10, fill = color, outline = color)
		self.canvas_width = self.canvas.winfo_width()
		#Starting position for the paddle
		self.canvas.move(self.id, 200, 300)
		self.x = 0
		self.canvas.bind_all('<KeyPress-Right>', self.move_right)
		self.canvas.bind_all('<KeyPress-Left>', self.move_left)

#Just a Reminder that `move` function moves the item relative to the current position

	def draw(self):

		self.canvas.move(self.id, self.x, 0)
		pos = self.canvas.coords(self.id)
		collided_wall = (pos[0] <= 0) or (pos[2] >= self.canvas_width)
		
		#A clever collision detection!
		if collided_wall:
			self.x = 0

	def move_right(self, event):
			self.x = paddle_speed

	def move_left(self, event):
			self.x = -paddle_speed

#Getting ready with the Canvas

tk = Tk()
tk.title('Bounce')
tk.resizable(0, 0)
tk.wm_attributes('-topmost', 1)
canvas = Canvas(tk, width = 500, height = 400, bd = 0, highlightthickness = 0)
canvas.pack()
#Background Image:
bgImage = PhotoImage(file='/home/ropo/python/bg.gif')
canvas.create_image(0, 0, anchor=NW, image=bgImage)
#Essential for the game, Initializes the animation
tk.update()

paddle = Paddle(canvas, 'blue')
ball = Ball(canvas, paddle, 'orange')

#Main Loop: Redraw the screen, wait for 1/100 of a sec
while 1:
	if ball.game_over == False:
		ball.draw()
		paddle.draw()
	tk.update_idletasks()
	tk.update()
	time.sleep(0.01)


