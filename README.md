Everything is contained in the AStar.py file.

You can simply run this file from the command line or from an IDE of your choosing.

If you run the file without any command line arguments it will print a help message.

You specify the starting and ending boards using the '-s' and '-g' flags respectively.

By default the program uses manhatten distance for its heuristic. To use the incorrect tile heuristic add a '-p' flag.


Examples:

Manhatten Distance
./Astar.py -s 817263540 -g 123456780

Missed Tiles
./Astar.py -s 817263540 -g 123456780 -p
