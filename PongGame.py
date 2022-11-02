#
# Simple Pong Game based upon PyGame
# My Pong Game, simplify Pong to play with Direct Ball, Pass Paddle and Ball as direct Features into DQN
#
# Yellow Left Hand Paddle is the DQN Agent Game Play
# A Red Ball return meant the Player missed the last Ball
# A Blue Ball return meant a successful return
#
#  Based upon Siraj Raval's inspiring Machine Learning vidoes
#  This is based upon Sirajs  Pong Game code
#  https://github.com/llSourcell/pong_neural_network_live
#
# Note needs imporved frame rate de sensitivition so as to ensure DQN perfomance across all computer types
# Currently Delta Time RATE fixed on each componet update to 7.5 !  => May ned to adjust increase/reduce depending upon perfomance
# ============================================================================================
import pygame
import random

# frame rate per second
FPS = 60  # Experiment Performance Seems rather sensitive to Computer performance (As Ball as rate vs Paddle rate sensitivity)

# size of our window
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400

# size of our paddle
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 60
# distance from the edge of the window
PADDLE_BUFFER = 15

# size of our ball
BALL_WIDTH = 10
BALL_HEIGHT = 10

# speeds of our paddle and ball
PADDLE_SPEED = 3
BALL_X_SPEED = 3
BALL_Y_SPEED = 2

# RGB colors for our paddle and ball
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
# initialize our screen using width and height vars
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


# ===============================================================
# Paddle 1 is our learning agent/us
# paddle 2 is the oponent  AI

# draw our ball
def drawBall(ballXPos, ballYPos, BallCol):
    # small rectangle, create it
    ball = pygame.Rect(ballXPos, ballYPos, BALL_WIDTH, BALL_HEIGHT)
    # draw it
    pygame.draw.rect(screen, BallCol, ball)


def drawPaddle1(paddle1YPos):
    # create it
    paddle1 = pygame.Rect(PADDLE_BUFFER, paddle1YPos, PADDLE_WIDTH, PADDLE_HEIGHT)
    # draw it
    pygame.draw.rect(screen, YELLOW, paddle1)


def drawPaddle2(paddle2YPos):
    # create it, opposite side
    paddle2 = pygame.Rect(WINDOW_WIDTH - PADDLE_BUFFER - PADDLE_WIDTH, paddle2YPos, PADDLE_WIDTH, PADDLE_HEIGHT)
    # draw it
    pygame.draw.rect(screen, WHITE, paddle2)


# update the ball, using the paddle posistions the balls positions and the balls directions
def updateBall(paddle1YPos, paddle2YPos, ballXPos, ballYPos, ballXDirection, ballYDirection, dft, BallColour):
    dft = 7.5
    # update the x and y position
    ballXPos = ballXPos + ballXDirection * BALL_X_SPEED * dft
    ballYPos = ballYPos + ballYDirection * BALL_Y_SPEED * dft
    Missed = False
    NewBallColor = BallColour;
    # checks for a collision, if the ball hits the Gamer Player side, our Learning agent
    if (
            ballXPos <= PADDLE_BUFFER + PADDLE_WIDTH and ballYPos + BALL_HEIGHT >= paddle1YPos and ballYPos - BALL_HEIGHT <= paddle1YPos + PADDLE_HEIGHT and ballXDirection == -1):
        # switches directions
        ballXDirection = 1
        #  Player returned the Ball Make the Objective Score (Reward) whenever Returns the Ball  aka playing Serena
        NewBallColor = BLUE
    # Check if Ball past Player
    elif (ballXPos <= 0):
        # negative score
        ballXDirection = 1
        # Player Missed the Ball, so negative Score Reward
        Missed = True
        NewBallColor = RED
        return [Missed, ballXPos, ballYPos, ballXDirection, ballYDirection, NewBallColor]

    # check if hits the AI Player
    if (
            ballXPos >= WINDOW_WIDTH - PADDLE_WIDTH - PADDLE_BUFFER and ballYPos + BALL_HEIGHT >= paddle2YPos and ballYPos - BALL_HEIGHT <= paddle2YPos + PADDLE_HEIGHT):
        # switch directions
        ballXDirection = -1
        NewBallColor = WHITE
    # past it
    elif (ballXPos >= WINDOW_WIDTH - BALL_WIDTH):
        # positive score
        ballXDirection = -1
        NewBallColor = WHITE
        return [Missed, ballXPos, ballYPos, ballXDirection, ballYDirection, NewBallColor]

    # if it hits the top move down
    if (ballYPos <= 0):
        ballYPos = 0;
        ballYDirection = 1;
    # if it hits the bottom, move up
    elif (ballYPos >= WINDOW_HEIGHT - BALL_HEIGHT):
        ballYPos = WINDOW_HEIGHT - BALL_HEIGHT
        ballYDirection = -1
    return [Missed, ballXPos, ballYPos, ballXDirection, ballYDirection, NewBallColor]


# ========================================================
# update the paddle position
def updatePaddle1(action, paddle1YPos, dft):
    # Assume Action is String:  'S':stay, 'U':Up, 'D':Down
    # if move up
    dft = 7.5
    if (action == 'U'):
        paddle1YPos = paddle1YPos - PADDLE_SPEED * dft
    # if move down
    if (action == 'D'):
        paddle1YPos = paddle1YPos + PADDLE_SPEED * dft

    # don't let it move off the screen
    if (paddle1YPos < 0):
        paddle1YPos = 0
    if (paddle1YPos > WINDOW_HEIGHT - PADDLE_HEIGHT):
        paddle1YPos = WINDOW_HEIGHT - PADDLE_HEIGHT
    return paddle1YPos


# =================================================================
def updatePaddle2(paddle2YPos, ballYPos, dft):
    dft = 7.5
    # move down if ball lower than Opponent Paddle
    if (paddle2YPos + PADDLE_HEIGHT / 2 < ballYPos + BALL_HEIGHT / 2):
        paddle2YPos = paddle2YPos + PADDLE_SPEED * dft
    # move up if ball is higher thn Openient Paddle
    if (paddle2YPos + PADDLE_HEIGHT / 2 > ballYPos + BALL_HEIGHT / 2):
        paddle2YPos = paddle2YPos - PADDLE_SPEED * dft
    # don't let it hit top
    if (paddle2YPos < 0):
        paddle2YPos = 0
    # dont let it hit bottom
    if (paddle2YPos > WINDOW_HEIGHT - PADDLE_HEIGHT):
        paddle2YPos = WINDOW_HEIGHT - PADDLE_HEIGHT
    return paddle2YPos


# =========================================================================
#  Main Pong Game class
class PongGame:
    def __init__(self):

        # Initialise pygame
        pygame.init()
        pygame.display.set_caption('Pong DQN Experiment')
        # random number for initial direction of ball
        num = random.randint(0, 9)

        # initialie positions of paddle
        self.paddle1YPos = WINDOW_HEIGHT / 2 - PADDLE_HEIGHT / 2
        self.paddle2YPos = WINDOW_HEIGHT / 2 - PADDLE_HEIGHT / 2
        # and ball direction
        self.ballXDirection = 1
        self.ballYDirection = 1
        # starting point
        self.ballXPos = WINDOW_WIDTH / 2 - BALL_WIDTH / 2

        self.clock = pygame.time.Clock()
        self.BallColor = WHITE
        self.FrameCount = 0
        self.GScore = -10.0
        self.GEpsilonDisplay = 1.0

        self.font = pygame.font.SysFont("calibri", 20)
        # randomly decide where the ball will move
        if (0 < num < 3):
            self.ballXDirection = 1
            self.ballYDirection = 1
        if (3 <= num < 5):
            self.ballXDirection = -1
            self.ballYDirection = 1
        if (5 <= num < 8):
            self.ballXDirection = 1
            self.ballYDirection = -1
        if (8 <= num < 10):
            self.ballXDirection = -1
            self.ballYDirection = -1
        # new random number
        num = random.randint(0, 9)
        # where it will start, y part
        self.ballYPos = num * (WINDOW_HEIGHT - BALL_HEIGHT) / 9

    # =========================================================================
    # Initialise Game
    def InitialDisplay(self):
        # for each frame, calls the event queue, like if the main window needs to be repainted
        pygame.event.pump()
        # make the background black
        screen.fill(BLACK)
        # draw our paddles
        drawPaddle1(self.paddle1YPos)
        drawPaddle2(self.paddle2YPos)
        # draw our ball
        drawBall(self.ballXPos, self.ballYPos, WHITE)
        #
        # updates the window
        pygame.display.flip()

    # =========================================================================
    #  Game Update Inlcuding Display
    def PlayNextMove(self, action):
        # Calculate DeltaFrameTime
        DeltaFrameTime = self.clock.tick(FPS)
        self.FrameCount = self.FrameCount + 1

        Quit = False
        # ====================================
        #  Process Keyboard Entry
        KeyPressed = pygame.key.get_pressed()
        if (KeyPressed[pygame.K_ESCAPE]):
            print("Esc pressed")
            Quit = True
        if (KeyPressed[pygame.K_q]):
            print("Esc pressed")
            Quit = True
        pygame.event.pump()  # Always need to Process event queue
        # ===================================

        PlayerMissed = False
        screen.fill(BLACK)

        # update our Player Paddle
        self.paddle1YPos = updatePaddle1(action, self.paddle1YPos, DeltaFrameTime)
        drawPaddle1(self.paddle1YPos)

        # Update  AI Right paddle
        self.paddle2YPos = updatePaddle2(self.paddle2YPos, self.ballYPos, DeltaFrameTime)
        drawPaddle2(self.paddle2YPos)

        # update our vars by updating ball position
        [PlayerMissed, self.ballXPos, self.ballYPos, self.ballXDirection, self.ballYDirection,
         self.BallColor] = updateBall(self.paddle1YPos, self.paddle2YPos, self.ballXPos, self.ballYPos,
                                      self.ballXDirection, self.ballYDirection, DeltaFrameTime, self.BallColor)
        # draw the ball
        drawBall(self.ballXPos, self.ballYPos, self.BallColor)
        #

        TimeDisplay = self.font.render("Frame: " + str(self.FrameCount), True, (255, 255, 255))
        screen.blit(TimeDisplay, (50., 40.))

        # update the Game Display
        pygame.display.flip()

        # return the score and the Player Paddle, Ball Position adn Direction
        return self.FrameCount, PlayerMissed, Quit

    # =========================================================================
    # Return the Curent Game State
    def ReturnCurrentState(self):
        # Simply return state
        return [self.paddle1YPos, self.ballXPos, self.ballYPos, self.ballXDirection, self.ballYDirection]
# =========================================================================


# =========================================================================