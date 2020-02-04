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
clicks = 0
counter = 1
teamplayer = 'team'

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

team_stats.sort()

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

player_stats.sort()
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
            dcc.Dropdown(id='drop1',  options=[{'label': i['full_name'], 'value': i['id']} for i in teamlist], style={'margin-right': '35px','display': 'inline-block', 'width':'300px'}),
            html.Label('Start Date', style={'display': 'inline-block', 'margin-right':'10px'}),
            dcc.Dropdown(id='startdate1', options=[{'label':x, 'value': x} for x in range(1946, 2021)], style={'margin-right': '10px','display': 'inline-block', 'width':'150px'}),
            html.Label('End Date', style={'display': 'inline-block', 'margin-right':'10px'}),
            dcc.Dropdown(id='enddate1', options=[{'label':x, 'value': x} for x in range(1946, 2021)],style={'margin-right': '35px','display': 'inline-block','width':'150px'})
            ], id='items'),
    html.Button('Add new player/team', id='add'),
    dcc.Checklist(id='stats', labelStyle={'margin-right': '30px', 'display': 'inline-block'},style={'width':'1250px', 'margin-top':'50px'}, value=[]),
    html.Button('Graph', id='graph_btn', style={'margin-top':'50px'}),
    html.Div(id='container'),
    ])


@app.callback(
        Output('items','children'),
        [Input('add','n_clicks'),
        Input('teamplayer','value')],
        [State('items', 'children')]
        )
def addItem(n_clicks, selection, items):
    global counter
    global teamplayer
    counter += 1
    ret = []
    if n_clicks is None:
        raise PreventUpdate
    else:
        if (selection == "team"):
            if (teamplayer == "team"):
                ret.append(html.Label('Team', style={'display':'block', 'margin-right':'10px'}))
                ret.append(dcc.Dropdown(id='drop'+str(counter), options=[{'label': i['full_name'], 'value': i['id']} for i in teamlist], style={'margin-right': '35px','display': 'inline-block', 'width':'300px'}))
                ret.append(html.Label('Start Date', style={'display': 'inline-block', 'margin-right':'10px'}))
                ret.append(dcc.Dropdown(id='startdate'+str(counter), options=[{'label':x, 'value': x} for x in range(1946, 2021)], style={'margin-right': '10px','display': 'inline-block', 'width':'150px'}))
                ret.append(html.Label('End Date', style={'display': 'inline-block', 'margin-right':'10px'}))
                ret.append(dcc.Dropdown(id='enddate'+str(counter), options=[{'label':x, 'value': x} for x in range(1946, 2021)],style={'margin-right': '35px','display': 'inline-block','width':'150px'}))
                items = items + ret
            else:
                items = html.Div([html.Label('Team', style={'margin-right':'10px'}),
                        dcc.Dropdown(id='drop1', options=[{'label': i['full_name'], 'value': i['id']} for i in teamlist], style={'margin-right': '35px','display': 'inline-block', 'width':'300px'}),
                        html.Label('Start Date', style={'display': 'inline-block', 'margin-right':'10px'}),
                        dcc.Dropdown(id='startdate1', options=[{'label':x, 'value': x} for x in range(1946, 2021)], style={'margin-right': '10px','display': 'inline-block', 'width':'150px'}),
                        html.Label('End Date', style={'display': 'inline-block', 'margin-right':'10px'}),
                        dcc.Dropdown(id='enddate1', options=[{'label':x, 'value': x} for x in range(1946, 2021)],style={'margin-right': '35px','display': 'inline-block','width':'150px'})
                        ], id='items')
                teamplayer = 'team'
        else:
            if (teamplayer == "player"):
                ret.append(html.Label('Player', style={'display':'block', 'margin-right':'10px'}))
                ret.append(dcc.Dropdown(id='drop'+str(counter), options=[{'label': i['full_name'], 'value': i['id']} for i in playerlist], style={'margin-right': '35px','display': 'inline-block', 'width':'300px'}))
                ret.append(html.Label('Start Date', style={'display': 'inline-block', 'margin-right':'10px'}))
                ret.append(dcc.Dropdown(id='startdate'+str(counter), options=[{'label':x, 'value': x} for x in range(1946, 2021)], style={'margin-right': '10px','display': 'inline-block', 'width':'150px'}))
                ret.append(html.Label('End Date', style={'display': 'inline-block', 'margin-right':'10px'}))
                ret.append(dcc.Dropdown(id='enddate'+str(counter), options=[{'label':x, 'value': x} for x in range(1946, 2021)],style={'margin-right': '35px','display': 'inline-block','width':'150px'}))
                items = items + ret
            else:
                items = html.Div([html.Label('Player', style={'margin-right':'10px'}),
                        dcc.Dropdown(id='drop1', options=[{'label': i['full_name'], 'value': i['id']} for i in playerlist], style={'margin-right': '35px','display': 'inline-block', 'width':'300px'}),
                        html.Label('Start Date', style={'display': 'inline-block', 'margin-right':'10px'}),
                        dcc.Dropdown(id='startdate1', options=[{'label':x, 'value': x} for x in range(1946, 2021)], style={'margin-right': '10px','display': 'inline-block', 'width':'150px'}),
                        html.Label('End Date', style={'display': 'inline-block', 'margin-right':'10px'}),
                        dcc.Dropdown(id='enddate1', options=[{'label':x, 'value': x} for x in range(1946, 2021)],style={'margin-right': '35px','display': 'inline-block','width':'150px'})
                        ], id='items')
                teamplayer = 'player'
        return items


@app.callback(
         Output('stats', 'options'),
         [Input('teamplayer', 'value')]
         )
def setDropDown(selection):
    if selection == 'team':
        return ([{'label': i[2:], 'value': i} for i in team_stats])
    else:

        return ([{'label': i[2:], 'value': i} for i in player_stats])


@app.callback(
        Output('container', 'children'),
        [Input('graph_btn','n_clicks'),
         Input('items', 'children'),
         Input('stats','value')],
        [State('teamplayer', 'value'),
         State('permode', 'value')])
def graphStats(n_clicks, children, stat_list, selection, permode):
    global clicks
    if n_clicks == clicks or n_clicks is None:
        raise PreventUpdate
    else:
        clicks += 1
        ids = []
        start_dates = []
        end_dates = []
        if (selection == 'team'):
            i = 1
            while i < len(children):
                if "value" in children[i]['props'].keys() and "value" in children[i+2]['props'].keys() and "value" in children[i+4]['props'].keys():
                    ids.append(nba.Team(children[i]['props']['value'], permode))
                    start_dates.append(children[i+2]['props']['value'])
                    end_dates.append(children[i+4]['props']['value'])

                i += 6

        else:
            i = 1
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
                df = ids[i].get_stats(j[2:], str(start_dates[i]), str(end_dates[i]))
                if same_dates == False:
                    traces.append(dict(x=(str(df.index)), y=df,
                                  name=ids[i].name, text=df.index))
                    typ = ''
                else:
                    traces.append(dict(x=df.index, y=df,
                                  name=ids[i].name))
                    typ = 'category'

            graphs.append(dcc.Graph(id=j[2:], figure={'data': traces,
                              'layout': dict(xaxis={'title': 'Range', 'type': typ},
                              yaxis={'title': j[2:]}, title=j[2:],
                              showlegend=True)}))

        return html.Div(graphs)
if __name__ == '__main__':
    app.run_server(debug=True)

