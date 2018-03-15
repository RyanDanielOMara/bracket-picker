import pprint
import random

pp = pprint.PrettyPrinter(indent=4)

SEED_VS_SEED_FILE = 'seed_vs_seed.txt'
TOP_25_VOTES_FILE = 'top_25_votes.txt'
GAMES_FILE        = 'games.txt'

def simulate_tournament(verbose):
        games = parse_games()

        for round in range(1, 7):
            games = simulate_round(games, round, verbose)
        return games


def simulate_n_tournaments(n):
    tournament_wins = {}
    for i in range(n):
        winner = simulate_tournament(False)
        if winner in tournament_wins:
            tournament_wins[winner] += 1
        else:
            tournament_wins[winner] = 1

    tournament_wins = sorted( ((v,k) for k,v in tournament_wins.iteritems()), reverse=True)

    print('\n\n\n After 100000 Simulations - Teams with wins:')
    pp.pprint(tournament_wins)
    return winner

def simulate_round(games, round, verbose):
    if verbose:
        if round == 1:
            print("Beginning calculations...\n")
            print("Round of 64 games:")
        elif round == 2:
            print("\nRound of 32 games:")
        elif round ==3:
            print("\nSweet 16 games:")
        elif round == 4:
            print("\nElite Eight games:")
        elif round == 5:
            print("\nFinal Four games:")
        elif round == 6:
            print("\nChampion game:")   
        pp.pprint(games)

    # Calculate the winner
    for game, matchup in games.items():
        winner = get_winner(matchup)
        games[game] = [winner[0], winner[1]]

    # Update games dictionary
    i = 1
    game_num = 1
    next_round_games = {}
    if round < 6:
        while i < len(games.keys()) + 1:
            next_round_games[game_num] = {games[i][0] : games[i][1], games[i+1][0] : games[i+1][1]}
            i += 2
            game_num += 1

    if verbose:
        if round == 1:
            print("\nRound of 64 winners:")
        elif round == 2:
            print("\nRound of 32 winners:")
        elif round ==3:
            print("\nSweet 16 winners:")
        elif round == 4:
            print("\nElite Eight winners:")
        elif round == 5:
            print("\nFinal Four winners:")
        elif round == 6:
            print("\nChampions:")
            print(games.values()[0])
            return games.values()[0][0]
        pp.pprint(games)

        return next_round_games


def get_winner(matchup):
    team1, team2 = matchup.keys()
    team1_seed, team2_seed = matchup.values()
    team1_odds = seed_vs_seed[team1_seed][team2_seed]

    team1_rank_bonus = 0
    team2_rank_bonus = 0

    if team1 in rankings:
        team1_rank_bonus = rankings[team1]/75
    
    if team2 in rankings:
        team2_rank_bonus = rankings[team2]/75

    overall_bonus = team1_rank_bonus-team2_rank_bonus


    if team1_odds == -1:
        team1_overall = seed_vs_seed[team1_seed]['ovr']
        team2_overall = seed_vs_seed[team2_seed]['ovr']
        overall_percent = team1_overall + team2_overall
        if overall_percent == 0:
            pick = random.randint(0, 100)
            team1_odds = 100-pick
            team2_odds = pick
        else:
            team1_odds = (team1_overall / overall_percent) + overall_bonus
            team2_odds = (team2_overall / overall_percent) - overall_bonus

        rand_int = random.randint(0, 100)
        variance = 0
        if (abs(int(team1_seed)-int(team2_seed))) > 0:
            variance = 30/(abs(int(team1_seed)-int(team2_seed)))
        sign = random.randint(0, 1)
        rand_int = rand_int + variance if sign == 0 else rand_int - variance
        if int(team1_odds) > rand_int:
            return (team1, team1_seed)
        else:
            return (team2, team2_seed)

    else:
        rand_int = random.randint(0, 100)
        variance = 0
        if (abs(int(team1_seed)-int(team2_seed))) > 0:
            variance = 200/(abs(int(team1_seed)-int(team2_seed)))
        sign = random.randint(0, 1)
        rand_int = rand_int + variance if sign == 0 else rand_int - variance


        if int(team1_odds + overall_bonus) > rand_int:
            return (team1, team1_seed)
        else:
            return (team2, team2_seed)


def parse_games():
    games = {}
    game = 1
    
    for line in open(GAMES_FILE):
        team1, team1_seed, team2, team2_seed = line.strip().split(',')
        games[game] = {team1 : team1_seed, team2 : team2_seed}
        game += 1
    return games


def parse_top_25_votes():
    rankings = {}

    for line in open(TOP_25_VOTES_FILE):
        team, votes = line.split(',')
        rankings[team] = int(votes)

    return rankings

'''
Parses a comma separated file containing the win percentages of teams with a given seed,
both the overall win percentage and a seed vs. seed win percentage.
'''
def parse_seed_vs_seed():
    seed_vs_seed = {}

    for line in open(SEED_VS_SEED_FILE):
        seed, opp_seed, win_percentage = line.strip().split(',')
        win_percentage = float(win_percentage)

        # Store seed's overall win percentage
        if opp_seed == 'ovr':
            seed_vs_seed[seed] = {'ovr' : win_percentage}
        
        # Store seed vs. seed win percentage
        else:
            if seed in seed_vs_seed.keys():
                seed_vs_seed[seed][opp_seed] = win_percentage
            else:
                seed_vs_seed[seed] = {opp_seed: win_percentage}

    return seed_vs_seed


seed_vs_seed = parse_seed_vs_seed()
rankings = parse_top_25_votes()
games = parse_games()
simulate_tournament(True)
