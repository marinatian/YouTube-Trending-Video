import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import dash_bootstrap_components as dbc
from heatmap import generate_heatmap
from mywordcloud import generate_wordcloud
from Top_5_videos import generate_top5_videos
from Top_10_Categories import generate_top10_categories

df = pd.read_csv("Youtube-Trending-Video.csv")

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# the sidebar layout
sidebar = dbc.Col(
    [
        html.Div([
            html.Img(src=app.get_asset_url('YTLogo_old_new_animation.gif'),id='image', style={'width': '100%'}),
            ], className='sidebar'),
        html.Hr(),
        dbc.Nav(
            [
                html.Div(
                    dcc.Dropdown(
                        id='country-dropdown',
                        options=[{'label': country, 'value': country} for country in df['country'].dropna().unique()],
                        value=df['country'].dropna().unique()[0],
                        className="mt-4",
                        placeholder="Select Country",
                    ),
                    style={"background-color": "white", "padding": "10px", "margin-bottom": "10px"}
                ),
                html.Div(
                    dcc.Slider(
                        id='time-slider',
                        min=0,
                        max=20,
                        step=1,
                        value=10,
                        marks={i: str(i) for i in range(21)},
                        className="mt-4",
                    ),
                    style={"background-color": "white", "padding": "10px", "margin-bottom": "10px"}
                ),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style={"position": "fixed", "top": 0, "left": 0, "bottom": 0, "width": "16rem", "padding": "2rem 1rem","background-color": "rgba(0, 123, 255, 0.6)"},
    md=3,
)


app.layout = dbc.Container([
    dbc.Row([
        sidebar,
        dbc.Col(
            md=9,
            style={'margin-left': '18rem'},
            children=[
                dbc.Row([
                    dbc.Col(dcc.Graph(id='top-10-categories-graph',style={'width': '100%', 'height': 'auto'}),width=6),
                    dbc.Col(html.Img(id='wordcloud-image', style={'width': '100%', 'height': 'auto'}), width=6, style={'margin-top': '110px'})
                ]),
                dbc.Row([
                    dbc.Col(
                        [
                            dcc.Dropdown(
                                id='heatmap-metric-selector',
                                options=[
                                    {'label': 'View Count', 'value': 'view_count'},
                                    {'label': 'Likes', 'value': 'likes'},
                                    {'label': 'Comment Count', 'value': 'comment_count'}
                                ],
                                value='view_count',
                                className="mb-2"
                            ),
                            dcc.Graph(id='heatmap-graph',style={'width': '100%', 'height': 'auto'})
                        ],
                        md=6,
                        className="mb-4"
                    ),
                    dbc.Col(
                        html.Div(id='top-5-videos-content'),
                        md=6,
                        className="mb-4"
                    )
                ])
            ]
        ),
    ]),
], fluid=True)


@app.callback(
    Output('wordcloud-image', 'src'),
    [Input('country-dropdown', 'value')]
)
def update_image(selected_country):
    return generate_wordcloud(df, selected_country)

@app.callback(
    Output('heatmap-graph', 'figure'),
    [Input('heatmap-metric-selector', 'value')]
)
def update_heatmap(selected_metric):
    return generate_heatmap(df, selected_metric)

@app.callback(
    Output('top-5-videos-content', 'children'),
    [Input('country-dropdown', 'value')]
)
def update_top5_videos(selected_country):
    return generate_top5_videos(df,selected_country)

@app.callback(
    Output('top-10-categories-graph', 'figure'),
    [Input('country-dropdown', 'value')]
)
def update_top10_categories(selected_country):
    return generate_top10_categories(df,selected_country)

if __name__ == '__main__':
    app.run_server(debug=True)
