# S8_Algorithmics
Advanced Algorithmics Project using Karger algorithm - April 2018

Al the data we use in our reports are in the interesting_result folder.

All programs are provided with an interactive command line and a help command.
Also, they export the results in a CSV file, name with the timestamp of the execution and the postfix "_analytics".

## For algo.ex

Run the algorithms on the examples provided in the 'exemples' directory.

usage: exemples.py [-h] [-d] [-r]

optional arguments:
  -h, --help       show this help message and exit
  -d, --debug      print debug logs, slows the program a lot, shouldn't run on
                   big graph nor many examples
  -r, --recursive  run only the recursive version with different value for a
                   and b

## For stat.ex

Run the algorithms on graphs generated uniformly, with the specified max number of vertices and the specified number of graphs.

usage: generator.py [-h] [-d] [-r] [-e] max_vertices graph_number

positional arguments:
  max_vertices     the number max number of vertices in the graph
  graph_number     the number of graph to generate and run

optional arguments:
  -h, --help       show this help message and exit
  -d, --debug      print debug logs, slows the program a lot, shouldn't run on
                   big graph nor many examples
  -r, --recursive  run only the recursive version with different value for a
                   and b
  -e, --export     export the generated graphs in the exports folder