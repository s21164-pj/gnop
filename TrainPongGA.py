#
#
#  requires pygame, numpy, matplotlib, keras [and hence Tensorflow or Theono backend]
# ==========================================================================================
from PongGame import PongGame  # import The Pong Game
from PongGenome import PongGenome
#
import random
import matplotlib.pyplot as plt
import operator

#
# =======================================================================

MAX_EVALUATE_FRAMES = 500
MAXEPOCHS = 31


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

    if (DeltaY >= 15):
        HString = 'Below'
    if (DeltaY < -15):
        HString = 'Above'

    # Enumerate the Rising/ Falling Values
    if (BDirection < 0):
        DirString = 'Left'
    else:
        DirString = 'Right'

    return DString, HString, DirString


# ======================================================================
# Drfgine a copy Genome metod to avoid Copy By Ref issues
def CopyGenome(OriginalGenome):
    NewGenome = PongGenome()
    NewGenome.DistanceValues = OriginalGenome.DistanceValues
    NewGenome.HeightValues = OriginalGenome.HeightValues
    NewGenome.BallDirection = OriginalGenome.BallDirection
    NewGenome.LengthGenome = OriginalGenome.LengthGenome
    NewGenome.score = -1
    NewGenome.PongGN = list(OriginalGenome.PongGN)
    return NewGenome


# =================================================================

# Main Experiment Method
def EvaluateGenome(TheGenome):
    FrameTime = 0

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
    # Main Evaluate Cycle
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
        # if(not(BestAction== AppliedAction)):
        #	print("Optimum Action: ", BestAction, "  Identified Action: ",AppliedAction, "  Player-Ball: ", (PlayerYPos +30- BallYPos+5))

        #  Now Apply the Recommended Action into the Game
        FrameCount, PMissed, GameQuit = TheGame.PlayNextMove(AppliedAction)

        # Move FrameTime Click
        FrameTime = FrameTime + 1

    TheGenome.SetScore(FrameTime)

    return GameQuit


# =======================================================================
def TrainPopulation():
    print()
    print("Creating Player Population set")

    EpochCount = 0
    HighestScore = 0
    TrainQuit = False

    GameHistory = []

    # Create a Best Ever Genome to Keep
    BestEverScore = 0
    BestEverGenome = PongGenome()

    # Create an Initial Population of 14 Genomes
    PlayerPopulation = []
    for ix in range(14):
        PlayerPopulation.append(PongGenome())

    print("Display Initial Population: ")
    for AGenome in PlayerPopulation:
        AGenome.DisplayFlat()

    # ====================================================
    print("*** Now Run Epoch Evaluations  *** ")
    # Now Train the whole Population through MAXEPOCHS

    while ((EpochCount < MAXEPOCHS) and (not TrainQuit)):

        # For Evaluate Each of the Genomes in the Population
        for AGenome in PlayerPopulation:
            TrainQuit = EvaluateGenome(AGenome)
            if (TrainQuit):
                break

        # Now Sort the Population into Highest Scores
        PlayerPopulation.sort(key=operator.attrgetter('score'), reverse=True)

        HighestScore = PlayerPopulation[0].score
        # Check the Best Ever Genome and Capture it
        if (HighestScore > BestEverScore):
            BestEverScore = HighestScore
            BestEverGenome = CopyGenome(PlayerPopulation[0])
            BestEverGenome.SetScore(BestEverScore)

        if EpochCount % 5 == 0:
            # Display Current Best Genome
            print()
            print("Current Best Genome: ")
            BestEverGenome.DisplayGenome()
            for AGenome in PlayerPopulation:
                AGenome.DisplayFlat()
            print()

        # Pick and Retain Two (As Parents) into New Population
        # Best Parents  Exists as Top Two sorted entries [0] and [1]

        # But Ensure that Best Ever Genome Stays at [0]
        PlayerPopulation[0] = CopyGenome(BestEverGenome)
        PlayerPopulation[0].SetScore(HighestScore)

        # Mutate Six (Three from Best, and Three from second Best Genomes
        PlayerPopulation[2] = CopyGenome(PlayerPopulation[0])  # ensure copy by value
        PlayerPopulation[2].Mutate()
        PlayerPopulation[3] = CopyGenome(PlayerPopulation[0])  # ensure copy by value
        PlayerPopulation[3].Mutate()
        PlayerPopulation[4] = CopyGenome(PlayerPopulation[0])  # ensure copy by value
        PlayerPopulation[4].Mutate()

        PlayerPopulation[5] = CopyGenome(PlayerPopulation[1])
        PlayerPopulation[5].Mutate()
        PlayerPopulation[6] = CopyGenome(PlayerPopulation[1])
        PlayerPopulation[6].Mutate()
        PlayerPopulation[7] = CopyGenome(PlayerPopulation[1])
        PlayerPopulation[7].Mutate()

        # ** No Flips in Pong as three Actions So Flip not helpful

        # Create Four Children
        PlayerPopulation[8] = PongGenome()
        PlayerPopulation[8].InheritFromParents(PlayerPopulation[0], PlayerPopulation[1])
        PlayerPopulation[9] = PongGenome()
        PlayerPopulation[9].InheritFromParents(PlayerPopulation[0], PlayerPopulation[1])
        PlayerPopulation[10] = PongGenome()
        PlayerPopulation[10].InheritFromParents(PlayerPopulation[0], PlayerPopulation[1])
        PlayerPopulation[11] = PongGenome()
        PlayerPopulation[11].InheritFromParents(PlayerPopulation[0], PlayerPopulation[1])

        # Create Two Competely New Random Genomes
        PlayerPopulation[12] = PongGenome()
        PlayerPopulation[13] = PongGenome()

        EpochCount = EpochCount + 1

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
    PlayerPopulation[0].DisplayFlat()
    print()
    PlayerPopulation[0].DisplayGenome()

    print(" *** Demo the Best Genome Playing *** ")
    # Now Demo the Best Genome:
    TrainQuit = EvaluateGenome(PlayerPopulation[0])

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
