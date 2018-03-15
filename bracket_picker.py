import pprint
import random

pp = pprint.PrettyPrinter(indent=4)

SEED_VS_SEED_FILE = 'seed_vs_seed.txt'
TOP_25_VOTES_FILE = 'top_25_votes.txt'
GAMES_FILE        = 'games.txt'


def simulate_n_tournaments(n):
    tournament_wins = {}
    for i in range(n):
        winner = simulate_tournament(False)
        if winner in tournament_wins:
            tournament_wins[winner] += 1
        else:
            tournament_wins[winner] = 1

    tournament_wins = sorted( ((v,k) for k,v in tournament_wins.iteritems()), reverse=True)

    print('\n\n\n After {} Simulations - Teams with wins:'.format(n))
    pp.pprint(tournament_wins)
    return winner


def simulate_tournament(verbose):
        games = dict(all_games)

        for round in range(1, 7):
            games = simulate_round(games, round, verbose)
        return games


def simulate_round(games, round, verbose):
    if verbose:
        if round   == 1: print("Beginning calculations...\n\nRound of 64 games:")
        elif round == 2: print("\nRound of 32 games:")
        elif round == 3: print("\nSweet 16 games:")
        elif round == 4: print("\nElite Eight games:")
        elif round == 5: print("\nFinal Four games:")
        elif round == 6: print("\nChampionship game:")   
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
        if round   == 1: print("\nRound of 64 winners:")
        elif round == 2: print("\nRound of 32 winners:")
        elif round == 3: print("\nSweet 16 winners:")
        elif round == 4: print("\nElite Eight winners:")
        elif round == 5: print("\nFinal Four winners:")
        elif round == 6: 
            print("\nChampions:\n{}".format(games.values()[0][0]))
            return games.values()[0][0]
        pp.pprint(games)

    return next_round_games if round < 6 else games.values()[0][0]


'''
Calculates a win percentage bonus to be given a team based on top 25 votes.

The current implementation looks at the total top 25 votes received by each
team and divides this number by gamma, currently set to 75.  The bonus is then
calculated to be the first team's rank bonus minus the second team's rank
bonus.  This isn't taken as an absolute value as the value is added to the first
team's odds and subtracted from the second team's odds.  So if two teams are
50/50 and the bonus is calculated to be +5, the odds will turn to 55/45.

If number 1 ranked Virginia (1625 votes) is playing number 4 ranked
Michigan State (1356 votes), the bonus given to Virginia will be:
(1625/75) - (1356/75) = 3

This will result in a 6 percentage swing (+3 and -3) for Virginia over
Michigan State.  From 50/50 to 53/47, for instance.

If Virginia plays an unranked team, the bonus given to Virginia will be:
(1625/75) - (0/75) = 21

This will result in a 42 percentage swing (+21 and -21) for Virginia over their
unranked opponent, From 50/50 to 71/29, for instance.
'''
def get_top_25_bonus(team1, team2):
    gamma = 75
    team1_rank_bonus, team2_rank_bonus = (0, 0)

    if team1 in rankings:
        team1_rank_bonus = rankings[team1]/gamma
    
    if team2 in rankings:
        team2_rank_bonus = rankings[team2]/gamma

    return team1_rank_bonus - team2_rank_bonus
    

def get_winner(matchup):
    team1, team2 = matchup.keys()
    team1_seed, team2_seed = matchup.values()
    team1_odds = (50 * .66) + (seed_vs_seed[team1_seed][team2_seed] * .34)

    overall_bonus = get_top_25_bonus(team1, team2)

    rand_int = random.randint(0, 100)
    variance = 0
    if (abs(int(team1_seed)-int(team2_seed))) > 0:
        variance = abs(int(team1_seed)-int(team2_seed))/4
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
all_games = parse_games()
simulate_tournament(True)
# simulate_n_tournaments(10000)
