#!/usr/bin/python
# -*- coding: utf-8 -*-

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
from nba_api.stats.static import *
import nba

teamlist = teams.get_teams()
playerlist = players.get_players()

team_stats_totals = {}
team_stats_per_game = {}

player_stats_totals = {}
player_stats_per_game = {}
player_stats_per36 = {}

team_stats = {
    'GP': 'GAMES PLAYED',
    'WINS': 'WINS',
    'LOSSES': 'LOSSES',
    'WIN_PCT': 'WIN%',
    'CONF_RANK': 'CONFERENCE RANK',
    'DIV_RANK': 'DIVISION RANK',
   # 'PO_WINS',
   # 'PO_LOSSES',
    'FGM': 'FGM',
    'FGA': 'FGA',
    'FG_PCT': 'FG%',
    'FG3M': '3PM',
    'FG3A': '3PA',
    'FG3_PCT': '3P%',
    'FTM': 'FTM',
    'FTA': 'FTA',
    'FT_PCT': 'FT%',
    'OREB' : 'OREB',
    'DREB': 'DREB',
    'REB': 'REB',
    'AST': 'AST',
    'PF': 'PF',
    'STL': 'STL',
    'TOV' : 'TOV',
    'BLK' : 'BLK',
    'PTS': 'PTS',
    'PTS_RANK': 'PTS RANK'
}


player_stats = {
    'TEAM_ABBREVIATION': 'TEAM',
    'PLAYER_AGE':'AGE',
    'GP': 'GAMES PLAYED',
    'GS': 'GAMES STARTED',
    'MIN': 'MIN',
    'FGM': 'FGM',
    'FGA': 'FGA',
    'FG_PCT': 'FG%',
    'FG3M': '3PM',
    'FG3A': '3PA',
    'FG3_PCT': '3P%',
    'FTM': 'FTM',
    'FTA': 'FTA',
    'FT_PCT': 'FT%',
    'OREB': 'OREB',
    'DREB': 'DREB',
    'REB': 'REB',
    'AST': 'AST',
    'STL': 'STL',
    'BLK':'BLK',
    'TOV': 'TOV',
    'PF': 'PF',
    'PTS':'PTS'
}

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.RadioItems(id='teamplayer', options=[{'label': 'Team',
                   'value': 'team'}, {'label': 'Player',
                   'value': 'player'}], value='team',
                   labelStyle={'display': 'inline-block',
                   'margin-right': 10}),
    dcc.RadioItems(id='permode', options=[{'label': 'Per Game',
                   'value': 'PerGame'}, {'label': 'Totals',
                   'value': 'Totals'}], value='PerGame',
                   labelStyle={'display': 'inline-block',
                   'margin-right': 10}),

    html.Div([html.Label('Team', style={'margin-right':'10px'}),
            dcc.Dropdown(options=[{'label': i['full_name'], 'value': i['id']} for i in teamlist], style={'margin-right': '35px','display': 'inline-block', 'width':'300px'}),
            html.Label('Start Date', style={'display': 'inline-block', 'margin-right':'10px'}),
            dcc.Dropdown(options=[{'label':x, 'value': x} for x in range(1946, 2021)], style={'margin-right': '10px','display': 'inline-block', 'width':'150px'}),
            html.Label('End Date', style={'display': 'inline-block', 'margin-right':'10px'}),
            dcc.Dropdown(options=[{'label':x, 'value': x} for x in range(1946, 2021)],style={'margin-right': '35px','display': 'inline-block','width':'150px'})
            ], id='items'),
    html.Button('Add new player/team', id='add'),
    dcc.Checklist(id='stats', labelStyle={'margin-right': '30px', 'display': 'inline-block'},style={'width':'1250px', 'margin-top':'50px'}, value=[]),
    html.Button('Graph', id='graph_btn', style={'margin-top':'50px'}),
    html.Div(id='graphs'),
    ])


teamplayer = 'team'
counter = 1

@app.callback(
        Output('items','children'),
        [Input('add','n_clicks'),
        Input('teamplayer','value')],
        [State('items', 'children')]
        )
def addItem(n_clicks, selection, items):
    global teamplayer
    global counter
    ret = []
    if n_clicks == counter or selection != teamplayer:
        if (selection == "team"):
            if (teamplayer == "team"):
                counter += 1
                ret.append(html.Label('Team', style={'display':'block', 'margin-right':'10px'}))
                ret.append(dcc.Dropdown(options=[{'label': i['full_name'], 'value': i['id']} for i in teamlist], style={'margin-right': '35px','display': 'inline-block', 'width':'300px'}))
                ret.append(html.Label('Start Date', style={'display': 'inline-block', 'margin-right':'10px'}))
                ret.append(dcc.Dropdown(options=[{'label':x, 'value': x} for x in range(1946, 2021)], style={'margin-right': '10px','display': 'inline-block', 'width':'150px'}))
                ret.append(html.Label('End Date', style={'display': 'inline-block', 'margin-right':'10px'}))
                ret.append(dcc.Dropdown(options=[{'label':x, 'value': x} for x in range(1946, 2021)],style={'margin-right': '35px','display': 'inline-block','width':'150px'}))
                items = items + ret
            else:
                items = html.Div([html.Label('Team', style={'margin-right':'10px'}),
                        dcc.Dropdown(options=[{'label': i['full_name'], 'value': i['id']} for i in teamlist], style={'margin-right': '35px','display': 'inline-block', 'width':'300px'}),
                        html.Label('Start Date', style={'display': 'inline-block', 'margin-right':'10px'}),
                        dcc.Dropdown(options=[{'label':x, 'value': x} for x in range(1946, 2021)], style={'margin-right': '10px','display': 'inline-block', 'width':'150px'}),
                        html.Label('End Date', style={'display': 'inline-block', 'margin-right':'10px'}),
                        dcc.Dropdown(options=[{'label':x, 'value': x} for x in range(1946, 2021)],style={'margin-right': '35px','display': 'inline-block','width':'150px'})
                        ], id='items')
                teamplayer = "team"
        else:
            if (teamplayer == "player"):
                counter += 1
                ret.append(html.Label('Player', style={'display':'block', 'margin-right':'10px'}))
                ret.append(dcc.Dropdown(options=[{'label': i['full_name'], 'value': i['id']} for i in playerlist], style={'margin-right': '35px','display': 'inline-block', 'width':'300px'}))
                ret.append(html.Label('Start Date', style={'display': 'inline-block', 'margin-right':'10px'}))
                ret.append(dcc.Dropdown(options=[{'label':x, 'value': x} for x in range(1946, 2021)], style={'margin-right': '10px','display': 'inline-block', 'width':'150px'}))
                ret.append(html.Label('End Date', style={'display': 'inline-block', 'margin-right':'10px'}))
                ret.append(dcc.Dropdown(options=[{'label':x, 'value': x} for x in range(1946, 2021)],style={'margin-right': '35px','display': 'inline-block','width':'150px'}))
                items = items + ret
            else:
                items = html.Div([html.Label('Player', style={'margin-right':'10px'}),
                        dcc.Dropdown(options=[{'label': i['full_name'], 'value': i['id']} for i in playerlist], style={'margin-right': '35px','display': 'inline-block', 'width':'300px'}),
                        html.Label('Start Date', style={'display': 'inline-block', 'margin-right':'10px'}),
                        dcc.Dropdown(options=[{'label':x, 'value': x} for x in range(1946, 2021)], style={'margin-right': '10px','display': 'inline-block', 'width':'150px'}),
                        html.Label('End Date', style={'display': 'inline-block', 'margin-right':'10px'}),
                        dcc.Dropdown(options=[{'label':x, 'value': x} for x in range(1946, 2021)],style={'margin-right': '35px','display': 'inline-block','width':'150px'})
                        ], id='items')
                teamplayer = "player"
    return items



@app.callback(
         [Output('stats', 'options'),
          Output('stats', 'value')],
         [Input('teamplayer', 'value')]
         )
def setDropDown(selection):
    if selection == 'team':
        return ([{'label': team_stats[i], 'value': i} for i in team_stats.keys()],[])
    else:

        return ([{'label': player_stats[i], 'value': i} for i in player_stats.keys()],[])


@app.callback(
        Output('graphs', 'children'),
        [Input('graph_btn','n_clicks')],
        [State('items', 'children'),
        State('stats','value'),
        State('teamplayer', 'value'),
         State('permode', 'value')])
def graphStats(n_clicks, children, stat_list, selection, permode):
    if n_clicks is None:
        raise PreventUpdate
    else:
        ids = []
        start_dates = []
        end_dates = []
        dic = ''
        if (selection == 'team'):
            i = 1
            dic = team_stats
            while i < len(children):
                if "value" in children[i]['props'].keys() and "value" in children[i+2]['props'].keys() and "value" in children[i+4]['props'].keys():
                    ids.append(nba.Team(children[i]['props']['value'], permode))
                    start_dates.append(children[i+2]['props']['value'])
                    end_dates.append(children[i+4]['props']['value'])

                i += 6

        else:
            i = 1
            dic = player_stats
            while i < len(children):
                if "value" in children[i]['props'].keys() and "value" in children[i+2]['props'].keys() and "value" in children[i+4]['props'].keys():
                    ids.append(nba.Player(children[i]['props']['value'], permode))
                    start_dates.append(children[i+2]['props']['value'])
                    end_dates.append(children[i+4]['props']['value'])
                i += 6

        same_dates = True
        for i in range(len(start_dates)):
            if (len(start_dates) != len(end_dates) or start_dates[i] != start_dates[i-1] or end_dates[i] != end_dates[i-1]):
                same_dates = False
                break


        graphs = []
        for j in stat_list:
            traces = []
            for i in range(len(ids)):
                df = ids[i].get_stats(j, str(start_dates[i]), str(end_dates[i]))
                if same_dates == False:
                    traces.append(dict(x=(str(df.index)), y=df,
                                  name=ids[i].name, text=df.index))
                    typ = ''
                else:
                    traces.append(dict(x=df.index, y=df,
                                  name=ids[i].name))
                    typ = 'category'

            graphs.append(dcc.Graph(figure={'data': traces,
                              'layout': dict(xaxis={'title': 'Range', 'type': typ},
                              yaxis={'title': dic[j]}, title=dic[j],
                              showlegend=True)}))

        return html.Div(graphs)
if __name__ == '__main__':
    app.run_server(debug=True)

