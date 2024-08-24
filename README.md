## ELO Rating Calculator

### Description

This script computes the ELO ratings of players using their game results. It supports updating ratings based on team matches, with options to customize the ELO parameters.

### Features

- Generate ELO ratings based on game outcomes.
- Generate a shell script to view player ratings from the command line.

### Usage

#### Basic Command

```bash
./elo_rating_calculator.py
```


#### Options
- `-T [int]`: Set the ELO performance rating scale (default: 400).
- `-K [int]`: Set the ELO rating change magnitude (default: 128).
- `-E [int]`: Set the starting ELO rating (default: 1500).
- `-o [filename]`: Set the path of the output shell script for fetching ELO ratings (default: get_elo.sh).
- `--no-ranking`: Do not display player rankings.
- `-h`: Display help message.


#### Example

```bash
./elo_rating_calculator.py -T 300 -K 64 -E 1600 -o get_elo.sh
```

This command sets custom ELO parameters and generates a shell script named `get_elo.sh` that outputs player ratings.

### Input Files

- `players.txt`: Contains player names, each on a new line.
- `games.txt`: Contains game results in the format `player1 player2 player3 player4 score1 score2`.

### Output

Prints the updated ELO ratings sorted in descending order.
