#Jeff Divinere and Joe Render
#Ping Pong Python Project

import tkinter
from tkinter import Frame, BOTH, Canvas, messagebox, Menu, IntVar, StringVar
from PongClient import PongClient

class Pong(Frame):

    def __init__(self, parent):
        self.WIN_MESSAGE = 'YOU WIN!!! NIIICEEE'
        self.LOSS_MESSAGE = 'YOU LOST!!! HA HA'
    
        self.client = None #reference to PongClient for this Pong game
        self.disp_ui_msg_time = 0 #keeps track of how long the current ui message has been displayed for
        
        # DEFAULTS
        self.net_enabled = False
        self.net = None
        self.netX = 800 / 2
        self.netY = 400 / 2
        self.netDY = 1
        self.net_touch_count = 0
        self.net_height = 75
        self.net_size_increment = 20
        self.net_max_size = 250
        self.net_speed = 1
        self.player1 = None
        self.player2 = None
        self.canvas = None
        self.winHEIGHT = 0
        self.winWIDTH = 0
        self.paddleSpeed = 15
        self.player1Points = 0
        self.player2Points = 0
        self.textLabel = 0

        # CURRENT SETTINGS
        self.fullscreen = False
        self.net_enabled = True
        self.verbose = False
        self.paddle_size = 50
        self.game_length = 7

                 
                    
        # Default factors to 1
        self.ballSpeed = 1
        self.paddle_size_factor = 1
        self.ball_speed_factor = 1
        self.player_count = 1
        self.auto_player2 = False

        # Ball
        self.ball_serve_pos1 = (100, 200, 110, 210)
        self.ball_serve_pos2 = (700, 200, 710, 210)
        self.ballX_pos = 50  # Starting X pos of ball
        self.ballY_pos = 50  # Starting Y pos of ball
        self.ball = None
        self.ballDX = 2
        self.ballDY = -2

        # Paddle
        self.paddle1 = None
        self.paddle2 = None
        self.paddle1X_pos = 2
        self.paddle1Y_pos = 2
        self.paddle2X_pos = 0
        self.paddle2Y_pos = 2
        
        # Inheriting from tk 
        Frame.__init__(self, parent)
        self.parent = parent
        self.start_gui(fullscreen=False)
        # Set up radio buttons
        self.ball_speed_radio = IntVar()
        self.ball_speed_radio.set(1)
        self.paddle_size_radio = IntVar()
        self.paddle_size_radio.set(1)
        self.player_count_radio = IntVar()
        self.player_count_radio.set(1)
        self.game_length_radio = IntVar()
        self.game_length_radio.set(7)
        self.setup_displayed_user_message()
        parent.protocol("WM_DELETE_WINDOW", self.quit_pong) #define window closing logic

    '''Sets up support for displaying messages to the user'''
    def setup_displayed_user_message(self):
        self.curr_ui_msg_text = ''
        self.user_message = None
        self.user_message_text = StringVar()
        self.user_message_text.trace('w', self.update_displayed_user_message)
     
    '''Tracks when the user message variable has been written to'''  
    def update_displayed_user_message(self, *args):
        if self.curr_ui_msg_text is not self.user_message_text.get():
            self.curr_ui_msg_text = self.user_message_text.get()
            self.disp_ui_msg_time = 0
            self.canvas.delete(self.user_message)        
            self.user_message = self.canvas.create_text(self.winWIDTH / 2, self.winHEIGHT - 15,
                                                        text=self.user_message_text.get())

    '''Checks status of client and terminates if it exists'''
    def check_client_destroyed(self):
        if self.client:
            self.client.destroy()
            self.client = None
            
    '''Destroys the active client and resets the game'''
    def terminate_multiplayer(self):
        if self.client:
            self.client.destroy()
        self.client = None
        self.player_count_radio.set(1)
        self.reset_score()

    '''Defines execution of logic on window close''' 
    def quit_pong(self):
        self.check_client_destroyed()
        self.parent.quit()

    def game_over(self, disp_msg):
        self.canvas.delete(self.textLabel)
        self.textLabel = self.canvas.create_text(self.winWIDTH / 2, 10, fill="RED", text="GAME OVER")
        messagebox.showinfo(title="Game Over", message=disp_msg + "\nCome back soon!")
        self.quit_pong()

    def on_keypress(self, event):
        global player1, player2

        # Paddle 1 keyboard Controls
        if event.char == 'w':
            if self.canvas.coords(self.paddle1)[1] >= 0:
                self.canvas.move(self.paddle1, 0, -self.paddleSpeed)
        if event.char == 's':
            if self.canvas.coords(self.paddle1)[3] <= self.winHEIGHT:
                self.canvas.move(self.paddle1, 0, self.paddleSpeed)

        # Paddle 2 keyboard Controls
        if event.char == 'p':
            if self.canvas.coords(self.paddle2)[1] >= 0:
                self.canvas.move(self.paddle2, 0, -self.paddleSpeed)
        if event.char == 'l':
            if self.canvas.coords(self.paddle2)[3] <= self.winHEIGHT:
                self.canvas.move(self.paddle2, 0, self.paddleSpeed)

        # Quit Game
        if event.char == 'q':
            self.quit_pong()

    def start_gui(self, fullscreen):
        if fullscreen:
            self.winHEIGHT = self.parent.winfo_screenheight()
            self.winWIDTH = self.parent.winfo_screenwidth()
        else:
            self.winHEIGHT = 400
            self.winWIDTH = 800

        self.paddle2X_pos = self.winWIDTH - 15
        self.netX = self.winHEIGHT - 15
        self.parent.title("Jeff and Joe's Ping Pong Game")
        self.pack(fill=BOTH, expand=1)
        self.canvas = Canvas(self, bg="white")
        self.canvas.pack(fill=BOTH, expand=1)

        # Create Ball and save ref
        self.ball = self.canvas.create_oval(0 + self.ballX_pos,
                                            0 + self.ballY_pos,
                                            10 + self.ballX_pos,
                                            10 + self.ballY_pos,
                                            outline="black",
                                            fill="black", width=1)
        # Create Paddle 1 and save ref
        self.paddle1 = self.canvas.create_rectangle(0 + self.paddle1X_pos,
                                                    0 + self.paddle1Y_pos,
                                                    10 + self.paddle1X_pos,
                                                    self.paddle_size + self.paddle1Y_pos,
                                                    outline="red",
                                                    fill="blue")
        # Create Paddle 2 and save ref
        self.paddle2 = self.canvas.create_rectangle(0 + self.paddle2X_pos,
                                                    0 + self.paddle2Y_pos,
                                                    10 + self.paddle2X_pos,
                                                    self.paddle_size + self.paddle2Y_pos,
                                                    outline="red",
                                                    fill="blue")
        # Create Net object and save ref (moves on Y axis only)
        self.net = self.canvas.create_rectangle(0 + self.netX,
                                                0 + self.netY,
                                                10 + self.netX,
                                                self.net_height + self.netY,
                                                outline="black",
                                                fill="black")
        # Create Scoreboard and save ref
        self.textLabel = self.canvas.create_text(self.winWIDTH / 2, 10,
                                                 text=str(self.player1Points) + " | " + str(self.player2Points))
        # Link key press event to on_keypress() callback method
        self.parent.bind("<Key>", self.on_keypress)
        self.canvas.pack(fill=BOTH, expand=1)
        # Set timer
        self.after(200, self.play)

    def check_ball_impact(self, game_ball, screen_object):
        """
        Check for bounding box overlap indicating canvas object collision by comparing 2 lists of len() = 4
        - Caller expects truthy after collision
        - Caller expects falsey if not collision

        :param game_ball: (x1, y1, x2, y2) describing the bounding box of the object.
        :param screen_object: (x1, y1, x2, y2) describing the bounding box of the object.
        :return:
        """
        ball_height = game_ball[3] - game_ball[1]  # y2 - y1 on game_ball
        ball_width = game_ball[2] - game_ball[0]  # x2 - x1 on game_ball
        paddle_height = screen_object[3] - screen_object[1]  # y2 - y1 on screen_object
        paddle_width = screen_object[2] - screen_object[0]  # x2 - x1 on screen_object
        impact = True  # assume impact truthy to start
        impact = not (game_ball[0] + ball_width < screen_object[
            0] or  # Check x-axis collision right edge game_ball touching left edge screen_object
                      game_ball[1] + ball_height < screen_object[
                          1] or  # Check y-axis collision screen_object upper left corner is above upper left corner game_ball plus coord1 height
                      game_ball[0] > screen_object[
                          0] + paddle_width or  # Check x-axis collision left edge game_ball not touching right edge screen_object
                      game_ball[1] > screen_object[
                          1] + paddle_height)  # Check y-axis collision game_ball upper left corner is above upper left corner screen_object plus coord2 height
        return impact

    def chase_ball(self, target):
        ball_pos = self.canvas.coords(self.ball)
        target_pos = self.canvas.coords(target)
        # Find midpoint of target
        target_mid = (target_pos[3] - target_pos[1]) / 2
        # Line up center of target with ball
        self.canvas.coords(target,
                           target_pos[0],
                           ball_pos[3] - target_mid,
                           target_pos[2],
                           ball_pos[3] + target_mid)
        # return info about what we did to caller for boolean or more nuanced comparison
        return target, target_pos[0], tuple([ball_pos[3] - target_mid, target_pos[2], ball_pos[3] + target_mid])
                    
    '''Resets game score'''
    def reset_score(self):
        self.player1Points = 0
        self.player2Points = 0
        self.canvas.coords(self.ball, self.ball_serve_pos1)
        self.update_score()

    def update_score(self):         
        # Update Scoreboard
        self.canvas.delete(self.textLabel)
        self.textLabel = self.canvas.create_text(self.winWIDTH / 2, 10, 
            text=str(self.player1Points) + " | " + str(self.player2Points))
        
        # Check for game over
        if self.player1Points >= self.game_length:
            if self.client:                   
                self.client.communicate_with_server('W') #tells the server that this client won  
            self.game_over(self.WIN_MESSAGE)
            
        # If player 2 won game over
        if self.player2Points >= self.game_length:
            if self.client:                   
                self.client.communicate_with_server('L') #tells the server that this client lost
            self.game_over(self.LOSS_MESSAGE)

    def is_auto(self):
        return not self.auto_player2 and self.client

    def play(self):
        # Move the ball
        self.canvas.move(self.ball, self.ballDX * self.ball_speed_factor, self.ballDY * self.ball_speed_factor)

        # Move the net with relative motion
        if self.net_enabled:
            self.canvas.move(self.net, 0, self.netDY * self.net_speed)

        # Automated Paddle Movement Logic (Computer)
        if not self.is_auto():
            self.chase_ball(self.paddle2)

        # Manage ball

        # TOP CHECK
        # Check ball Y1 upper left edge of bounding box to Bounce ball off top of window
        ball_loc = self.canvas.coords(self.ball)
        if ball_loc[1] <= 0:  # check Y1 not negative
            self.ballDY = -self.ballDY  # Reverse Ball Direction on y-axis

        # BOTTOM CHECK
        # Check ball Y2 lower right edge of bounding box to Bounce ball off of window bottom
        if ball_loc[3] >= self.winHEIGHT:
            self.ballDY = -self.ballDY  # Reverse Ball Direction on y-axis

        ### Manage Net ###

        # TOP CHECK
        # Check net Y1 upper left edge of bounding box to Bounce net off bottom of window
        net_loc = self.canvas.coords(self.net)
        if net_loc[1] <= 0:
            net_loc[1] = 0
            self.netDY = -self.netDY  # Reverse Ball Direction on y-axis

        # BOTTOM CHECK
        #  Check net Y2 lower right edge of bounding box to bounce net off of window bottom
        if net_loc[3] >= self.winHEIGHT:
            net_loc[3] = self.winHEIGHT
            self.netDY = -self.netDY  # Reverse Ball Direction on y-axis

        self.canvas.coords(self.net, tuple(net_loc))  # redraw net

        ### Manage Defense ###

        # Did player 1 return volley ?
        if self.check_ball_impact(self.canvas.coords(self.ball), self.canvas.coords(self.paddle1)):
            self.ballDX = -self.ballDX
            if self.verbose:
                print("play: Player1 returns shot")

        # Did player 2 return volley ?
        if self.check_ball_impact(self.canvas.coords(self.ball), self.canvas.coords(self.paddle2)):
            self.ballDX = -self.ballDX
            if self.verbose:
                print("play: Player2 returns shot")

        ### Manage Scoring ###

        # Player 1 Scored because ball passed right window edge
        if self.canvas.coords(self.ball)[2] >= self.winWIDTH:
            # Bounce
            self.ballDX = -self.ballDX
            self.player1Points += 1  # PLayer 1 Scored
            self.user_message_text.set("SCORE!: Player 1 scored : {} points".format(self.player1Points))
            # Reset moving net object after score
            if self.net_enabled:
                # get in serve position
                if self.verbose:
                    print("play: setup player 1 serve")
                self.canvas.coords(self.ball, self.ball_serve_pos1)
                self.ballDX = -self.ballDX
                self.reset_net()

            self.update_score()

        # Player 2 Scored because ball passed left window edge
        if self.canvas.coords(self.ball)[0] <= 0:
            # Bounce
            self.ballDX = -self.ballDX
            self.player2Points += 1
            self.user_message_text.set("SCORE!: Player 2 scored : {} points".format(self.player2Points))
            # Reset moving net object after score
            if self.net_enabled:
                # get in serve position
                if self.verbose:
                    print("play: setup player 2 serve")
                self.canvas.coords(self.ball, self.ball_serve_pos2)
                self.ballDX = -self.ballDX
                self.reset_net()

            # Update Scoreboard
            self.canvas.delete(self.textLabel)
            self.textLabel = self.canvas.create_text(self.winWIDTH / 2, 10,
                                                     text=str(self.player1Points) + " | " + str(self.player2Points))
        if self.net_enabled:
            self.check_for_net_contact()
            
        if self.is_auto():
            self.client.update_multiplayer_game_objects()
        
        #remove ui message if displayed longer than ~5 seconds
        if self.disp_ui_msg_time > 500 and self.user_message_text.get():
            self.disp_ui_msg_time = 0
            self.user_message_text.set('')
        else:
            self.disp_ui_msg_time += 1
            
        # Set timer
        self.after(10, self.play)

    def check_for_net_contact(self):
        impact = False
        # Did ball hit net ?
        if self.check_ball_impact(self.canvas.coords(self.ball), self.canvas.coords(self.net)):
            impact = True
            # vertical Bounce using the net's  bounce
            self.netDY = -self.netDY

            # Horizontal Ball reflection after touching net
            self.ballDX = -self.ballDX

            # count ball touches
            self.net_touch_count += 1

            # speed up net
            self.net_speed *= 1.05

            # Net grows when ball hits it, resets size and position after a point scored
            self.inflate_net()

            # Manage bobble with net triggered by a double touch
            if self.net_touch_count > 0:
                self.net_touch_count = 0
                # Anti-bobble shift
                self.canvas.move(self.ball, 10, 0)  # Move ball 10 pixels right
                return impact
        else:
            return impact

    def reset_net(self):
        # Reset moving net object after score or overexpansion
        self.net_height = 75  # Reset net to original size after point scored
        self.net_speed = 1  # Reset net to original speed after point scored

        self.canvas.coords(self.net,
                           0 + self.netX,
                           0 + self.netY,
                           10 + self.netX,
                           self.net_height + self.netY)

    def expand_rectangle(self, offset):
        old_net_loc = net_loc = self.canvas.coords(self.net)
        if self.verbose:
            print("expand_rectangle: Original net dimensions: {}".format(old_net_loc))
        if net_loc[1] <= 0:
            net_loc[1] = 0
        if net_loc[3] > 400:
            net_loc[3] = 399

        # Add half of offset to top with minus
        net_loc[1] -= (offset // 2)
        # Add half of offset to bottom with plus
        net_loc[3] += (offset // 2)
        self.canvas.coords(self.net, tuple(net_loc))
        self.net_height = abs(net_loc[3] - net_loc[1])

        new_net_loc = net_loc
        if self.verbose:
            print("expand_rectangle: Inflated net dimensions: {}".format(new_net_loc))
        return True

    def inflate_net(self):
        # Get current position of net object
        net_loc = self.canvas.coords(self.net)

        # FIX BAD Y VALUES
        if net_loc[1] < 0:
            net_loc[1] = 0
        if net_loc[3] >= self.winHEIGHT:
            net_loc[3] = self.winHEIGHT - 1

        # Expand rect only if there is room at top or bottom
        if net_loc[3] < self.winHEIGHT - self.net_size_increment or net_loc[1] < self.net_size_increment:
            self.expand_rectangle(self.net_size_increment)

        # trim when self.net_height > self.net_max_size
        loc = self.canvas.coords(self.net)

        # sanity check actual net_size
        rect_height = abs(loc[3] - loc[1])

        if rect_height > self.net_max_size:
            self.net_height = self.net_max_size
            self.reset_net()
        else:
            # correct object by asking canvas
            self.net_height = rect_height
        if self.verbose:
            print("inflate_net: net_height as: {}".format(int(self.net_height)))
            print("inflate_net: computed net_height from coords as: {}".format(int(rect_height)))
            print("inflate_net: maximum net_height : {}".format(int(self.net_max_size)))
        return

    def change_paddle_size(self):
        self.paddle_size_factor = self.paddle_size_radio.get()
        self.user_message_text.set("Paddle Size is now: {} pixels".format(self.paddle_size_factor * self.paddle_size))
        paddle1_loc = self.canvas.coords(self.paddle1)
        self.canvas.coords(self.paddle1,
                           paddle1_loc[0],
                           paddle1_loc[1],
                           paddle1_loc[2],
                           (self.paddle_size * self.paddle_size_factor) + paddle1_loc[1])
        paddle2_loc = self.canvas.coords(self.paddle2)
        self.canvas.coords(self.paddle2,
                           paddle2_loc[0],
                           paddle2_loc[1],
                           paddle2_loc[2],
                           (self.paddle_size * self.paddle_size_factor) + paddle2_loc[1])  # Grow paddle

    def change_ball_speed(self):
        self.ball_speed_factor = self.ball_speed_radio.get()
        self.user_message_text.set("Ball speed is now: {}X".format(self.ball_speed_factor))

    def change_game_length(self):
        self.game_length = self.game_length_radio.get()
        self.user_message_text.set("Game length is now: {} points".format(self.game_length))

    def change_player_count(self):
        self.player_count = self.player_count_radio.get()
        self.user_message_text.set("Number of human players is now: {}".format(self.player_count))
        if self.player_count < 2:
            self.auto_player2 = True
            self.check_client_destroyed()
        else:
            if not self.client:                
                self.client = PongClient(self)
            self.auto_player2 = False

    def build_menus(self, menu_bar, gameref):
        player_menu = Menu(menu_bar, tearoff=0)
        ballspeed_menu = Menu(menu_bar, tearoff=0)
        paddlesize_menu = Menu(menu_bar, tearoff=0)
        gamelength_menu = Menu(menu_bar, tearoff=0)

        player_menu.add_radiobutton(label='Man Vs. Computer', variable=self.player_count_radio, value=1,
                                    command=gameref.change_player_count)
        player_menu.add_radiobutton(label='1 vs 1', variable=self.player_count_radio, value=2,
                                    command=gameref.change_player_count)
        player_menu.add_command(label="Quit", command=self.quit_pong)

        paddlesize_menu.add_radiobutton(label='Small', variable=self.paddle_size_radio, value=1,
                                        command=gameref.change_paddle_size)
        paddlesize_menu.add_radiobutton(label='Medium', variable=self.paddle_size_radio, value=2,
                                        command=gameref.change_paddle_size)
        paddlesize_menu.add_radiobutton(label='Large', variable=self.paddle_size_radio, value=3,
                                        command=gameref.change_paddle_size)

        ballspeed_menu.add_radiobutton(label='1x', variable=self.ball_speed_radio, value=1,
                                       command=gameref.change_ball_speed)
        ballspeed_menu.add_radiobutton(label='2x', variable=self.ball_speed_radio, value=2,
                                       command=gameref.change_ball_speed)
        ballspeed_menu.add_radiobutton(label='3x', variable=self.ball_speed_radio, value=3,
                                       command=gameref.change_ball_speed)

        gamelength_menu.add_radiobutton(label='7 Point Game', variable=self.game_length_radio, value=7,
                                        command=gameref.change_game_length)
        gamelength_menu.add_radiobutton(label='15 Point Game', variable=self.game_length_radio, value=15,
                                        command=gameref.change_game_length)
        gamelength_menu.add_radiobutton(label='21 Point Game', variable=self.game_length_radio, value=21,
                                        command=gameref.change_game_length)

        menu_bar.add_cascade(label="Players", menu=player_menu)
        menu_bar.add_cascade(label="Game Length", menu=gamelength_menu)
        menu_bar.add_cascade(label="Paddle Size", menu=paddlesize_menu)
        menu_bar.add_cascade(label="Ball Speed", menu=ballspeed_menu)


def main():
    root = tkinter.Tk()
    gameref = Pong(root)
    root.geometry("800x400+300+200")
    
    # Setup Menu
    menu_bar = Menu(root)
    gameref.build_menus(menu_bar, gameref)
    root.config(menu=menu_bar)

    root.mainloop()


if __name__ == '__main__':
    main()
