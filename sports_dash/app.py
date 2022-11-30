import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, Input, Output, dash_table, callback
import pandas as pd
from datetime import date, timedelta
import dash_mantine_components as dmc


# Bring data into App
dfp = pd.read_csv(r'C:\Users\kellya\Documents\Python Code\python_for_coaches-main\python_for_coaches-main\Learning\sports_dash\UWW_FB_PERFORMANCE_TESTING.csv')
dfp = dfp.to_dict('records')

uww_logo = 'https://dbukjj6eu5tsf.cloudfront.net/sidearm.sites/uwwsports.com/images/responsive_2019/main_logo.svg'

dbc_css = ("https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.2/dbc.min.css")
app = dash.Dash(
    __name__,
    use_pages=True,
    pages_folder="Pages",
    external_stylesheets=[dbc.themes.PULSE, dbc_css],
    suppress_callback_exceptions=True, meta_tags=[{'name': 'viewport','content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,'}],
)



navbar = dbc.NavbarSimple(
    children=[
                            dbc.NavItem(dbc.NavLink("Individual", href=app.get_relative_path("/"))),
                            dbc.NavItem(dbc.NavLink("Team", href=app.get_relative_path("/team"))),
                            dbc.DropdownMenu(
                                children=[
                                    dbc.DropdownMenuItem("GPS Conversion Tool", href=app.get_relative_path("/gps")),
                                    dbc.DropdownMenuItem("Hydration Tool", href=app.get_relative_path("/hydration")),
                                ],
                                nav=True,
                                in_navbar=True,
                                label="More",
                            ),
                            dbc.NavItem(html.Img(src=uww_logo, height="30px")),
                        ],
                        brand="UW-Whitewater Football Dashboard",
                        brand_href="/",
                        color="primary",
                        fluid=True,
                        dark=True,
)

app.layout = html.Div(children=[dmc.Container([navbar,
    dcc.Store(id="stored-performance-data", data=dfp),
    dcc.Store(id="store-dropdown-value", data=None),
    dash.page_container],
    fluid=True,)])

if __name__ == "__main__":
    app.run_server(debug=True, port=4050)
