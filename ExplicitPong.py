#
#
#  requires pygame, numpy, matplotlib, keras [and hence Tensorflow or Theono backend]
# ==========================================================================================
from PongGame import PongGame  # import The Pong Game
from PongGenome import PongGenome
#
import random
import matplotlib.pyplot as plt

#
# =======================================================================

MAX_EVALUATE_FRAMES = 250
MAXEPOCHS = 3


# =====================================================================
def GetFuzzyValues(BallX, BallY, PlayerY, BDirection):
    """Returns the Fuzzifed Values for Distance, Heioght and Rising"""
    """ Fuzzy Values Will need some Tuning  to get optimum GA performance"""

    DString = 'Null'
    HString = 'Same'
    DirString = 'Null'

    # Enumerate the Distance Values  : 'Far','Med','Near'
    if (BallX >= 175):
        DString = 'Far'
    if ((BallX < 175) and (BallX >= 50)):
        DString = 'Med'
    if (BallX < 50):
        DString = 'Near'

    # Enumerate the Height Values: ('Above', 'Same','Below')
    DeltaY = (PlayerY + 30) - (BallY + 5)

    if (DeltaY >= 10):
        HString = 'Below'
    if (DeltaY < -10):
        HString = 'Above'

    # Enumerate the Rising/ Falling Values
    if (BDirection < 0):
        DirString = 'Left'
    else:
        DirString = 'Right'

    return DString, HString, DirString


# ======================================================================
# Main Experiment Method
def EvaluateGenome(TheGenome):
    FrameTime = 0

    GameHistory = []

    # Create our PongGame instance
    TheGame = PongGame()
    # Initialise Game
    TheGame.InitialDisplay()
    #

    # Initialise NextAction  Assume Action is scalar:  0:stay, 1:Up, 2:Down
    AppliedAction = 'S'
    PMissed = False
    GameQuit = False

    # =================================================================
    # Main Evlate  Loop
    while ((FrameTime < MAX_EVALUATE_FRAMES) and (not PMissed) and (not GameQuit)):

        # Get Current Game State
        [PlayerYPos, BallXPos, BallYPos, BallXDirection, BallYDirection] = TheGame.ReturnCurrentState()
        DValue, HValue, DirValue = GetFuzzyValues(BallXPos, BallYPos, PlayerYPos, BallXDirection)
        # print(" Fuzzy Values D,H,Dir :",DValue, " , ", HValue, " , ", DirValue)

        AppliedAction = 'S'

        # print(" Fuzzy Values D,H,Dir :",DValue, " , ", HValue, " , ", DirValue)

        # Uncomment this out to Test Game Engine:  Player Paddle then Acts the same way as Right Hand programmed Player
        # Move up if ball is higher than Openient Paddle
        if (PlayerYPos + 30 > BallYPos + 5):
            BestAction = 'U'
        # Move down if ball lower than Opponent Paddle
        if (PlayerYPos + 30 < BallYPos + 5):
            BestAction = 'D'
        # =============================
        #  Use Genome to Select Identified Action
        AppliedAction = TheGenome.RtnAction(HValue, DValue, DirValue)

        # print("HValue: ", HValue ,"   Aaction:  ", AppliedAction)
        if (not (BestAction == AppliedAction)):
            print("Optimum Action: ", BestAction, "  Identified Action: ", AppliedAction, "  Player-Ball: ",
                  (PlayerYPos + 30 - BallYPos + 5))

        #  Now Apply the Recommended Action into the Game
        FrameCount, PMissed, GameQuit = TheGame.PlayNextMove(AppliedAction)

        # Move FrameTime Click
        FrameTime = FrameTime + 1

    TheGenome.SetScore(FrameTime)

    return GameQuit


# =======================================================================
def TrainPopulation():
    print()
    print("Creating The Explicit Player ")

    EpochCount = 0
    HighestScore = 0
    TrainQuit = False

    GameHistory = []

    # Initialise and Clear Pong Genome
    TheGenome = PongGenome()
    TheGenome.Clear()
    #
    #
    print()
    print("Set Explicit Player Settings : ")

    # HeightValues = ('Above', 'Same','Below')   #  DistanceValues = ('Far','Med','Near')  # BallDirection = ('Left','Right')  : Values : ['U', 'S', 'D']
    # If Ball Above,  Set Player Down
    TheGenome.SetValue('Above', 'Far', 'Left', 'D')
    TheGenome.SetValue('Above', 'Med', 'Left', 'D')
    TheGenome.SetValue('Above', 'Near', 'Left', 'D')
    TheGenome.SetValue('Above', 'Far', 'Right', 'D')
    TheGenome.SetValue('Above', 'Med', 'Right', 'D')
    TheGenome.SetValue('Above', 'Near', 'Right', 'D')

    # If Ball Below,  Set Player Up
    TheGenome.SetValue('Below', 'Far', 'Left', 'U')
    TheGenome.SetValue('Below', 'Med', 'Left', 'U')
    TheGenome.SetValue('Below', 'Near', 'Left', 'U')
    TheGenome.SetValue('Below', 'Far', 'Right', 'U')
    TheGenome.SetValue('Below', 'Med', 'Right', 'U')
    TheGenome.SetValue('Below', 'Near', 'Right', 'U')

    TheGenome.DisplayGenome()
    TheGenome.DisplayFlat()

    print("*** Now Run Epoch Evaluations  *** ")
    # Now Train the whole Population through MAXEPOCHS
    # ===================================================================
    while ((EpochCount < MAXEPOCHS) and (not TrainQuit)):
        # For Evaluate Each of the Genomes in the Population
        TrainQuit = EvaluateGenome(TheGenome)

        EpochCount = EpochCount + 1
        #
        HighestScore = TheGenome.score

        print("Epoch: ", EpochCount, "  High Score: ", HighestScore)
        GameHistory.append((EpochCount, HighestScore))
    # ======================================
    print("*** End of Training Epochs*** ")

    # ==================================
    #  Plot the Score vs Epochs  profile
    x_val = [x[0] for x in GameHistory]
    y_val = [x[1] for x in GameHistory]

    plt.plot(x_val, y_val)
    plt.xlabel("Epochs ")
    plt.ylabel("Best Score")
    plt.show()
    # ==========================
    print()
    print("Best Genome: ")
    TheGenome.DisplayFlat()
    print()
    TheGenome.DisplayGenome()

    print("******** END OF SHOW ********* ")
    print()


# =============================================================================

def main():
    #
    # Main Method Just Play our Experiment
    TrainPopulation()


# =======================================================================
if __name__ == "__main__":
    main()
