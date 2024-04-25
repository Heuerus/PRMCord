from main_gitversion import cursor
from random import randint


async def matchup(team1,team2):
    winners = []

    cursor.execute("SELECT toplaner, jungler, midlaner, adc, supporter, coach1, coach2, fantasyname, elo, buff FROM fantasy WHERE discord_id = %s", (team1,))
    team1 = cursor.fetchone()
    cursor.execute("SELECT toplaner, jungler, midlaner, adc, supporter, coach1, coach2, fantasyname, elo, buff FROM fantasy WHERE discord_id = %s", (team2,))
    team2 = cursor.fetchone()

    async def get_pos_info(pos, team):
        cursor.execute("SELECT teamname,div24sp FROM teams WHERE %s = %s", (pos, team))
        return cursor.fetchone()

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

    def div_check(div, Divisions = { 1 : 160, 2 : 80, 3 : 40, 4 : 20, 5 : 10, 6 : 5, None : 0}):
        return Divisions[div]

    def headcoach_buff(div, Headcoaches = { 1 : 2.0, 2 : 1.75, 3 : 1.5, 4 : 1.25, 5 : 1.15, 6 : 1.1, None : 0}): 
        return Headcoaches[div]
    
    def asscoach_buff(div, Asscoaches = { 1 : 1.4, 2 : 1.3, 3 : 1.2, 4 : 1.1, None : 0}):
        return Asscoaches[div]

    def player_value_base(player_info, position, buffed_position, headcoach_info, asscoach_info, top_info, jungle_info, mid_info, adc_info, sup_info):
        value = div_check(player_info[1])
        value = round(value * headcoach_buff(headcoach_info[1]))
        if jungle_info[0] == top_info[0] and mid_info[0] == top_info[0] and adc_info[0] == top_info[0] and sup_info[0] == top_info[0]: #team buff
            value = round(value * 1.5)
        if buffed_position == position: #asscoach buff
            value = round(value * asscoach_buff(asscoach_info[1]))
        if (( position == "jgl" or position == "mid" ) and  jungle_info[0] == mid_info[0]) or (( position == "adc" or position == "sup" ) and adc_info[0] == sup_info[0]): #synergy buffs
            value = round(value * 1.25)
        print("Value: ", value)
        return value
    
    def player_value(player_info, position, team):
        print("Team: ", team, "Position: ", position, "Playerdiv: ", player_info[1])
        if team == 1:
            return player_value_base(player_info, position, buffed_position = team1[9], headcoach_info = headcoach_1_info, asscoach_info = asscoach_1_info, top_info = toplane_1_info, jungle_info = jungle_1_info, mid_info = midlane_1_info, adc_info = adc_1_info, sup_info = support_1_info)
        else:
            return player_value_base(player_info, position, buffed_position = team2[9], headcoach_info = headcoach_2_info, asscoach_info = asscoach_2_info, top_info = toplane_2_info, jungle_info = jungle_2_info, mid_info = midlane_2_info, adc_info = adc_2_info, sup_info = support_2_info)
    
    def compare_pos(pos1, pos2, pos):
        pool = player_value(pos1, pos, 1) + player_value(pos2, pos, 2)
        chance = randint(1, pool)
        if chance <= player_value(pos1, pos, 1):
            winners.append(team1[7])
        else:
            winners.append(team2[7])

    compare_pos(toplane_1_info, toplane_2_info, "top")
    compare_pos(jungle_1_info, jungle_2_info, "jgl")
    compare_pos(midlane_1_info, midlane_2_info, "mid")
    compare_pos(adc_1_info, adc_2_info, "adc")
    compare_pos(support_1_info, support_2_info, "sup")

    return winners