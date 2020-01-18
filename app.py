#!/usr/bin/python
# -*- coding: utf-8 -*-

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output
from nba_api.stats.static import *
import nba

teamlist = teams.get_teams()
playerlist = players.get_players()
clicks = 0

team_stats = [
    't_TEAM_ID',
    't_TEAM_CITY',
    't_TEAM_NAME',
    't_YEAR',
    't_GP',
    't_WINS',
    't_LOSSES',
    't_WIN_PCT',
    't_CONF_RANK',
    't_DIV_RANK',
    't_PO_WINS',
    't_PO_LOSSES',
    't_CONF_COUNT',
    't_DIV_COUNT',
    't_NBA_FINALS_APPEARANCE',
    't_FGM',
    't_FGA',
    't_FG_PCT',
    't_FG3M',
    't_FG3A',
    't_FG3_PCT',
    't_FTM',
    't_FTA',
    't_FT_PCT',
    't_OREB',
    't_DREB',
    't_REB',
    't_AST',
    't_PF',
    't_STL',
    't_TOV',
    't_BLK',
    't_PTS',
    't_PTS_RANK',
    ]

player_stats = [
    'p_PLAYER_ID',
    'p_SEASON_ID',
    'p_LEAGUE_ID',
    'p_TEAM_ID',
    'p_TEAM_ABBREVIATION',
    'p_PLAYER_AGE',
    'p_GP',
    'p_GS',
    'p_MIN',
    'p_FGM',
    'p_FGA',
    'p_FG_PCT',
    'p_FG3M',
    'p_FG3A',
    'p_FG3_PCT',
    'p_FTM',
    'p_FTA',
    'p_FT_PCT',
    'p_OREB',
    'p_DREB',
    'p_REB',
    'p_AST',
    'p_STL',
    'p_BLK',
    'p_TOV',
    'p_PF',
    'p_PTS',
    ]

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.RadioItems(id='teamplayer', options=[{'label': 'Team',
                   'value': 'team'}, {'label': 'Player',
                   'value': 'player'}], value='team',
                   labelStyle={'display': 'inline-block',
                   'margin-right': 10}),
    dcc.Dropdown(id='drop1', multi=False),
    dcc.Dropdown(id='drop2', multi=False),
    dcc.Dropdown(id='drop3', multi=False),
    dcc.Checklist(id='stats', labelStyle={'margin-right': '10',
                  'display': 'inline-block'}, values=[]),
    html.Button('Graph', id='graph_btn'),
    html.Div(id='container'),
    ])


@app.callback(
        [Output('drop1', 'options'),
         Output('drop2', 'options'),
         Output('drop3', 'options'),
         Output('stats', 'options')],
         [Input('teamplayer', 'value')])
def setDropDown(selection):
    if selection == 'team':
        return ([{'label': i['full_name'], 'value': i['id']} for i in teamlist],
                [{'label': i['full_name'], 'value': i['id']} for i in teamlist],
                [{'label': i['full_name'], 'value': i['id']} for i in teamlist],
                [{'label': i[2:], 'value': i} for i in team_stats])
    else:

        return ([{'label': i['full_name'], 'value': i['id']} for i in playerlist],
                [{'label': i['full_name'], 'value': i['id']} for i in playerlist],
                [{'label': i['full_name'], 'value': i['id']} for i in playerlist],
                [{'label': i[2:], 'value': i} for i in player_stats])


@app.callback(
        Output('container', 'children'),
        [Input('graph_btn','n_clicks'),
         Input('drop1', 'value'),
         Input('drop2', 'value'),
         Input('stats','values'),
         Input('teamplayer', 'value')])
def graphStats(n_clicks, id, id2, stat_list, teamplayer):
    global clicks
    if n_clicks == clicks or n_clicks is None:
        raise PreventUpdate
    else:
        clicks += 1

        if (teamplayer == 'team'):
            id1 = nba.Team(id)
            id2 = nba.Team(id2)
        else:
            id1 = nba.Player(id)
            id2 = nba.Player(id2)

        objects = [id1, id2]
        graphs = []
        for j in stat_list:
            traces = []
            for i in objects:
                df = i.get_stats(j[2:], '1975', '2020')
                traces.append(dict(x=str(df.index), y=df,
                              name=i.name))

                graphs.append(dcc.Graph(id=j[2:], figure={'data': traces,
                              'layout': dict(xaxis={'title': 'Range'},
                              yaxis={'title': j[2:]}, title=j[2:],
                              showlegend=True)}))

        return html.Div(graphs)
if __name__ == '__main__':
    app.run_server(debug=True)

