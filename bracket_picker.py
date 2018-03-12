import pprint
import random

pp = pprint.PrettyPrinter(indent=4)
seed_vs_seed = {'1' : {'ovr' : 78.6}}
seed_num = '1'
games = {   1  : {'Virginia'       : '1', 'UMBC' : '16'},
            2  : {'Creighton'      : '8', 'Kansas St.' : '9'},
            3  : {'Kentucky'       : '5', 'Davidson' : '12'},
            4  : {'Arizona'        : '4', 'Buffalo' : '13'},
            5  : {'Miama (Fla.)'   : '6', 'Loyola Chicago' : '11'},
            6  : {'Tennessee'      : '3', 'Wright State' : '14'},
            7  : {'Nevada'         : '7', 'Texas' : '10'},
            8  : {'Cincinnati'     : '2', 'Georgia State' : '15'},
            9  : {'Xavier'         : '1', 'NCC/TSU' : '16'},
            10 : {'Missouri'       : '8', 'Florida State' : '9'},
            11 : {'Ohio St.'       : '5', 'South Dakota St.' : '12'},
            12 : {'Gonzaga'        : '4', 'UNCG' : '13'},
            13 : {'Houston'        : '6', 'San Diego State' : '11'},
            14 : {'Michigan'       : '3', 'Montana' : '14'},
            15 : {'Texas A&M'      : '7', 'Providence' : '10'},
            16 : {'North Carolina' : '2', 'Lipscomb' : '15'},
            17 : {'Villanova'      : '1', 'LIUB/RAD' : '16'},
            18 : {'Virginia Tech'  : '8', 'Alabama' : '9'},
            19 : {'West Virginia'  : '5', 'Murray State' : '12'},
            20 : {'Wichita State'  : '4', 'Marshall' : '13'},
            21 : {'Florida'        : '6', 'SBU/UCLA' : '11'},
            22 : {'Texas Tech'     : '3', 'SFA' : '14'},
            23 : {'Arkansas'       : '7', 'Butler' : '10'},
            24 : {'Purdue'         : '2', 'CSU Fullerton' : '15'},
            25 : {'Kansas'         : '1', 'Penn' : '16'},
            26 : {'Seton Hall'     : '8', 'NC State' : '9'},
            27 : {'Clemson'        : '5', 'New Mexico St.' : '12'},
            28 : {'Auburn'         : '4', 'Charleston' : '13'},
            29 : {'TCU'            : '6', 'ASU/SYR' : '11'},
            30 : {'Mich. St.'      : '3', 'Bucknell' : '14'},
            31 : {'Rhode Island'   : '7', 'Oklahoma' : '10'},
            32 : {'Duke'           : '2', 'Iona' : '15'},
        }

rankings = { 'Virginia' : 1625, 'Villanova' : 1516, 'Xavier' : 1510, 'Mich State' : 1356, 'Duke' : 1340, 'Gonzaga' : 1254, 'Michigan' : 1231, 'Cincinnati' : 1213, 'Kansas' : 1129,
            'Purdue' : 1096, 'Wichita State' : 861, 'North Carolina' : 852, 'Tennessee' : 825, 'Texas Tech' : 784, 'Arizona' : 739, 'Auburn' : 14, 'Ohio St.' : 603, 'West Virginia' : 486,
            'Clemson' : 422, 'Houston' : 247, 'Nevada' : 218, 'Florida' : 192, 'Miama (Fla.)' : 191, 'Rhode Island' : 86, 'St. Bonaventure' : 72, 'Kentucky' : 66, 'TCU' : 45, 'Loyola Chicago' : 43,
            'Virignia Tech' : 15, 'Seton Hall' : 10, 'Middle Tennessee' : 9, 'Creighton' : 8, 'Arkansas' : 4, 'Nebraska' : 2, 'Kansas St.' : 2, 'NC State' : 2, 'Florida St.' : 1, 'Buffalo' : 1,
            'New Mexico St.' : 1, 'Texas A&M' : 1

}
for line in open('seed_vs_seed.txt'):
    toks = line.split()
    if len(toks) == 8:
        seed_num = toks[4][1:]
        seed_vs_seed[seed_num] = {'ovr' : float(toks[7][:-1])}
    elif len(toks) == 4:
        opp_seed = toks[1][1:]
        win_percentage = float(toks[3][:-1])
        if seed_num in seed_vs_seed.keys():
            seed_vs_seed[seed_num][opp_seed] = win_percentage
        else:
            seed_vs_seed[seed_num] = {opp_seed: win_percentage}

for k, v in seed_vs_seed.items():
    for k1, v1 in v.items():
        if k1 == 'ovr':
            continue
        if v1 == 0.0:
            if seed_vs_seed[k1][k] == 0.0:

                seed_vs_seed[k][k1] = -1.0
                seed_vs_seed[k1][k] = -1.0


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

def simulate_tournament(verbose):
    games = {   1  : {'Virginia'       : '1', 'UMBC' : '16'},
            2  : {'Creighton'      : '8', 'Kansas St.' : '9'},
            3  : {'Kentucky'       : '5', 'Davidson' : '12'},
            4  : {'Arizona'        : '4', 'Buffalo' : '13'},
            5  : {'Miama (Fla.)'   : '6', 'Loyola Chicago' : '11'},
            6  : {'Tennessee'      : '3', 'Wright State' : '14'},
            7  : {'Nevada'         : '7', 'Texas' : '10'},
            8  : {'Cincinnati'     : '2', 'Georgia State' : '15'},
            9  : {'Xavier'         : '1', 'NCC/TSU' : '16'},
            10 : {'Missouri'       : '8', 'Florida State' : '9'},
            11 : {'Ohio St.'       : '5', 'South Dakota St.' : '12'},
            12 : {'Gonzaga'        : '4', 'UNCG' : '13'},
            13 : {'Houston'        : '6', 'San Diego State' : '11'},
            14 : {'Michigan'       : '3', 'Montana' : '14'},
            15 : {'Texas A&M'      : '7', 'Providence' : '10'},
            16 : {'North Carolina' : '2', 'Lipscomb' : '15'},
            17 : {'Villanova'      : '1', 'LIUB/RAD' : '16'},
            18 : {'Virginia Tech'  : '8', 'Alabama' : '9'},
            19 : {'West Virginia'  : '5', 'Murray State' : '12'},
            20 : {'Wichita State'  : '4', 'Marshall' : '13'},
            21 : {'Florida'        : '6', 'SBU/UCLA' : '11'},
            22 : {'Texas Tech'     : '3', 'SFA' : '14'},
            23 : {'Arkansas'       : '7', 'Butler' : '10'},
            24 : {'Purdue'         : '2', 'CSU Fullerton' : '15'},
            25 : {'Kansas'         : '1', 'Penn' : '16'},
            26 : {'Seton Hall'     : '8', 'NC State' : '9'},
            27 : {'Clemson'        : '5', 'New Mexico St.' : '12'},
            28 : {'Auburn'         : '4', 'Charleston' : '13'},
            29 : {'TCU'            : '6', 'ASU/SYR' : '11'},
            30 : {'Mich. St.'      : '3', 'Bucknell' : '14'},
            31 : {'Rhode Island'   : '7', 'Oklahoma' : '10'},
            32 : {'Duke'           : '2', 'Iona' : '15'},
        }
    if verbose:
        print("Beginning calculations...\n")
        print("Round of 64 games:")

        pp.pprint(games)

    for game, matchup in games.items():
        winner = get_winner(matchup)
        games[game] = [winner[0], winner[1]]

    if verbose:
        print("\nRound of 64 winners:")
        pp.pprint(games)

    i = 1
    game_num = 1
    temp_dict = {}
    while i < len(games.keys()) + 1:
        temp_dict[game_num] = {games[i][0] : games[i][1], games[i+1][0] : games[i+1][1]}
        i += 2
        game_num += 1

    games = temp_dict

    if verbose:
        print("\nRound of 32 games:")
        pp.pprint(games)

    for game, matchup in games.items():
        winner = get_winner(matchup)
        games[game] = [winner[0], winner[1]]

    if verbose:
        print("\nRound of 32 winners:")    
        pp.pprint(games)

    i = 1
    game_num = 1
    temp_dict = {}
    while i < len(games.keys()) + 1:
        temp_dict[game_num] = {games[i][0] : games[i][1], games[i+1][0] : games[i+1][1]}
        i += 2
        game_num += 1

    games = temp_dict

    if verbose:
        print("\nSweet Sixteen games:")
        pp.pprint(games)

    for game, matchup in games.items():
        winner = get_winner(matchup)
        games[game] = [winner[0], winner[1]]

    if verbose:
        print("\nSweet Sixteen winners:")    
        pp.pprint(games)

    i = 1
    game_num = 1
    temp_dict = {}
    while i < len(games.keys()) + 1:
        temp_dict[game_num] = {games[i][0] : games[i][1], games[i+1][0] : games[i+1][1]}
        i += 2
        game_num += 1

    games = temp_dict

    if verbose:
        print("\nElite Eight games:")
        pp.pprint(games)

    for game, matchup in games.items():
        winner = get_winner(matchup)
        games[game] = [winner[0], winner[1]]
        
    if verbose:
        print("\nElite Eight winners::")    
        pp.pprint(games)

    i = 1
    game_num = 1
    temp_dict = {}
    while i < len(games.keys()) + 1:
        temp_dict[game_num] = {games[i][0] : games[i][1], games[i+1][0] : games[i+1][1]}
        i += 2
        game_num += 1

    games = temp_dict

    if verbose:
        print("\nFinal Four games:")
        pp.pprint(games)

    for game, matchup in games.items():
        winner = get_winner(matchup)
        games[game] = [winner[0], winner[1]]
        
    if verbose:
        print("\nFinal Four winners:")    
        pp.pprint(games)

    i = 1
    game_num = 1
    temp_dict = {}
    while i < len(games.keys()) + 1:
        temp_dict[game_num] = {games[i][0] : games[i][1], games[i+1][0] : games[i+1][1]}
        i += 2
        game_num += 1

    games = temp_dict

    if verbose:
        print("\nChampionship game:")
        pp.pprint(games)

    for game, matchup in games.items():
        winner = get_winner(matchup)
        games[game] = [winner[0], winner[1]]
        
    if verbose:
        print("\nChampions:")    
        pp.pprint(games)
    return games.values()[0][0]

tournament_wins = {}

# pp.pprint(simulate_tournament(True))


# Uncomment to simulate many tournaments
for i in range(100000):
    winner = simulate_tournament(False)
    if winner in tournament_wins:
        tournament_wins[winner] += 1
    else:
        tournament_wins[winner] = 1

tournament_wins = sorted( ((v,k) for k,v in tournament_wins.iteritems()), reverse=True)

print('\n\n\n After 100000 Simulations - Teams with wins:')
pp.pprint(tournament_wins)





