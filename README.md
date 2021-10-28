# WatersortPuzzle

this is an algorithm to solve the puzzle game called water sort.
original game is avaliable at google play store.

game rules are as follows:

main mechanic of the game is pouring water from a tube to another.
pouring water is only possible if there is avaliable space at the top of the target tube and,
water color(symbolized with differnt numbers in this project) on the top of targeted tube is the same with the one on top of source tube.

pouring water continues as long as target tube complitely fills up or same colored water run out at the source tube.
empty tubes can be targetted by all colors

game is won when all tubes are pure (are fully filled up and contains only one color of water).

to run the files you need python with keras, tensorflow and numpy installed.
if you have python but not tensorflow or keras run "pip install tensorflow", "pip install keras" and "pip insall numpy" lines on console.

to train the ai run the ai.py file 
(it will override current watersort.h5 when process ends so it is not recommended if it is not your intention)

to shuffle and solve a puzzle run main.py file

main.py will display initial state, shuffeled state and calculated moves to solve the puzzle while processing it.
moves are formatted as [position1, position2] and means "pour water from position1 to position2".

unfortinately I couldn't bothered to implement a system to enter your own shuffeled positions so it must be done by editing the code.
to enter your initial position edit my_glasses variable to be same with your desired position,
uncomment my_table.glasses = my_glasses line by removing # at the begining, 
comment print(my_table.shuffle(6)) line by adding "#" to begining.

if you want to change the shuffling amount change the number inside print(my_table.shuffle(6)) line.
