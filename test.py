from main_gitversion import cursor
from random import randint

async def get_pos_info(pos, team):
    cursor.execute("SELECT teamname,div24sp FROM teams WHERE %s = %s", (pos, team))
    return cursor.fetchone()

async def matchup(team1,team2):
    winners = []

    cursor.execute("SELECT toplaner, jungler, midlaner, adc, supporter, coach1, coach2, fantasyname, elo, buff FROM fantasy WHERE discord_id = %s", (team1,))
    team1 = cursor.fetchone()
    cursor.execute("SELECT toplaner, jungler, midlaner, adc, supporter, coach1, coach2, fantasyname, elo, buff FROM fantasy WHERE discord_id = %s", (team2,))
    team2 = cursor.fetchone()


    #pos info
    toplane_1_info = await get_pos_info("toplaner", team1[0])
    toplane_2_info = await get_pos_info("toplaner", team2[0])

    jungle_1_info = await get_pos_info("jungler", team1[1])
    jungle_2_info = await get_pos_info("jungler", team2[1])

    midlane_1_info = await get_pos_info("midlaner", team1[2])
    midlane_2_info = await get_pos_info("midlaner", team2[2])

    adc_1_info = await get_pos_info("adc", team1[3])
    adc_2_info = await get_pos_info("adc", team2[3])

    support_1_info = await get_pos_info("supporter", team1[4])
    support_2_info = await get_pos_info("supporter", team2[4])

    headcoach_1_info = await get_pos_info("headcoach", team1[5])
    headcoach_2_info = await get_pos_info("headcoach", team2[5])

    asscoach_1_info = await get_pos_info("asscoach", team1[6])
    asscoach_2_info = await get_pos_info("asscoach", team2[6])

    teambuff1 = False
    teambuff2 = False
    mid_jungle1 = False
    mid_jungle2 = False
    duo_bot1 = False
    duo_bot2 = False

    #asscoach buff
    buffed_position1 = team1[9]
    buffed_position2 = team2[9]

    #teambuff1
    team_check = toplane_1_info[0]
    if jungle_1_info[0] == team_check and midlane_1_info[0] == team_check and adc_1_info[0] == team_check and support_1_info[0] == team_check:
        teambuff1 = True
    #teambuff2
    team_check = toplane_2_info[0]
    if jungle_2_info[0] == team_check and midlane_2_info[0] == team_check and adc_2_info[0] == team_check and support_2_info[0] == team_check:
        teambuff2 = True
    
    #mid_jungle_duo1
    if jungle_1_info[0] == midlane_1_info[0]:
        mid_jungle1 = True
    #mid_jungle_duo2
    if jungle_2_info[0] == midlane_2_info[0]:
         mid_jungle2 = True

    #bot_duo1
    if adc_1_info[0] == support_1_info[0]:
        duo_bot1 = True
    #bot_duo2
    if adc_2_info[0] == support_2_info[0]:
        duo_bot2 = True
        
    def div_check(div):
        value = 0
        if div == 1:
            value = 160
        elif div == 2:
            value = 80
        elif div == 3:
            value = 40
        elif div == 4:
            value = 20
        elif div == 5:
            value = 10
        elif div == 6:
            value = 5
        return value

    def headcoach_buff(div):
        value = 0.0
        if div == 1:
            value = 2.0
        elif div == 2:
            value = 1.75
        elif div == 3:
            value = 1.5
        elif div == 4:
            value = 1.25
        elif div == 5:
            value = 1.15
        elif div == 6:
            value = 1.1
        return value
    
    def asscoach_buff(div):
        value = 0.0
        if div == 1:
            value = 1.4
        if div == 2:
            value = 1.3
        elif div == 3:
            value = 1.2
        elif div == 4:
            value = 1.1
        return value

    def player_value(player_info, headcoach_info, asscoach_info, teambuff, buffed_position, position):
        value = div_check(player_info[1])
        value = round(value * headcoach_buff(headcoach_info[1]))
        if teambuff == True:
            value = round(value * 1.5)
        if buffed_position == position:
            value = round(value * asscoach_buff(asscoach_info[1]))
        # mid jungl and adc supp buff
        return value

    def top_value(team):
        if team == 1:
            div = toplane_1_info[1]
        else:
            div = toplane_2_info[1]
        value = div_check(div)
        if team == 1:
            value = round(value * headcoach_buff(headcoach_1_info[1]))
            if teambuff1 == True:
                value = round(value * 1.5)
            if buffed_position1 == "top":
                value = round(value * asscoach_buff(asscoach_1_info[1]))
        else:
            if teambuff2 == True:
                round(value * headcoach_buff(headcoach_2_info[1]))
                value = round(value * 1.5)
            if buffed_position2 == "top":
                value = round(value * asscoach_buff(asscoach_2_info[1]))
        return value           

    def jgl_value(team):
        if team == 1:
            div = jungle_1_info[1]   # Div von jgl holen
        else:
            div = jungle_2_info[1]   # Div von jgl holen
        value = div_check(div)      # Je nach div value geben
        if team == 1:
            value = round(value * headcoach_buff(headcoach_1_info[1]))    # coach buff verrechenn
            if teambuff1 == True:                          # team buff verrechnen
                value = round(value * 1.5)
            elif mid_jungle1 == True:                      # synergy buff verrechnen
                value = round(value * 1.25)
            if buffed_position1 == "jgl":
                value = round(value * asscoach_buff(asscoach_1_info[1]))
        else:
            value = round(value * headcoach_buff(headcoach_2_info[1]))
            if teambuff2 == True:
                value = round(value * 1.5)
            elif mid_jungle2 == True:
                value = round(value * 1.25) 
            if buffed_position1 == "jgl":
                value = round(value * asscoach_buff(asscoach_2_info[1]))
        return value    

    def mid_value(team):
        if team == 1:
            div = midlane_1_info[1]
        else:
            div = midlane_2_info[1]
        value = div_check(div)
        if team == 1:
            value = round(value * headcoach_buff(headcoach_1_info[1]))
            if teambuff1 == True:
                value = round(value * 1.5)
            elif mid_jungle1 == True:
                value = round(value * 1.25)
            if buffed_position1 == "mid":
                value = round(value * asscoach_buff(asscoach_1_info[1]))
        else:
            value = round(value * headcoach_buff(headcoach_2_info[1]))
            if teambuff2 == True:
                value = round(value * 1.5)
            elif mid_jungle2 == True:
                value = round(value * 1.25)
            if buffed_position1 == "mid":
                value = round(value * asscoach_buff(asscoach_2_info[1]))
        return value

    def adc_value(team):
        if team == 1:
            div = adc_1_info[1]
        else:
            div = adc_2_info[1]
        value = div_check(div)
        if team == 1:
            value = round(value * headcoach_buff(headcoach_1_info[1]))
            if teambuff1 == True:
                value = round(value * 1.5)
            elif duo_bot1 == True:
                value = round(value * 1.25)
            if buffed_position1 == "adc":
                value = round(value * asscoach_buff(asscoach_1_info[1]))
        else:
            value = round(value * headcoach_buff(headcoach_2_info[1]))
            if teambuff2 == True:
                value = round(value * 1.5)
            elif duo_bot2 == True:
                    value = round(value * 1.25)
            if buffed_position1 == "adc":
                value = round(value * asscoach_buff(asscoach_2_info[1]))
        return value

    def sup_value(team):
        if team == 1:
            div = support_1_info[1]
        else:
            div = support_2_info[1]
        value = div_check(div)
        if team == 1:
            value = round(value * headcoach_buff(headcoach_1_info[1]))
            if teambuff1 == True:
                value = round(value * 1.5)
            elif duo_bot1 == True:
                value = round(value * 1.25)
            if buffed_position1 == "sup":
                value = round(value * asscoach_buff(asscoach_1_info[1]))
        else:
            value = round(value * headcoach_buff(headcoach_2_info[1]))
            if teambuff2 == True:
                value = round(value * 1.5)
            elif duo_bot2 == True:
                value = round(value * 1.25)
            if buffed_position1 == "sup":
                value = round(value * asscoach_buff(asscoach_2_info[1]))
        return value


    pool = top_value(1) + top_value(2)         # top matchup
    chance = randint(1, pool) 
    if chance <= top_value(1):
        winners.append(team1[7])
    else:
        winners.append(team2[7])  

    pool = jgl_value(1) + jgl_value(2)
    chance = randint(1, pool)                   # sup matchup
    if chance <= jgl_value(1):
        winners.append(team1[7])
    else:
        winners.append(team2[7])  

    pool = mid_value(1) + mid_value(2)
    chance = randint(1, pool)
    if chance <= mid_value(1):                  # sup matchup
        winners.append(team1[7])
    else:
        winners.append(team2[7])  

    pool = adc_value(1) + adc_value(2)
    chance = randint(1, pool)
    if chance <= adc_value(1):                  # sup matchup
        winners.append(team1[7])
    else:
        winners.append(team2[7])  

    pool = sup_value(1) + sup_value(2)
    chance = randint(1, pool)                  # sup matchup
    if chance <= sup_value(1):
        winners.append(team1[7])
    else:
        winners.append(team2[7]) 
    return winners