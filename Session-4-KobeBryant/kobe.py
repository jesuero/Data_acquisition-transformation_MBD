import json

# In this script some calculations are done over a json that contains NBA stats from Kobe Bryant

def load_json(path):
    """
    Loads JSON file in given path into a dictionary that will
    be returned.
    Params
    -------
    path : str
        The path to the target JSON file.
    Return
    -------
    d : dic
        The dictionary with the JSON content loaded.
    """
    with open(path, "r") as input_file:
        d = json.load(input_file)
    return d

def regular_stats():
    '''
    The next parameters are taken from the Regular Season stats of the json
    SEASON_ID
    PLAYER_AGE
    GP (Games Played)
    PTS (Average Points Scored)
    AST (Average Assists)
    REB (Average Rebounds)
    -------
    The function returns:
    regular_season_stats: list of lists containing all the previous parameters for each season
    season_max_points: season with more points scored (points scored per season are GP * PTS)
    max_points: points scored in season_max_points
    season_min_points: season with more points scored (points scored per season are GP * PTS)
    min_points: points scored in season_min_points
    avg_career_points: average points scored in his career (all seasons)
    avg_career_assists: average assists scored in his career (all seasons)
    avg_career_rebounds: average rebounds scored in his career (all seasons)
    '''
    regular_season_stats = []
    regular_season_stats.append(["AÑO DE LA TEMPORADA", "EDAD DEL JUGADOR", "PARTIDOS DISPUTADOS", 
    "MEDIA DE PUNTOS ANOTADOS", "MEDIA DE ASISTENCIAS REPARTIDAS", "MEDIA DE REBOTES RECOGIDOS"])
    if d["resultSets"][0]["name"] == "SeasonTotalsRegularSeason":
        for r in d["resultSets"][0]["rowSet"]:
            row = []
            row.extend([r[1], r[5], r[6], r[26], r[21], r[20]])
            regular_season_stats.append(row)

    total_pts = []
    total_ast = []
    total_reb = []
    for season in regular_season_stats[1:]:
        total_pts.append(season[2]*season[3])
        total_ast.append(season[2]*season[4])
        total_reb.append(season[2]*season[5])
    
    max_points = max(total_pts)
    season_max_points = regular_season_stats[total_pts.index(max(total_pts))][0]
    min_points = min(total_pts)
    season_min_points = regular_season_stats[total_pts.index(min(total_pts))][0]
    avg_career_points = sum(total_pts) / len(total_pts)
    avg_career_assists = sum(total_ast) / len(total_ast)
    avg_career_rebounds = sum(total_reb) / len(total_reb)
    
    return(regular_season_stats, max_points, min_points, season_max_points, season_min_points, avg_career_points, avg_career_assists, avg_career_rebounds)

def post_stats():
    '''
    The next parameters are taken from the Post Season stats of the json
    SEASON_ID
    PTS (Average Points Scored)
    -------
    The function returns a list of lists containing all the previous parameters for each season
    '''
    post_season_stats = []
    post_season_stats.append(["AÑO DE LA TEMPORADA", "MEDIA DE PUNTOS ANOTADOS"])
    if d["resultSets"][2]["name"] == "SeasonTotalsPostSeason":
        for r in d["resultSets"][2]["rowSet"]:
            row = []
            row.extend([r[1], r[26]])
            post_season_stats.append(row)
    return post_season_stats

def post_regular_comparison(regular_season_stats, post_season_stats):
    '''
    This function takes as parameters two list of lists
    one containing the stats from the regular season and the other stats from the post season
    -----
    Compares the lists and returns and array whose values are:
    True: if average points scored in Post Season is higher than average points scored in Regular Season
    False: if is lower
    N/A: if Post Season was not played
    '''
    better_in_post_season = ["N/A"] * len(regular_season_stats)
    for regular, post in zip(regular_season_stats, post_season_stats):
        if(post[1] > regular[3]):
            better_in_post_season[regular_season_stats.index(regular)] = True
        elif(post[1] < regular[3]):
            better_in_post_season[regular_season_stats.index(regular)] = False
    return better_in_post_season[1:]


if __name__ == "__main__":
    # json with kobe bryant stats is loaded
    d = load_json("kobe.json")
    # getting the parameters returned from the regular stats function and storing them in regular_stats
    regular_stats = regular_stats()
    print("Season with more pts scored was season: "+str(regular_stats[3])+" with a total of "+str(regular_stats[1])+" points")
    print("Season with less pts scored was season: "+str(regular_stats[4])+" with a total of "+str(regular_stats[2])+" points")
    print("Average total pts in Regular Season was: "+str(regular_stats[5]))
    print("Average total assists in Regular Season was: "+str(regular_stats[6]))
    print("Average total rebounds in Regular Season was: "+str(regular_stats[7]))
    # getting the stats from post season and storing in post_season_stats
    post_season_stats = post_stats()
    # calling post_regular_function giving stats from regular and post season as parameters and storing in better_in_post_season
    better_in_post_season = post_regular_comparison(regular_stats[0], post_season_stats)
    print(better_in_post_season)