#!python3


import math
import argparse
import os


def calculate_avg_elo(elo1, elo2, T=400):
    exp_elo1 = 10 ** (elo1 / T)
    exp_elo2 = 10 ** (elo2 / T)
    avg_elo = math.log10((exp_elo1 + exp_elo2) / 2) * T
    return avg_elo


def calculate_avg_win(elo1, elo2, T=400):
    return 1 / (1 + 10 ** ((elo2 - elo1) / T))


def calculate_elo_diff(elo1, elo2, score1, score2, T=400, K=128):
    if score1 + score2 == 0:
        return 0
    expected_win = calculate_avg_win(elo1, elo2, T=T)
    win = score1 / (score1 + score2)
    elo_diff = K * (win - expected_win)
    return elo_diff


def calculate_elo_diff_team(
    t1_elo1, t1_elo2, t2_elo1, t2_elo2, t1_score, t2_score, T=400, K=128
):
    avg_elo1 = calculate_avg_elo(t1_elo1, t1_elo2, T=T)
    avg_elo2 = calculate_avg_elo(t2_elo1, t2_elo2, T=T)
    elo_diff1 = calculate_elo_diff(avg_elo1, avg_elo2, t1_score, t2_score, T=T, K=K)
    return elo_diff1


def load_players(elo_start=1500):
    players = {}
    with open("players.txt", "r") as f:
        for line in f:
            player = line.strip()
            players[player] = elo_start
    return players


def load_games():
    games = []
    with open("games.txt", "r") as f:
        for line in f:
            game = line.strip().split(" ")
            games.append(game)
    return games


T = 400
K = 128
elo_start = 1500


def generate_sh(players, elo_start, f):
    # generate shell script that, given a name, outputs the ELO rating
    f.write("#! /bin/bash\n")
    f.write("case $1 in\n")
    for player, elo in players.items():
        f.write(f"{player})\n")
        f.write(f"echo {elo:.0f}\n")
        f.write(";;\n")
    f.write("*)\n")
    f.write(f"echo {elo_start}\n")
    f.write(";;\n")

    f.write("esac\n")


def generate_sh_with_rankings(players, elo_start, f):
    # generate shell script that, given a name, outputs the ELO rating
    f.write("#! /bin/bash\n")
    f.write("case $1 in\n")
    for i, (player, elo) in enumerate(
        sorted(players.items(), key=lambda x: x[1], reverse=True)
    ):
        emoji = ["🥇", "🥈", "🥉"]
        icon = emoji[i] if i < 3 else ""

        f.write(f"{player})\n")
        f.write(f"echo {elo:.0f}{icon}\n")
        f.write(";;\n")
    f.write("*)\n")
    f.write(f"echo {elo_start}\n")
    f.write(";;\n")

    f.write("esac\n")

    # print rankings in the shell script as a comment
    f.write("\n# Rankings\n")
    for i, (player, elo) in enumerate(
        sorted(players.items(), key=lambda x: x[1], reverse=True)
    ):
        emoji = ["🥇", "🥈", "🥉"]
        icon = emoji[i] if i < 3 else ""
        f.write(f"# {i+1}. {player}: {elo:.0f}{icon}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-T", type=int, default=T, help="ELO performance rating scale")
    parser.add_argument("-K", type=int, default=K, help="ELO rating change magnitude")
    parser.add_argument("-E", type=int, default=elo_start, help="ELO rating start")
    parser.add_argument(
        "-o",
        type=str,
        default=False,
        help="outputs an shell scipt that generates the ELO ratings",
    )
    parser.add_argument(
        "-r",
        help="display rankings in the shell",
        action="store_true",
    )

    args = parser.parse_args()
    T = args.T
    K = args.K
    elo_start = args.E

    players = load_players()
    games = load_games()
    for game in games:
        elo_change = calculate_elo_diff_team(
            players[game[0]],
            players[game[1]],
            players[game[2]],
            players[game[3]],
            int(game[4]),
            int(game[5]),
            T=T,
            K=K,
        )
        players[game[0]] += elo_change
        players[game[1]] += elo_change
        players[game[2]] -= elo_change
        players[game[3]] -= elo_change

    if args.o:
        with open(args.o, "w") as f:
            if args.r:
                generate_sh_with_rankings(players, elo_start, f)
            else:
                generate_sh(players, elo_start, f)
            os.chmod(args.o, 0o755)

    print("Rankings")
    for i, (player, elo) in enumerate(
        sorted(players.items(), key=lambda x: x[1], reverse=True)
    ):
        emoji = ["🥇", "🥈", "🥉"]
        icon = emoji[i] if i < 3 else ""
        print(f" {i+1}. {player}: {elo:.0f}{icon}")
