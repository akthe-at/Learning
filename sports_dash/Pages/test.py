import base64
import datetime
import io

import dash
from dash.dependencies import Input, Output, State
from dash import dcc, html, dash_table

import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Div(id='output-data-upload'),
    html.Div(
    [
        html.Button("Download CSV", id="btn_csv"),
        dcc.Download(id="download-dataframe-csv"),
    ]),
])

def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            global df
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
            if 'Hi Intensity Accels' in df.columns:
                df = df[['AthleteName', 'Hi Intensity Accels', 'Distance Total', 'Group', 'Position', 'Date']]
                df[['AthleteName', 'First Name']] = df['AthleteName'].str.split(',',expand=True)
                df['Name'] = df['First Name'] + ' ' + df['AthleteName']
                df['Name'] = df['Name'].str.lstrip()
                df['Date'] = pd.to_datetime(df['Date']).dt.date
                df = df[['Name','Date', 'Group', 'Position', 'Hi Intensity Accels', 'Distance Total']]
            else:
                df[['AthleteName', 'First Name']] = df['AthleteName'].str.split(',',expand=True)
                df['Name'] = df['First Name'] + ' ' + df['AthleteName']
                df['Name'] =  df['Name'].str.lstrip()
                df['Date'] = pd.to_datetime(df['Date']).dt.date
                df['Max Speed'] = df['Max Speed'] * 0.621371192
                df = df[['Name','Date', 'Group', 'Position', 'Sprints', 'Max Speed']]
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        dash_table.DataTable(
            df.to_dict('records'),
            [{'name': i, 'id': i} for i in df.columns]
        ),

        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])

@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children

@app.callback(
    Output("download-dataframe-csv", "data"),
    Input("btn_csv", "n_clicks"),
    prevent_initial_call=True,
)

def func(n_clicks):
    return dcc.send_data_frame(df.to_csv, "mydf.csv")

if __name__ == '__main__':
    app.run_server(debug=True)
