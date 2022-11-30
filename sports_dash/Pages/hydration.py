import dash
from dash import dcc, html, Input, Output, dash_table, callback, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
from plotly.subplots import make_subplots
import dash_mantine_components as dmc




dash.register_page(__name__, path="/hydration")
pio.templates.default = "ggplot2"

# build your components

# app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

input_groups = html.Div(
    [
        dbc.InputGroup(
            [dbc.InputGroupText("First Name"), dbc.Input(id="user-first-name", placeholder="First Name", debounce=True)],
            className="mb-3",
        ),
        dbc.InputGroup(
            [
                dbc.InputGroupText("Last Name"),
                dbc.Input(id="user-last-name", placeholder="Last Name", debounce=True),
            ],
            className="mb-3",
        ),
        dbc.InputGroup(
            [
                dbc.InputGroupText("Pre-Practice Weight in Pounds (lbs)"),
                dbc.Input(id="user-pre-weight", placeholder="Weight", type="number", debounce=True),
            ],
            className="mb-3",
        ),
        dbc.InputGroup(
            [
                dbc.InputGroupText("Post-Practice Weight in Pounds (lbs)"),
                dbc.Input(id="user-post-weight", placeholder="Weight", type="number", min=50, max=400, debounce=True),
            ],
            className="mb-3",
        ),
        dbc.Label("Select Your Sport"),
        dbc.RadioItems(
            options=[
                {"label": "Football", "value": "Football"},
                {"label": "Baseball", "value": "Baseball"},
                {"label": "Bowling", "value": "Bowling"},
                {"label": "Men's Basketball", "value": "Men's Basketball"},
                {"label": "Women's Basketball", "value": "Women's Basketball"},
                {"label": "Softball", "value": "Softball"},
                {"label": "Men's Tennis", "value": "Men's Tennis"},
            ],
            value=1,
            id="sport-select-radioitems-input",
        ),
        html.Div([dbc.Button("Submit", id="submit-form", outline=False, color="primary", className="me-1", n_clicks=0)], style={"horizontalAlign":"middle"}, className="d-grid gap-2 col-6 mx-auto"),
        dbc.Modal(
            [
                dbc.ModalFooter(
                    dbc.Button(
                        "Close", id="close", className="ms-auto", n_clicks=0
                    )
                ),
            ],
            id="modal",
            is_open=False,
        ),
    ]
)

test_card = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H2("Rehydration Tool", className="card-title"),
                input_groups,
            ]
        ),
    ],
)


# Customize your own layout

layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [test_card],
                    {"size": 3, "offset": 9},
                ),
            ]
        ),
    ],
    className="dbc",
)



@callback(
    Output("modal", "children"),
    Input("user-first-name", "value"),
    Input("user-last-name", "value"),
    Input("user-pre-weight", "value"),
    Input("user-post-weight", "value"),
    Input("submit-form", "n_clicks"), prevent_initial_call=True,
)
def result_message(first_name, last_name, pre_weight, post_weight, n):
    weight_change = pre_weight - post_weight
    hydration_demand = weight_change * 16
    if n > 1:
        return [
            dbc.ModalHeader(f"Hey {first_name} {last_name}!"),
            dbc.ModalBody(f"""Today you lost a total of {weight_change}lbs during practice.
            To rehydrate you are going to need to drink {hydration_demand} additional fluid ounces."""),
            ]
@callback(
    Output("modal", "is_open"),
    [Input("submit-form", "n_clicks")],
    [State("modal", "is_open")], prevent_initial_callback=True,
)
def toggle_modal(n1, is_open):
    if n1:
        return not is_open
    return is_open    
    

#Will need these things!!!
# Another button to clear/reset form
# Figure out Modal or use a popup window of some other sort?
# Another callback function setup for adding these variable items to a db
# Add a timestamp to the above db addition.
# Add conditional statements to change messaging regarding hydration