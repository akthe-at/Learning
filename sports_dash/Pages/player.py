### Individual player focused page
import dash
from dash import dcc, html, Dash, Input, Output, dash_table, callback
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
from plotly.subplots import make_subplots
import dash_mantine_components as dmc
pd.options.mode.chained_assignment = None

dash.register_page(__name__, path="/")
pio.templates.default = "ggplot2"

# Bring data into App
bodyweight_df = pd.read_csv(r'C:\Users\kellya\Documents\Python Code\python_for_coaches-main\python_for_coaches-main\Learning\sports_dash\UWW FB SSI - Body Weights.csv')
weightload_df = pd.read_csv(r'C:\Users\kellya\Documents\Python Code\python_for_coaches-main\python_for_coaches-main\Learning\sports_dash\UWW_FB_WEIGHT_LOAD.csv')
hrvdf = pd.read_csv(r'C:\Users\kellya\Documents\Python Code\python_for_coaches-main\python_for_coaches-main\Learning\sports_dash\HRV_MASTER.csv')
master_roster = pd.read_csv(r'C:\Users\kellya\Documents\Python Code\python_for_coaches-main\python_for_coaches-main\Learning\sports_dash\Full_FB_Roster.csv')
wellness_df = pd.read_csv(r'C:\Users\kellya\Documents\Python Code\python_for_coaches-main\python_for_coaches-main\Learning\sports_dash\Wellness.csv')
active_roster = master_roster[master_roster.active_status == True]


# build your components
dbc_css = ("https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.2/dbc.min.css")
app = dash.Dash(external_stylesheets=[dbc.themes.PULSE, dbc_css])
status_radio = dcc.RadioItems(id='active_inactive_radio', options=['Active Players Only', 'All Time Player Records'], value='Active Players Only', inputStyle={"margin-right": "2px", "margin-left": "5px"})
hrvdropdown = dcc.Dropdown(id='hrv_dropdown', options=hrvdf.Name.unique(),placeholder="Please Select an Athlete",  maxHeight=500)
hrvgraph = dcc.Graph(id='hrv_graph', figure={})
rhrgraph = dcc.Graph(id='rhr_graph', figure={})
wellness_mixed = dcc.Graph(id='mixed_graph', figure={})

# Customize your own layout,
layout = dbc.Container([
    dbc.Row([
        dbc.Col([html.H2(
        "Individual Player Metrics",
        style={'text-align': 'center', 'padding':50})],
        {"size": 3, "offset": 9}),
        ]),
    dmc.Paper(children=[dbc.Row([dbc.Col([html.Div([status_radio], style={'padding':10, 'offset':4})], xs=12, sm=12, md=12, lg=6, xl=6)]),
    dmc.Space(h=30),
    dmc.Paper(children=[dbc.Row([dbc.Col([html.Div(id='weightgraph-dropdown-container', children=[], style={'padding':10, "align":"center"})], align="center", xs=12, sm=12, md=12, lg=6, xl=6)], align="center")], shadow="md", p="md", radius="md", withBorder=True),
    dbc.Row([dbc.Col([html.Div(id='body_weight_graph', children=[], style={'padding': 10})], xs=12, sm=12, md=12, lg=12, xl=12)])], shadow="md", p="md", radius="md", withBorder=True),
    dmc.Space(h=30),
    dmc.Paper(children=[dbc.Row([dbc.Col([html.H6("The graph below shows an athlete's relative load by session. This is calculated by multiplying weight lifted x total repetitions & sets and is then divided by bodyweight.", style={'padding':10, 'textalign': 'center'},)], xs=12, sm=12, md=12, lg=12, xl=12)]),
    dbc.Row([dbc.Col([html.Div(id="weightroom-load-graph", children=[], style={'padding': 10})], xs=12, sm=12, md=12, lg=12, xl=12)])], shadow="md", p="md", radius="md", withBorder=True),
    dmc.Space(h=30),
    dmc.Paper(children=[dbc.Row([dbc.Col([html.H6("The following graphs are based on survey questions given to each football player at every lifting session via the TeamBuildr App.", style={'padding':10, 'textalign': 'center'},)], xs=12, sm=12, md=12, lg=12, xl=12)]),
    dbc.Row([dbc.Col([html.Div([wellness_mixed], style={'padding': 10})], xs=12, sm=12, md=12, lg=12, xl=12)])], shadow="md", p="md", radius="md", withBorder=True),
    dmc.Space(h=30),
    dmc.Paper(children=[dbc.Row([dbc.Col([html.Div(id='wellness_graph3', children=[], style={'padding': 5})], xs=12, sm=12, md=12, lg=12, xl=6), dbc.Col([html.Div(id='wellness_graph4', children=[], style={'padding': 5})], xs=12, sm=12, md=12, lg=12, xl=6)])], shadow="md", p="md", radius="md", withBorder=True),
    dmc.Space(h=30),
    dmc.Paper(children=[dbc.Row([dbc.Col(html.Div(dash_table.DataTable(
                id='my-datatable',
                filter_action="native",
                sort_action="native",
                style_table={'overflowX': 'auto'},
                style_header={'backgroundColor': '#9481A6','color': 'black'},
                style_data={'backgroundColor': 'white','color': 'black'},
                ),style={'padding':20}), xs=12, sm=12, md=12, lg=12, xl=12,)])], shadow="md", p="md", radius="md", withBorder=True),
    dmc.Space(h=30),
    dmc.Paper(children=[dbc.Row([dbc.Col([html.H6('The dropdown menu below holds a list of all athletes that are tracking HRV data. The graph shows their HRV over time with the shaded range representing the "normal range" for the last 60 days of data. Each individual bar is the daily HRV score, and the line represents a 7-day rolling average. Ideally, the 7 day average line should stay within the shaded normal range to represent coping with training and life stimuli.', style={'padding':20, 'textalign': 'center'},)], xs=10, sm=10, md=10, lg=12, xl=12)]),
    dbc.Row([dbc.Col(html.Div([hrvdropdown]), style={'padding': 10}, xs=12, sm=12, md=12, lg=12, xl=12)]),
    dbc.Row([dbc.Col(html.Div([hrvgraph], style={'padding': 10}), xs=12, sm=12, md=12, lg=12, xl=12)]),
    dbc.Row([dbc.Col(html.Div([rhrgraph], style={'padding': 10}), xs=12, sm=12, md=12, lg=12, xl=12)])], shadow="md", p="md", radius="md", withBorder=True),
    ], className="dbc")


# Callbacks allow components to interact

@callback(
    Output("weightgraph-dropdown-container", "children"),
    Input("active_inactive_radio", "value"))

def populate_weightgraph_dropdownvalues(active_choice):
    df = bodyweight_df
    if active_choice == "Active Players Only":
       dff = df[df['Name'].isin(active_roster['Name'].tolist())]
    else:
        dff = df
    return dcc.Dropdown(
        id="dropdown_1",
        options=dff.Name.unique(),
        placeholder="Please Select an Athlete",
        clearable=False,
        persistence=True,
        persistence_type="session"
        ),


@callback(
    [Output("body_weight_graph", "children"),
    Output("store-dropdown-value", "data")],
    Input("dropdown_1", "value")
    )

def update_graph(column_name):
    bw_df = bodyweight_df.loc[(bodyweight_df['Name'] == column_name)]
    fig = px.line(data_frame=bw_df, x='Date', y=['Weight'],
    color_discrete_map={'Weight': "#5E308C"},
    markers=True,
    title=(f"{column_name}'s<br>Weight Progress<br>Over Time"),
    )
    fig.update_yaxes(title_text='Weight (lbs)')
    fig.add_scatter(x=bw_df['Date'], y=bw_df['Goal'], name="Weight Goal", mode='lines', line_color="green", line_dash="dot")
    fig.update_layout(legend_title_text='Legend')
    fig.update_xaxes(title_text='Date', type='category')
    fig.update_layout(legend=dict(
        orientation="h",
    yanchor="top",
    y=-0.6,
    xanchor="center",
    x=0.5
))
    return dcc.Graph(figure=fig), column_name


@callback(
    Output("weightroom-load-graph", "children"),
    Input("dropdown_1", "value")
    )

def update_graph2(selected_name):
    df = weightload_df.loc[(weightload_df['Name'] == selected_name)]
    bw_df = bodyweight_df.loc[(bodyweight_df['Name'] == selected_name)]
    avg_weight = bw_df['Weight'].mean()
    df['normalized_load'] = df['Volume_Load'].div(avg_weight).round(2)
    fig2 = px.bar(data_frame=df, x='Date',
    y='normalized_load',
    title=(f"{selected_name}'s<br>Weight Room Load<br>Per Session"),
    color='normalized_load',
    color_continuous_scale=px.colors.sequential.Turbo,
    )
    fig2.update_xaxes(title_text='Date')
    fig2.update_xaxes(title_text='Date', type='category')
    fig2.update_yaxes(title_text='Relative Load')
    fig2.update_layout(legend=dict(
        orientation="h",
    yanchor="top",
    y=-0.6,
    xanchor="center",
    x=0.5
))
    return dcc.Graph(figure=fig2)

@callback(
    Output('my-datatable', 'data'),
    Output('my-datatable', 'columns'),
    [Input("store-dropdown-value", "data"), Input('stored-performance-data', 'data')]
    )

def update_performance_table(selected_value, data):
    dfp = pd.DataFrame(data)
    df = dfp.loc[(dfp['Name'] == selected_value)]

    return df.to_dict('records'), [
        {'name': x, 'id': x} for x in df]


@callback(
    Output('hrv_graph', 'figure'),
    Input(hrvdropdown, 'value')
    )

def update_hrv_graph(column_name3):
    hrvdff = hrvdf.loc[(hrvdf['Name'] == column_name3)]
    hrvdff['date'] = hrvdff['date'].str[0:10]
    hrvdff['date'] = pd.to_datetime(hrvdff['date'])
    hrvdff['date'] = hrvdff['date'].dt.strftime('%Y-%m-%d')
    clrs = hrvdff['clrs']
    fig3 = make_subplots()

    fig3.add_trace(go.Scatter(x=hrvdff['date'],
    y=hrvdff['HRV Lower Limit'], name="Lower Limit of Normal Range",
    mode="lines", line_color="rgba(202,228,227,.6)"))

    fig3.add_trace(go.Scatter(x=hrvdff['date'],
    y=hrvdff['HRV Upper Limit'], name="Upper Limit of Normal Range",
    mode="lines", line_color="rgba(202,228,227,.6)", fill='tonexty',
    fillcolor='rgba(202,228,227,.6)' ))

    fig3.add_trace(go.Bar(x=hrvdff['date'], y=hrvdff['rMSSD'], marker_color=clrs,
    name="Daily HRV Score"))

    fig3.add_trace(go.Scatter(x=hrvdff['date'], y=hrvdff['rmssd7'],
    name="7 Day HRV Average", mode="lines", line_color="#1A78B5"))

    fig3.update_layout(
        template="plotly_dark",
        title=(f"{column_name3}'s Heart Rate Variability"),
        xaxis_title="Date",
        yaxis_title="HRV(rMSSD)",
        legend_title="Legend",)
    fig3.update_layout(legend=dict(
        orientation="h",
        yanchor="top",
        y=-0.6,
        xanchor="center",
        x=0.5
        ))
    return fig3

@callback(
    Output('rhr_graph', 'figure'),
    Input(hrvdropdown, 'value')
    )

def update_rhr_graph(column_name3):
    hrvdff = hrvdf.loc[(hrvdf['Name'] == column_name3)]
    hrvdff['date'] = hrvdff['date'].str[0:10]
    hrvdff['date'] = pd.to_datetime(hrvdff['date'])
    hrvdff['date'] = hrvdff['date'].dt.strftime('%Y-%m-%d')
    fig4 = make_subplots()

    fig4.add_trace(go.Scatter(x=hrvdff['date'],
    y=hrvdff['RHR Lower Limit'], name="Lower Limit of Normal Range",
    mode="lines", line_color="rgba(202,228,227,.65)"))

    fig4.add_trace(go.Scatter(x=hrvdff['date'],
    y=hrvdff['RHR Upper Limit'], name="Upper Limit of Normal Range",
    mode="lines", line_color="rgba(202,228,227,.65)", fill='tonexty',
    fillcolor="rgba(202,228,227,.65)"))

    fig4.add_trace(go.Bar(x=hrvdff['date'], y=hrvdff['HR'],marker_color='#54BFB5',
    name="Daily Resting HR"))

    fig4.add_trace(go.Scatter(x=hrvdff['date'], y=hrvdff['rhr7'],
    name="7 Day RHR Average", mode="lines", line_color="#1A78B5"))

    fig4.update_layout(
        template="plotly_dark",
        title=(f"{column_name3}'s Resting Heart Rate"),
        xaxis_title="Date",
        yaxis_title="Resting Heart Rate (bpm)",
        legend_title="Legend",)
    fig4.update_layout(yaxis_range=[30,90])
    fig4.update_layout(legend=dict(
        orientation="h",
        yanchor="top",
        y=-0.6,
        xanchor="center",
        x=0.5
        ))
    return fig4

@callback(
    Output('mixed_graph', 'figure'), Input("dropdown_1", "value") , prevent_initial_call=True
    )

def update_wellness5(selected_name):
    df = wellness_df.loc[(wellness_df['Name'] == selected_name)]
    fig = make_subplots()

    fig.add_trace(go.Bar(x=df['Date'], y=df['Energy Level'], marker_color='#9481A6',
    name="Energy Level"))

    fig.add_trace(go.Scatter(x=df['Date'],
    y=df['Overall Lower Body Soreness'], name="Lower Body Soreness",
    mode="lines+markers", line_color="#331A4D"))

    fig.add_trace(go.Scatter(x=df['Date'],
    y=df['Overall Upper Body Soreness'], name="Upper Body Soreness",
    mode="lines+markers", line_color="#D9C15F", line_dash="dot"))


    fig.update_layout(
        template="ggplot2",
        title=(f"{selected_name}'s Energy Level x Soreness"),
        xaxis_title="Date",
        yaxis_title="Score",
        legend_title="Legend",)
    fig.update_layout(yaxis_range=[0,10])
    fig.update_xaxes(title_text='Date', type='category')
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="top",
        y=-0.6,
        xanchor="center",
        x=0.5
        ))
    return fig

@callback(
    Output("wellness_graph1", "children"), Input("dropdown_1", "value") , prevent_initial_call=True
    )

@callback(
    Output("wellness_graph3", "children"), Input("dropdown_1", "value") , prevent_initial_call=True
    )

def update_wellness3(selected_name):
    df = wellness_df.loc[(wellness_df['Name'] == selected_name)]
    fig= px.line(
    data_frame=df,
    x='Date',
    y='Number of Meals in Last 24 Hours',
    title=("Number of Meals in Last 24 Hours"),
    markers=True
    )
    fig.update_xaxes(title_text='Date', type='category')
    fig.update_traces(line_color='#331A4D')
    return dcc.Graph(figure=fig)

@callback(
    Output("wellness_graph4", "children"), Input("dropdown_1", "value") , prevent_initial_call=True
    )

def update_wellness4(selected_name):
    df = wellness_df.loc[(wellness_df['Name'] == selected_name)]
    fig= px.line(
    data_frame=df,
    x='Date',
    y='Hours of Sleep in Last 24 Hours',
    title=("Hours of Sleep in Last 24 Hours"),
    markers=True
    )
    fig.update_xaxes(title_text='Date', type='category')
    fig.update_traces(line_color='#331A4D')
    return dcc.Graph(figure=fig)