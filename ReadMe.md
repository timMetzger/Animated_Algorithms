# Animated Algorithms

Currently this project has animated algorithms for sorting, pathfinding, spanning trees, tic-tac-toe, and connect-four. I am hoping to add the box coloring problem(similar to the coloring the states problem) and the airplane scheduler problem

## Sorting
For these sorting algorithms I took inspirations from the famous animated sorting algorithm videos with sound and made my own along with a timer for comparison. The following are currently implemented.

Radix Sort

Quick Sort

Heap Sort

Bubble Sort

Selection Sort

Insertion Sort

## Pathfinding
The pathfinding algorithms are some of the most interesting ones that I have built. The user inputs the start and end points along with any obstacles or mazes they want, and the algorithm will find the path. The control scheme for this is as follows.

Left Click - Start Point

Right Click - End Point 

Middle Click - Wall

Q - Add weight to a tile

W - Generates an Unweighted Maze

E - Generates a Weighted Maze

**Currently, the following algorithms are implemented.**

Dijkstra

A-Star

Breadth First

Depth First

## Minimum Spanning Trees
This is another cool one that I haven't finalized. Currently, I need to find a better way of drawing the current state of the minimum tree so that the user can better visualize the algorithm. At the moment only Primm's algorithm is implemented as it is the easiest to visualize given its procedure. 

**Plan to add**
Reverse-Delete

Boruvka's

Kruskal's


##Tic-Tac-Toe & Connect Four
Both of these algorithms use the minimax algorithm to choose moves for the computer. The tic-tac-toe minimax works quite well as creating a balanced game. The connect-four minimax algorithm has a bit extra to it by using alpha beta pruning. Connect-four has proven more difficult to implement due to the scoring becoming more important in the computers decision making. 