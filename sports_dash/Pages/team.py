import dash

dash.register_page(__name__, path="/team")
from dash.exceptions import PreventUpdate
from dash import dcc, html, Dash, Input, Output, dash_table, State, callback
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash_mantine_components as dmc


# Bring data into App
master_roster = pd.read_csv(
    r"C:\Users\kellya\Documents\Python Code\python_for_coaches-main\python_for_coaches-main\Learning\sports_dash\Full_FB_Roster.csv"
)
active_roster = master_roster[master_roster.active_status == True]
dfgps = pd.read_csv(
    r"C:\Users\kellya\Documents\Python Code\python_for_coaches-main\python_for_coaches-main\Learning\sports_dash\UWW_FB_GPS.csv"
)
dfp = pd.read_csv(
    r"C:\Users\kellya\Documents\Python Code\python_for_coaches-main\python_for_coaches-main\Learning\sports_dash\UWW_FB_PERFORMANCE_TESTING.csv"
)
weight_goal_data = pd.read_csv(
    r"C:\Users\kellya\Documents\Python Code\python_for_coaches-main\python_for_coaches-main\Learning\sports_dash\weight_goal_colors.csv"
)
team_wellness_df = pd.read_csv(
    r"C:\Users\kellya\Documents\Python Code\python_for_coaches-main\python_for_coaches-main\Learning\sports_dash\FB_Team_Wellness.csv"
)

# transform every unique date to a number
# numdate= [x for x in range(len(dfgps['Date'].unique()))]


# build your components
dbc_css = (
    "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.2/dbc.min.css"
)
app = dash.Dash(
    external_stylesheets=[dbc.themes.PULSE, dbc_css], 
    suppress_callback_exceptions=True, 
)
team_table_dropdown = dcc.Dropdown(
    id="team-table-dropdown",
    options=[{"label": x, "value": x} for x in dfp.columns],
    value=["Name", "Added Date", "Position"],
    multi=True,
)
team_table_active_status_dropdown = dcc.Dropdown(
    id="active_status_choice",
    options=["Active Players Only", "All Time Player Records"],
    value="Active Players Only",
)
gpsdropdown = dcc.Dropdown(
    id="gps_dropdown",
    options=["Hi Intensity Accels", "Distance Total (M)", "Sprints", "Max Speed (MPH)"],
    placeholder="Select a Metric",
)
gps_grouping_dropdown = dcc.Dropdown(
    id="gps_grouping_dropdown",
    options=["Team", "By Position", "By Individual"],
    placeholder="Select Team, Postion, or Individual View",
)
gps_subgrouping_dropdown = dcc.Dropdown(
    id="gps_subgrouping_dropdown", options=[], multi=False
)
gps_dateselection = dcc.Dropdown(
    id="gps_date_dropdown", options=[], placeholder="Select Event(s).", multi=True
)
gps_position_dropdown = dcc.Dropdown(id="gps_position_dropdown", options=[], multi=True)
gps_graph = dcc.Graph(id="gps_graph", figure={})
gps_active_status_dropdown = dcc.Dropdown(
    id="gps_active_status_choice",
    options=["Active Players Only", "All Time Player Records"],
    value="Active Players Only",
)
team_wellness_mixed = dcc.Graph(id="team_wellness_mixed_graph", figure={})
gps_games_or_practices = dcc.RadioItems(
    id="games_or_practices_radio",
    options=["Practice Data", "Game Data", "Both"],
    inputStyle={"margin-right": "2px", "margin-left": "5px"},
)
gps_year_selection = dcc.Dropdown(
    id="year_selection", options=[2021, 2022], multi=True, placeholder="Select Year(s)"
)
gps_season_selection = dcc.Dropdown(
    id="season_selection",
    options=["Fall", "Spring", "Preseason"],
    multi=True,
    placeholder="Select Season(s)",
)
gps_comparison_selection = dcc.Dropdown(
    id="gps_comparison",
    options=[
        {"label": "Week", "value": "Week"},
        {"label": "Practice Number", "value": "Practice_Number"},
        {"label": "Season/Year", "value": "season_year"},
        {"label": "Event Type", "value": "event_type"},
        {"label": "Uniform Worn", "value": "Uniform"},
        {"label": "Location", "value": "Location"},
        {"label": "Date", "value": "Date"},
    ],
    multi=False,
    placeholder="Select Data Comparison Style",
    clearable=True,
)


# Customize the layout

layout = layout = dbc.Container([
    dbc.Row([
        dbc.Col([html.H2(
        "Team Metrics",
        style={'text-align': 'center', 'padding':30})],
        {"size": 3, "offset": 9}),
        ]),
    dmc.Paper(children=[dbc.Row([dbc.Col(html.Div(dash_table.DataTable(
        weight_goal_data.to_dict('records'),
        sort_action='native',
        columns=[
            {'name': 'Name', 'id': 'Name', 'type': 'text', 'editable': False},
            {'name': 'Initial Weight', 'id': 'Initial Weight', 'type': 'numeric', 'editable': False},
            {'name': 'Week 2', 'id': 'Week 2', 'type': 'numeric', 'editable': False},
            {'name': 'Week 3', 'id': 'Week 3', 'type': 'numeric', 'editable': False},
            {'name': 'Week 4', 'id': 'Week 4', 'type': 'numeric', 'editable': False},
            {'name': 'Week 5', 'id': 'Week 5', 'type': 'numeric', 'editable': False},
            {'name': 'Week 6', 'id': 'Week 6', 'type': 'numeric', 'editable': False},
            {'name': 'Week 7', 'id': 'Week 7', 'type': 'numeric', 'editable': False},
            {'name': 'Week 8', 'id': 'Week 8', 'type': 'numeric', 'editable': False},
            {'name': 'Week 9', 'id': 'Week 9', 'type': 'numeric', 'editable': False},
            {'name': 'Week 10', 'id': 'Week 10', 'type': 'numeric', 'editable': False},
            {'name': 'Week 11', 'id': 'Week 11', 'type': 'numeric', 'editable': False},
            {'name': 'Week 12', 'id': 'Week 12', 'type': 'numeric', 'editable': False},
            {'name': 'December Goal', 'id': 'December Goal', 'type': 'numeric', 'editable': False},
        ],
        fixed_columns={'headers': True, 'data': 2},
        fixed_rows={'headers': True},
        page_action='native',
        filter_action='native',
        style_table={'minWidth': '100%'},
        style_header={'backgroundColor': '#9481A6','color': 'black', 'textAlign': 'center', 'width': 'auto'},
        style_data={'backgroundColor': 'white','color': 'black', 'height':'auto'},
        style_cell={'minWidth': 100,  'width': 'auto', 'height':'auto', 'textAlign': 'center'},
        style_data_conditional=(
            [
                # 'filter_query', 'column_id', 'column_type', 'row_index', 'state', 'column_editable'.
                # filter_query ****************************************
                {
                    'if': {
                        'filter_query': '{COLOR2} = black',
                        'column_id': 'Week 2'
                    },
                    'backgroundColor': '#111111',
                    'color': 'white'
                },
                                {
                    'if': {
                        'filter_query': '{COLOR3} = black',
                        'column_id': 'Week 3'
                    },
                    'backgroundColor': '#111111',
                    'color': 'white'
                },
                                {
                    'if': {
                        'filter_query': '{COLOR4} = black',
                        'column_id': 'Week 4'
                    },
                    'backgroundColor': '#111111',
                    'color': 'white'
                },
                                {
                    'if': {
                        'filter_query': '{COLOR5} = black',
                        'column_id': 'Week 5'
                    },
                    'backgroundColor': '#111111',
                    'color': 'white'
                },
                                {
                    'if': {
                        'filter_query': '{COLOR6} = black',
                        'column_id': 'Week 6'
                    },
                    'backgroundColor': '#111111',
                    'color': 'white'
                },
                                {
                    'if': {
                        'filter_query': '{COLOR7} = black',
                        'column_id': 'Week 7'
                    },
                    'backgroundColor': '#111111',
                    'color': 'white'
                },
                                {
                    'if': {
                        'filter_query': '{COLOR8} = black',
                        'column_id': 'Week 8'
                    },
                    'backgroundColor': '#111111',
                    'color': 'white'
                },
                                {
                    'if': {
                        'filter_query': '{COLOR9} = black',
                        'column_id': 'Week 9'
                    },
                    'backgroundColor': '#111111',
                    'color': 'white'
                },
                                {
                    'if': {
                        'filter_query': '{COLOR10} = black',
                        'column_id': 'Week 10'
                    },
                    'backgroundColor': '#111111',
                    'color': 'white'
                },
                                {
                    'if': {
                        'filter_query': '{COLOR11} = black',
                        'column_id': 'Week 11'
                    },
                    'backgroundColor': '#111111',
                    'color': 'white'
                },
                                {
                    'if': {
                        'filter_query': '{COLOR12} = black',
                        'column_id': 'Week 12'
                    },
                    'backgroundColor': '#111111',
                    'color': 'white'
                },
                                {
                    'if': {
                        'filter_query': '{COLOR13} = black',
                        'column_id': 'Week 13'
                    },
                    'backgroundColor': '#111111',
                    'color': 'white'
                },
                {
                    'if': {
                        'filter_query': '{COLOR2} = green',
                        'column_id': 'Week 2'
                    },
                    'backgroundColor': '#2ECC40',
                },
                                {
                    'if': {
                        'filter_query': '{COLOR3} = green',
                        'column_id': 'Week 3'
                    },
                    'backgroundColor': '#2ECC40',
                },
                                {
                    'if': {
                        'filter_query': '{COLOR4} = green',
                        'column_id': 'Week 4'
                    },
                    'backgroundColor': '#2ECC40',
                },
                                {
                    'if': {
                        'filter_query': '{COLOR5} = green',
                        'column_id': 'Week 5'
                    },
                    'backgroundColor': '#2ECC40',
                },
                                {
                    'if': {
                        'filter_query': '{COLOR6} = green',
                        'column_id': 'Week 6'
                    },
                    'backgroundColor': '#2ECC40',
                },
                                {
                    'if': {
                        'filter_query': '{COLOR7} = green',
                        'column_id': 'Week 7'
                    },
                    'backgroundColor': '#2ECC40',
                },
                                {
                    'if': {
                        'filter_query': '{COLOR8} = green',
                        'column_id': 'Week 8'
                    },
                    'backgroundColor': '#2ECC40',
                },
                                {
                    'if': {
                        'filter_query': '{COLOR9} = green',
                        'column_id': 'Week 9'
                    },
                    'backgroundColor': '#2ECC40',
                },
                                {
                    'if': {
                        'filter_query': '{COLOR10} = green',
                        'column_id': 'Week 10'
                    },
                    'backgroundColor': '#2ECC40',
                },
                                {
                    'if': {
                        'filter_query': '{COLOR11} = green',
                        'column_id': 'Week 11'
                    },
                    'backgroundColor': '#2ECC40',
                },
                                {
                    'if': {
                        'filter_query': '{COLOR12} = green',
                        'column_id': 'Week 12'
                    },
                    'backgroundColor': '#2ECC40',
                },
                                {
                    'if': {
                        'filter_query': '{COLOR13} = green',
                        'column_id': 'Week 13'
                    },
                    'backgroundColor': '#2ECC40',
                },
                {
                    'if': {
                        'filter_query': '{COLOR2} = yellow',
                        'column_id': 'Week 2'
                    },
                    'backgroundColor': '#FFDC00',
                },
                                {
                    'if': {
                        'filter_query': '{COLOR3} = yellow',
                        'column_id': 'Week 3'
                    },
                    'backgroundColor': '#FFDC00',
                },
                                {
                    'if': {
                        'filter_query': '{COLOR4} = yellow',
                        'column_id': 'Week 4'
                    },
                    'backgroundColor': '#FFDC00',
                },
                                {
                    'if': {
                        'filter_query': '{COLOR5} = yellow',
                        'column_id': 'Week 5'
                    },
                    'backgroundColor': '#FFDC00',
                },
                                {
                    'if': {
                        'filter_query': '{COLOR6} = yellow',
                        'column_id': 'Week 6'
                    },
                    'backgroundColor': '#FFDC00',
                },
                                {
                    'if': {
                        'filter_query': '{COLOR7} = yellow',
                        'column_id': 'Week 7'
                    },
                    'backgroundColor': '#FFDC00',
                },
                                {
                    'if': {
                        'filter_query': '{COLOR8} = yellow',
                        'column_id': 'Week 8'
                    },
                    'backgroundColor': '#FFDC00',
                },
                                {
                    'if': {
                        'filter_query': '{COLOR9} = yellow',
                        'column_id': 'Week 9'
                    },
                    'backgroundColor': '#FFDC00',
                },
                                {
                    'if': {
                        'filter_query': '{COLOR10} = yellow',
                        'column_id': 'Week 10'
                    },
                    'backgroundColor': '#FFDC00',
                },
                                {
                    'if': {
                        'filter_query': '{COLOR11} = yellow',
                        'column_id': 'Week 11'
                    },
                    'backgroundColor': '#FFDC00',
                },
                                {
                    'if': {
                        'filter_query': '{COLOR12} = yellow',
                        'column_id': 'Week 12'
                    },
                    'backgroundColor': '#FFDC00',
                },
                                {
                    'if': {
                        'filter_query': '{COLOR13} = yellow',
                        'column_id': 'Week 13'
                    },
                    'backgroundColor': '#FFDC00',
                },
                {
                    'if': {
                        'filter_query': '{COLOR2} = red',
                        'column_id': 'Week 2'
                    },
                    'backgroundColor': '#FF4136',
                },
                                {
                    'if': {
                        'filter_query': '{COLOR3} = red',
                        'column_id': 'Week 3'
                    },
                    'backgroundColor': '#FF4136',
                },
                                {
                    'if': {
                        'filter_query': '{COLOR4} = red',
                        'column_id': 'Week 4'
                    },
                    'backgroundColor': '#FF4136',
                },
                                {
                    'if': {
                        'filter_query': '{COLOR5} = red',
                        'column_id': 'Week 5'
                    },
                    'backgroundColor': '#FF4136',
                },
                {
                    'if': {
                        'filter_query': '{COLOR6} = red',
                        'column_id': 'Week 6'
                    },
                    'backgroundColor': '#FF4136',
                },
                {
                    'if': {
                        'filter_query': '{COLOR7} = red',
                        'column_id': 'Week 7'
                    },
                    'backgroundColor': '#FF4136',
                },
                {
                    'if': {
                        'filter_query': '{COLOR8} = red',
                        'column_id': 'Week 8'
                    },
                    'backgroundColor': '#FF4136',
                },
                {
                    'if': {
                        'filter_query': '{COLOR9} = red',
                        'column_id': 'Week 9'
                    },
                    'backgroundColor': '#FF4136',
                },
                {
                    'if': {
                        'filter_query': '{COLOR10} = red',
                        'column_id': 'Week 10'
                    },
                    'backgroundColor': '#FF4136',
                },
                {
                    'if': {
                        'filter_query': '{COLOR11} = red',
                        'column_id': 'Week 11'
                    },
                    'backgroundColor': '#FF4136',
                },
                {
                    'if': {
                        'filter_query': '{COLOR12} = red',
                        'column_id': 'Week 12'
                    },
                    'backgroundColor': '#FF4136',
                },
                {
                    'if': {
                        'filter_query': '{COLOR13} = red',
                        'column_id': 'Week 13'
                    },
                    'backgroundColor': '#FF4136',
                },
            ])
        )),style={'padding':20}, width={"size": 12})])], shadow="md", p="md", radius="md", withBorder=True),
    dmc.Space(h=30),
    dmc.Paper(children=[dbc.Row([dbc.Col(html.Div(html.P(children="Here are several interactive dropdown menus to build a custom graph of our available GPS Data. You can isolate specific practices, weeks, games, years and/or specific players, positions, etc.", style={'text-align': 'center'})), style={'padding': 10}, width={"size": 10},)]), 
    dbc.Row([dbc.Col(html.Div([gpsdropdown]), style={'padding': 10}, width={"size": 6})]),
    dbc.Row([dbc.Col(html.Div([gps_grouping_dropdown]), style={'padding': 10}, width={"size": 6})]),
    dbc.Row([dbc.Col(html.Div([gps_subgrouping_dropdown]), style={'padding': 10}, width={"size": 6}), dbc.Col(html.Div([gps_position_dropdown]), style={'padding': 10}, width={"size": 6})]),
    dbc.Row([dbc.Col(html.Div([gps_active_status_dropdown]), style={'padding': 10}, width={"size": 6})]),
    dbc.Row([dbc.Col(html.Div([gps_games_or_practices]), style={'padding': 10}, width={"size": 6})]),
    dbc.Row([dbc.Col(html.Div([gps_year_selection]), style={'padding': 10}, width={"size": 6}), dbc.Col(html.Div([gps_season_selection]), style={'padding': 10}, width={"size": 6})]),
    dbc.Row([dbc.Col(html.Div([gps_dateselection]), style={'padding': 10}, width={"size": 6})]),
    dbc.Row([dbc.Col(html.Div([gps_comparison_selection]), style={'padding': 10}, width={"size": 6})]),
    dbc.Row([dbc.Col(html.Div([html.Button("Update Graph", id="gps_button", n_clicks=0)]), style={'padding': 10}, width={"size": 5})]),
    dbc.Row([dbc.Col(html.Div([gps_graph], style={'padding': 20}), width={"size": 12})])], shadow="md", p="md", radius="md", withBorder=True),
    dmc.Space(h=30),
    dmc.Paper(children=[dbc.Row([dbc.Col(html.Div([team_wellness_mixed], style={'padding': 20}), width={"size": 12})])], shadow="md", p="md", radius="md", withBorder=True),
    dmc.Space(h=30),
    dmc.Paper(children=[dbc.Row([dbc.Col(html.Div([html.P(children="This next area allows you to view the performance testing of the entire team. First, you can choose if you want to see only the currently rostered athletes only OR you can view all-time athlete data. The below table has a lot of built in filtering functions.")]))]), dbc.Row([dbc.Col(html.Div([team_table_active_status_dropdown]), style={'padding': 10}, width={"size": 6})]),
    dbc.Row([dbc.Col(html.Div([team_table_dropdown]), style={'padding': 10}, width={"size": 12})]),
    dbc.Row([dbc.Col(html.Div([html.P(children="Please use the above dropdown menu to select which performance test(s) you want to view in the below table.", style={'text-align': 'center'})]))]),
    dbc.Row([dbc.Col(html.Div(dash_table.DataTable(
                id='team-datatable',
                fixed_rows={'headers': True},
                page_action='native',
                filter_action="native",
                sort_action="native",
                style_table={'overflowX': 'auto', 'height': '400'},
                style_header={'backgroundColor': '#9481A6','color': 'black'},
                style_data={'backgroundColor': 'white','color': 'black'},
                style_cell={'minWidth': 95, 'maxWidth': 95, 'width': 95},
                ),
                style={'padding':30}))],)], shadow="md", p="md", radius="md", withBorder=True),
    dmc.Space(h=30),
   ],
   className="dbc", fluid=False)


# Callbacks allow components to interact
@callback(
    Output("team-datatable", "data"),
    Output("team-datatable", "columns"),
    [Input("team-table-dropdown", "value"), Input("active_status_choice", "value")],
)
def update_performance_table(options_chosen, active_choice):
    if active_choice == "Active Players Only":
        filter_dfp = dfp[dfp["Name"].isin(active_roster["Name"].tolist())]
    else:
        filter_dfp = dfp

    return filter_dfp.to_dict("records"), [{"name": x, "id": x} for x in options_chosen]


@callback(
    Output("gps_subgrouping_dropdown", "options"),
    [
        Input("gps_grouping_dropdown", "value"),
        Input("gps_active_status_choice", "value"),
    ],
    prevent_initial_call=True,
)
def set_subgrouping_options(chosen_subgroup, active_choice):
    if chosen_subgroup is None:
        raise PreventUpdate
    elif chosen_subgroup == "Team":
        subgroup = ["Whole Team", "Offense vs. Defense"]
        return subgroup
    elif chosen_subgroup == "By Position":
        subgroup = ["Position vs. Position(s)", "Personnel within Position"]
        return subgroup
    elif chosen_subgroup == "By Individual":
        if active_choice == "Active Players Only":
            filter_dfgps = dfgps[dfgps["Name"].isin(active_roster["Name"].tolist())]
        else:
            filter_dfgps = dfgps
    subgroup = [{"label": x, "value": x} for x in filter_dfgps.Name.unique()]
    return subgroup


@callback(
    Output("gps_date_dropdown", "options"),
    [
        Input("games_or_practices_radio", "value"),
        Input("year_selection", "value"),
        Input("season_selection", "value"),
    ],
    prevent_initial_call=True,
)
def set_event_selection(selected_event_types, selected_year, selected_season):
    df = dfgps.copy()
    if selected_event_types is None:
        raise PreventUpdate
    elif selected_year is None:
        raise PreventUpdate
    elif selected_season is None:
        raise PreventUpdate
    elif selected_event_types == "Practice Data":
        df_events = (
            df.loc[(df["event_type"] == "Practice")]
            .loc[(df.Year.isin(selected_year))]
            .loc[(df.season.isin(selected_season))]
        )
        options = [{"label": "Select All", "value": "all_values"}] + [
            {"label": x, "value": x}
            for x in df_events.season_year_event_number.unique()
        ]
    elif selected_event_types == "Game Data":
        df_events = (
            df.loc[(df["event_type"] == "Game")]
            .loc[(df.Year.isin(selected_year))]
            .loc[(df.season.isin(selected_season))]
        )
        options = [{"label": "Select All", "value": "all_values"}] + [
            {"label": x, "value": x}
            for x in df_events.season_year_event_number.unique()
        ]
    elif selected_event_types == "Both":
        df_events = (
            df.loc[(df["event_type"] == "Practice") | (df["event_type"] == "Game")]
            .loc[(df.Year.isin(selected_year))]
            .loc[(df.season.isin(selected_season))]
        )
        options = [{"label": "Select All", "value": "all_values"}] + [
            {"label": x, "value": x}
            for x in df_events.season_year_event_number.unique()
        ]
    return options


@callback(
    Output("gps_active_status_choice", "style"),
    Input("gps_grouping_dropdown", "value"),
)
def set_posit_indiv_options1(chosen_group):
    if chosen_group == "By Individual":
        return {"display": "block"}
    elif chosen_group == "By Position":
        return {"display": "none"}
    elif chosen_group == "Team":
        return {"display": "none"}


@callback(
    Output("gps_comparison", "style"),
    Input("gps_grouping_dropdown", "value"),
    prevent_initial_call=True,
)
def set_posit_indiv_options2(chosen_group):
    if chosen_group is None:
        raise PreventUpdate
    elif chosen_group == "By Individual":
        return {"display": "none"}
    elif chosen_group == "By Position":
        return {"display": "none"}
    elif chosen_group == "Team":
        return {"display": "block"}


@callback(
    Output("gps_position_dropdown", "options"),
    Output("gps_position_dropdown", "style"),
    Input("gps_grouping_dropdown", "value"),
    prevent_initial_call=True,
)
def set_posit_indiv_options(chosen_group):
    if chosen_group is None:
        raise PreventUpdate
    elif chosen_group == "By Individual":
        subgroup = ["None"]
        return subgroup, {"display": "none"}
    elif chosen_group == "By Position":
        subgroup = [{"label": x, "value": x} for x in dfgps.Position.unique()]
        return subgroup, {"display": "block"}
    elif chosen_group == "Team":
        subgroup = ["None"]
        return subgroup, {"display": "none"}


@callback(
    Output("gps_graph", "figure"),
    [
        Input("gps_button", "n_clicks"),
        State(gpsdropdown, "value"),
        State(gps_grouping_dropdown, "value"),
        State(gps_subgrouping_dropdown, "value"),
        State("gps_position_dropdown", "value"),
        State("gps_date_dropdown", "value"),
        State("games_or_practices_radio", "value"),
        State("season_selection", "value"),
        State(gps_comparison_selection, "value"),
        State("year_selection", "value"),
    ],
    prevent_initial_call=True,
)
def update_gps_graph(
    n,
    metric_selection,
    group_select,
    subgroup_select,
    position_select,
    date_select,
    event_type_filter,
    selected_season,
    comparison_selection,
    year_selected,
):
    df = dfgps.copy()
    if date_select == ["all_values"]:
        if event_type_filter == "Practice Data":
            df_events = (
                df.loc[(df["event_type"] == "Practice")]
                .loc[(df.participation_status == "full")]
                .loc[(df.Year.isin(year_selected))]
                .loc[(df.season.isin(selected_season))]
            )
        elif event_type_filter == "Game Data":
            df_events = (
                df.loc[(df["event_type"] == "Game")]
                .loc[(df.participation_status == "full")]
                .loc[(df.Year.isin(year_selected))]
                .loc[(df.season.isin(selected_season))]
            )
        elif event_type_filter == "Both":
            df_events = (
                df.loc[(df["event_type"] == "Practice") | (df["event_type"] == "Game")]
                .loc[(df.participation_status == "full")]
                .loc[(df.Year.isin(year_selected))]
                .loc[(df.season.isin(selected_season))]
            )
        df = df_events
    else:
        df = df.loc[df["season_year_event_number"].isin(date_select)]
    if group_select == "Team" and subgroup_select == "Whole Team":
        fig = px.violin(
            df,
            x=f"{metric_selection}",
            y=f"{comparison_selection}",
            color=f"{comparison_selection}",
            box=False,
            points="all",
            hover_data=df.columns,
        )
        fig.update_traces(
            orientation="h",
            side="positive",
            width=2,
            points=False,
            meanline_visible=True,
        )
        fig.update_layout(xaxis_showgrid=False, xaxis_zeroline=False)
        return fig
    elif group_select == "Team" and subgroup_select == "Offense vs. Defense":
        fig = px.violin(
            df,
            x=f"{metric_selection}",
            y=f"{comparison_selection}",
            color="Side",
            box=False,
            points="all",
            hover_data=df.columns,
        )
        fig.update_traces(
            orientation="h",
            side="positive",
            width=2,
            points=False,
            meanline_visible=True,
        )
        fig.update_layout(xaxis_showgrid=False, xaxis_zeroline=False)
        return fig
    elif (
        group_select == "By Position" and subgroup_select == "Position vs. Position(s)"
    ):
        dff = df.loc[df["Position"].isin(position_select)]
        fig = px.violin(
            dff,
            x=f"{metric_selection}",
            y="Position",
            color="Position",
            box=False,
            points="all",
            hover_data=df.columns,
        )
        fig.update_traces(
            orientation="h",
            side="positive",
            width=2,
            points=False,
            meanline_visible=True,
        )
        fig.update_layout(xaxis_showgrid=False, xaxis_zeroline=False)
        return fig
    elif (
        group_select == "By Position" and subgroup_select == "Personnel within Position"
    ):
        dff = df.loc[(df["Position"].isin(position_select))]
        fig = px.violin(
            dff,
            x=f"{metric_selection}",
            y="Name",
            color="Name",
            box=False,
            points="all",
            hover_data=dff.columns,
        )
        fig.update_traces(
            orientation="h",
            side="positive",
            width=2,
            points=False,
            meanline_visible=True,
        )
        fig.update_layout(xaxis_showgrid=False, xaxis_zeroline=False)
        return fig
    elif group_select == "By Individual":
        dff = df.loc[(df["Name"] == subgroup_select)]
        fig = px.bar(
            dff,
            x="Date",
            y=f"{metric_selection}",
            color=f"{metric_selection}",
            hover_data=dff.columns,
        )
        return fig


@callback(
    Output("team_wellness_mixed_graph", "figure"),
    Input("active_status_choice", "value"),
)
def update_team_wellness_graph(status):
    df = team_wellness_df
    # fig2 = status
    fig = make_subplots()

    fig.add_trace(
        go.Bar(
            x=df.Date, y=df["Energy Level"], marker_color="#9481A6", name="Energy Level"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df.Date,
            y=df["Overall Lower Body Soreness"],
            name="Lower Body Soreness",
            mode="lines+markers",
            line_color="#331A4D",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df.Date,
            y=df["Overall Upper Body Soreness"],
            name="Upper Body Soreness",
            mode="lines+markers",
            line_color="#D9C15F",
            line_dash="dot",
        )
    )

    fig.update_layout(
        template="ggplot2",
        title=("Team's Average Energy Level x Soreness"),
        xaxis_title="Date",
        yaxis_title="Score",
        legend_title="Legend",
    )
    fig.update_layout(yaxis_range=[0, 10])
    fig.update_layout(
        legend=dict(orientation="h", yanchor="top", y=-0.6, xanchor="center", x=0.5)
    )
    return fig
