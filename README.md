Pong Game Genetic Algorithm Learning
Genetic Algorithm Based Learning for simple Pong PyGame. This python based Pong Game (control of Left Hand Yellow Paddle against a programmed RHS Paddle)

alt text

The Objective is simply measured as successfully returning of the Ball by the Yellow Left Hand Agent, evolved from Genetic Algorithm.
The programmed opponent Right Hand Paddle player is a pretty hot player. So success is simply the ability to return ball. In this Interpration, Success is deemed when the Player is able to continues to return the Ball, without Missing for 500 Game Frames. The follwoing diagram demonstrates the evolution of the Score, through 30 Genetic Algorithm Epoch cycles. (Which is pretty fast, much faster and more Robust than Nueral Net Procesing !)

alt text

The use of Genetic Algorithms and some Fuzzy Logic has been inspired from frustrations with Nueral Net Reinforcement processing being so slow, lack of robustness and lack of interpretation. As with the other Pong Experiment below, this relies upon a capture of Ball and player positions. So it DOES NOT generalise as Convolutional Reinforcement learning methods have the advantage of.

The Paddle, Ball positions and Direction are passed into a Fuzzy Logic Interetation (Or basic Binning) so as to map into Genome Based Rules Table. The relative Postion of the Ball is interprested to (Above, Same, Below) and the Distance to the Ball (Far, Med, Near) and the Ball Direction as (Left, Right). The Output Action, as decribd in the Genome is for (U:Up, S:same, D:Down)
The advantage of Fuzzy Logic (and Genetic Algorith Development) is that it allows the developed Genomes rules to be Human Readable, Interpreted and Reviewable. This is major advantage over Nueral network based solutions which are effectively Black Box.

The Genomes can either be displayed either in a Flat Genome String Sequence Structure or laid out in a Tabular Structure. The Tabular Strcuture ie easily interepeted by humans. See the example below, halfway through the Training.

alt text

This shows the Console Output part way through evolution, with the Best Genome Displayed in a Tabular Format and the Population of Genomes displayed as a set of Genome sequences with their scores. The Populations shows the Top most Genome is already achieved Optimum perfomance (500), with the other Genomes (Mutated, Children, Random) not perfoming quite so well.

A review of the Best Genome in Tabular format (at the conclusion of the Training Epochs) can be compared against an intuitive understanding of the optimum Pong Player perfomance. Basically the Paddle should move U (up) when the Paddle is Below the Ball and Paddle should move D (Down) when Pddle is Above the Ball. This is particularly critical when the Ball is moving Left towards the Player Paddle. The Paddle Action when Moving Right, is not so critical, as the AI has enough time to to respond, waiting for the Ball to be returned. When the Paddle is at the 'same' height as the ball, it does not need to do any action 'S' (Same)

Useage
python TrainPongGA.py

This main Training runs through a Population of 14 x PongGenomes, and resorts and releselects the best Genomes at each Epoch, based upon the scores acehievd for each Genome in the population. A Total of only 30 Epochs appears to be needed to train the Population, and evolve consistent results.

The Genetic Algorithm choice selections (following a sorted population) are as follows :

Keep Top Two Scoring Genomes in the Population [0,1] - Also noting to potentially replace the top [0] entry with the Best Ever Genome
The Next 5 [2,3,4,5,6,7 ] Genomes are Created as Mutants from the top two [0] and [1] - Just a single Bit is changed at random
The next four [8,9,10,11] Are Created as Childen from the Top two, through crossover splits (Two crossover points) of [0] and [1]
The last two slots [12,13] Are two compltely new Random Genomes.
This new Population is then reevaluated by playing through the game for Genome of the Population and capturing the Frame Score Count (Number of Frames played, until the Paddle misses the returned Ball) for each.

Supporting Classes
The Genome class describes the Genome methods: Genetic Modifications and CLI Display methods : PongGenome.py

The Py Game based Pong Game is:
PongGame.py

ExplicitPong.Py is a Main Executable, which is used to set up an intuitive optimum Genome, so as to compare performance and the evolved Genomes against.

Other Pong Experiments
Please see my other repository for a Convolotional DQN game of Pong from Game Screen Imagary https://github.com/JulesVerny/PongConvolutionalDQN and and Explcit Nueral network based upon Game Paramters Ball Postion, and Player Position https://github.com/JulesVerny/PongReinforcementLearning

Flappy Bird
Please look into the Flappy Bird Sub Directory for an Example of the same Approach used for Flappy Bird Game. Not so Successful

Acknowledgments:
The Pong Game Code is based upon Siraj Raval's inspiring vidoes on Machine learning and Reinforcement Learning [ Which does employ full convolutional DQN example]: https://github.com/llSourcell/pong_neural_network_live