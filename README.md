# hse_msds_ml_project
## Required packages
This bot requires Python < 3.8. Upon Python this bot requires rasa and nba_api packages to be installed in order to work.

## Starting the bot
This bot needs 2 servers, so 2 commands should be executed, one is for a bot itself and one is for custom actions:

```rasa shell```
```rasa run action```

## Bot abilities

The bot can tell a user the most recent result for an NBA team the user asks. It can also tell the user the most recent result of a game between 2 NBA teams. If the user greets the bot, it greets the user back and offers her to ask it about a game. When the result is provided, the bot offers to ask more about the game. Possible questions are:
- stats leaders
- points scored
- assists made
- rebounds collected

## How the bot works:

The bot uses well-documented RASA features: stories and forms. Custom actions are written in actions/actions.py and are executed on the action server mentioned earlier. All actions and intents are specified in the domain YML file.

To send requests about the game this bot uses nba_api package: https://github.com/swar/nba_api/. It is a Python library to send requests to stats.nba.com. Actions utilize two requests:
- leaguegamefinder.LeagueGameFinder to fetch games (accepts 1 or 2 teams as arguments). This function returns a list of games. The first element of this list is chosen customly;
- boxscoretraditionalv2.BoxScoreTraditionalV2 to fetch box scores given game id (set in the previous step). Specific information (points, assists, etc.) is extracted customly.
