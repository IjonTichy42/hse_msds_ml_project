from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguegamefinder, playbyplayv2, boxscoretraditionalv2
from rasa_sdk.events import SlotSet

def team_id_by_name(name):
    return [team for team in nba_teams if (name.lower() in team["full_name"].lower()) or (name.lower() in team["abbreviation"].lower())][0]["id"]

nba_teams = teams.get_teams()

class ActionLatestGame(Action):
    
    def name(self) -> Text:
        return "action_team_latest_game"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        name = tracker.slots["team_1"]
        if [team for team in nba_teams if (name.lower() in team["full_name"].lower()) or (name.lower() in team["abbreviation"])]:
            id = team_id_by_name(name)
            gamefinder = leaguegamefinder.LeagueGameFinder(team_id_nullable=id)
            games = gamefinder.get_data_frames()[0]
            game = games.iloc[0]

            dispatcher.utter_message(game["MATCHUP"] + " " + game["GAME_DATE"] + " " + str(game["PTS"]) + "-" + str(int((game["PTS"] - game["PLUS_MINUS"]))))
            dispatcher.utter_message("I can tell you more about this game. Ask me about stats")
        else:
            dispatcher.utter_message("Sorry, I don't know such team!")
            return []
        
        return [SlotSet("game_id", game["GAME_ID"]), SlotSet("team_1", None)]
    
class ActionLatestMatchUp(Action):
    
    def name(self) -> Text:
        return "action_latest_match_up"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        team_1 = tracker.slots["team_1"]
        team_2 = tracker.slots["team_2"]
        
        if [team for team in nba_teams if (team_1.lower() in team["full_name"].lower()) or (team_1.lower() in team["abbreviation"])] and [team for team in nba_teams if (team_2.lower() in team["full_name"].lower()) or (team_2.lower() in team["abbreviation"])]:
            team_1_id = team_id_by_name(team_1)
            team_2_id = team_id_by_name(team_2)
            if team_1_id == team_2_id:
                dispatcher.utter_message("Please enter different teams")
                return [SlotSet("team_1", None), SlotSet("team_2", None)]
            gamefinder = leaguegamefinder.LeagueGameFinder(team_id_nullable=team_1_id, vs_team_id_nullable = team_2_id)
            games = gamefinder.get_data_frames()[0]
            game = games.iloc[0]

            dispatcher.utter_message(game["MATCHUP"] + " " + game["GAME_DATE"] + " " + str(game["PTS"]) + "-" + str(int((game["PTS"] - game["PLUS_MINUS"]))))
            dispatcher.utter_message("I can tell you more about this game. Ask me about stats")
        else:
            dispatcher.utter_message("Sorry, I don't know such team!")
            return []

        return [SlotSet("game_id", game["GAME_ID"]), SlotSet("team_1", None), SlotSet("team_2", None)]
    
class GetStatsLeaders(Action):
    
    def name(self) -> Text:
        return "action_get_stats_leaders"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        game_id = tracker.slots["game_id"]
        stats = ['PTS', 'AST', 'REB', 'STL', 'BLK']
        bs = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id).get_data_frames()[0]
        teams = bs["TEAM_ABBREVIATION"].unique()
        
        for team in teams:
            dispatcher.utter_message(team)
            team_stats = bs[bs["TEAM_ABBREVIATION"] == team]
            for stat in stats:
                player = team_stats.iloc[team_stats[stat].argmax()]
                dispatcher.utter_message(player["PLAYER_NAME"] + ': ' + str(player[stat]) + ' ' + stat)
                
        return []

class GetScorers(Action):
    
    def name(self) -> Text:
        return "action_get_scorers"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        game_id = tracker.slots["game_id"]
        bs = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id).get_data_frames()[0]
        
        for player in bs.iloc:
            dispatcher.utter_message(player["PLAYER_NAME"] + ' ' + player["TEAM_ABBREVIATION"] + ' ' + str(player["PTS"]) + " pts")
                
        return []

class GetAssists(Action):
    
    def name(self) -> Text:
        return "action_get_assists"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        game_id = tracker.slots["game_id"]
        bs = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id).get_data_frames()[0]
        
        for player in bs.iloc:
            dispatcher.utter_message(player["PLAYER_NAME"] + ' ' + player["TEAM_ABBREVIATION"] + ' ' + str(player["AST"]) + " assists")
                
        return []

class GetRebounds(Action):
    
    def name(self) -> Text:
        return "action_get_rebounds"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        game_id = tracker.slots["game_id"]
        bs = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id).get_data_frames()[0]
        
        for player in bs.iloc:
            dispatcher.utter_message(player["PLAYER_NAME"] + ' ' + player["TEAM_ABBREVIATION"] + ' ' + str(player["REB"]) + " rebounds")
                
        return []



