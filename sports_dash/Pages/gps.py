import dash

dash.register_page(__name__, path="/gps")

from dash import dcc, html, Input, Output, dash_table, State, callback
import dash_bootstrap_components as dbc
import pandas as pd
import base64
import io
import datetime

ext_style = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
dbc_css = ("https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.2/dbc.min.css")
app = dash.Dash(external_stylesheets=[dbc.themes.PULSE, ext_style, dbc_css], suppress_callback_exceptions=True)


layout = dbc.Container([
    dbc.Row([dbc.Col(html.Div([html.Div([dcc.Upload(html.Button('Upload File'), id='upload-data', style={'padding': 10}, multiple=True)])], style={'padding': 10}), width={"size": 3})]),
    dbc.Row([dbc.Col(html.Div([html.Div(id='output-data-upload'),
    html.Div([html.Button("Download CSV", id="btn_csv"), dcc.Download(id="download-dataframe-csv")])]), width={"size": 3})]),
    ], className="dbc")

def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            global gps_df
            gps_df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
            if 'Hi Intensity Accels' in gps_df.columns:
                gps_df = gps_df[['AthleteName', 'Hi Intensity Accels', 'Distance Total', 'Group', 'Position', 'Date']]
                gps_df[['AthleteName', 'First Name']] = gps_df['AthleteName'].str.split(',',expand=True)
                gps_df['Name'] = gps_df['First Name'] + ' ' + gps_df['AthleteName']
                gps_df['Name'] = gps_df['Name'].str.lstrip()
                gps_df['Name'] = gps_df['Name'].str.rstrip()
                gps_df['Name'] = gps_df['Name'].str.replace('Tegan Christensen', 'Tegan Christiansen', case = False)
                gps_df['Date'] = pd.to_datetime(gps_df['Date']).dt.date
                gps_df = gps_df.drop(columns=['First Name', 'AthleteName'])
                gps_df['Group'] = gps_df['Group'].str.replace("Defence", "Defense", case = False)
                gps_df['Position'] = gps_df['Position'].str.replace('Wide receiver', 'WR', case = False)
                gps_df['Position'] = gps_df['Position'].str.replace('Tight end', 'TE', case = False)
                gps_df['Position'] = gps_df['Position'].str.replace('Safety', 'DB', case = False)
                gps_df['Position'] = gps_df['Position'].str.replace('Running back', 'RB', case = False)
                gps_df['Position'] = gps_df['Position'].str.replace('Quarterback', 'QB', case = False)
                gps_df['Position'] = gps_df['Position'].str.replace('Linebacker', 'LB', case = False)
                gps_df['Position'] = gps_df['Position'].str.replace('Left guard and right guard', 'OL', case = False)
                gps_df['Position'] = gps_df['Position'].str.replace('Defensive tackle', 'DL', case = False)
                gps_df['Position'] = gps_df['Position'].str.replace('Defensive end', 'DL', case = False)
                gps_df['Position'] = gps_df['Position'].str.replace('Cornerback', 'DB', case = False)
                gps_df['Position'] = gps_df['Position'].str.replace('Centre', 'OL', case = False)
                gps_df['Distance Total_Miles'] = gps_df['Distance Total'] / 1609.344
                gps_df = gps_df[['Name', 'Date', 'Hi Intensity Accels', 'Distance Total', 'Distance Total_Miles', 'Position', 'Group']]
            else:
                gps_df = gps_df[['AthleteName', 'Date', 'Group', 'Position', 'Sprints', 'Max Speed']]
                gps_df[['AthleteName', 'First Name']] = gps_df['AthleteName'].str.split(',',expand=True)
                gps_df['Name'] = gps_df['First Name'] + ' ' + gps_df['AthleteName']
                gps_df['Name'] =  gps_df['Name'].str.lstrip()
                gps_df['Date'] = pd.to_datetime(gps_df['Date']).dt.date
                gps_df['Group'] = gps_df['Group'].str.replace("Defence", "Defense", case = False)
                gps_df['Position'] = gps_df['Position'].str.replace('Wide receiver', 'WR', case = False)
                gps_df['Position'] = gps_df['Position'].str.replace('Tight end', 'TE', case = False)
                gps_df['Position'] = gps_df['Position'].str.replace('Safety', 'DB', case = False)
                gps_df['Position'] = gps_df['Position'].str.replace('Running back', 'RB', case = False)
                gps_df['Position'] = gps_df['Position'].str.replace('Quarterback', 'QB', case = False)
                gps_df['Position'] = gps_df['Position'].str.replace('Linebacker', 'LB', case = False)
                gps_df['Position'] = gps_df['Position'].str.replace('Left guard and right guard', 'OL', case = False)
                gps_df['Position'] = gps_df['Position'].str.replace('Defensive tackle', 'DL', case = False)
                gps_df['Position'] = gps_df['Position'].str.replace('Defensive end', 'DL', case = False)
                gps_df['Position'] = gps_df['Position'].str.replace('Cornerback', 'DB', case = False)
                gps_df['Position'] = gps_df['Position'].str.replace('Centre', 'OL', case = False)
                gps_df['Max Speed'] = gps_df['Max Speed'].multiply(0.621371)
                gps_df['Name'] = gps_df['Name'].str.replace('Tegan Christensen', 'Tegan Christiansen', case = False)
                gps_df = gps_df[['Name', 'Date','Sprints', 'Max Speed', 'Position', 'Group']]
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            gps_df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        dash_table.DataTable(
            gps_df.to_dict('records'),
            [{'name': i, 'id': i} for i in gps_df.columns],
            id='csv_table', editable=True,
        ),

        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])

@callback(
    Output('output-data-upload', 'children'),
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename'),
    State('upload-data', 'last_modified')]
    )
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [parse_contents(c, n, d) for c, n, d in zip(list_of_contents, list_of_names, list_of_dates)]
        return children

@callback(
    Output("download-dataframe-csv", "data"),
    Input("btn_csv", "n_clicks"),
    State('csv_table', 'data'),
    prevent_initial_call=True,
)

def func(n_clicks,data):
    new_gps_df = pd.DataFrame(data)
    new_gps_df.to_csv('gps_converted.csv', mode='a')
    return dcc.send_data_frame(new_gps_df.to_csv, "gps_converted.csv")