import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import dash_bootstrap_components as dbc
from heatmap import generate_heatmap
from mywordcloud import generate_wordcloud
from Top_5_videos import generate_top5_videos
from Top_10_Categories import generate_top10_categories
pd.options.mode.chained_assignment = None  # default='warn'

df = pd.read_csv("YouTube-Trending-Video.csv", low_memory=False,lineterminator='\n')

df.dropna(inplace=True)

df = (
    df
    .assign(trending_date=lambda x: pd.to_datetime(x['trending_date']))
    .assign(trending_date=lambda x: x['trending_date'])
    # add a column to map the trending_date from min to max
    .assign(trending_date_map=lambda x: (x['trending_date'] - min(x['trending_date'])).dt.days)
)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# the sidebar layout
sidebar = dbc.Col(
    [
        html.Div(style={'margin-top': '10px'}),
        html.Div([
            html.Img(src=app.get_asset_url('YTLogo_old_new_animation.gif'),id='image', style={'width': '100%'}),
            ], className='sidebar'),
        html.Div(style={'margin-top': '60px'}),
        html.H3("Trending Video",style={"textAlign": "center"}),
        html.Div(style={'margin-top': '10px'}),
        dbc.Nav(
            [
                # create a datapickerRange
                # html.Div(
                #     dcc.DatePickerRange(
                #         id='date-picker-range',
                #         start_date=df['trending_date'].min(),
                #         end_date=df['trending_date'].max(),
                #         display_format='YYYY-MM-DD',
                #         with_portal=True,
                #         clearable=True
                #     ),
                #     style={"background-color": "white", "padding": "10px", "margin-bottom": "10px"}
                # ),

                # create a slider to select the date range to map the trending_date_map
                html.Div(
                    dcc.RangeSlider(
                        id='date-slider',
                        min=1,
                        max=df['trending_date_map'].max(),
                        step=1,
                        value=[1, df['trending_date_map'].max()],
                        marks=
                        {
                            1: str(min(df['trending_date']).date()), 
                            int(df['trending_date_map'].max()): str(max(df['trending_date']).date())
                        }   
                    ),
                    style={"background-color": "white", "padding": "10px", "margin-bottom": "10px"}
                ),               

                html.Div(style={'margin-top': '60px'}),
                html.Div([
                    html.Label('Country', className='mt-4'),
                    dcc.RadioItems(
                        id='country-radioitems',
                        options=[{'label': country, 'value': country} for country in df['country'].dropna().unique()],
                        value=df['country'].dropna().unique()[0],
                        labelStyle={
                            'display': 'block',
                            'font-size': '20px',
                            'padding': '20px',
                            'margin-left': '25px'}
                    )
                ],
                style={
                    "background-color": "white", 
                    "padding": "10px", 
                    "margin-top": "50px",
                    "margin-bottom": "10px",
                    'border-top': '2px solid #d6d6d6'
                    }
                )
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style={
        "position": "fixed", 
        "top": 0, 
        "left": 0, 
        "bottom": 0, 
        "width": "18rem", 
        'border-right': '2px solid #d6d6d6',
        "padding": "2rem 1rem",
        #"background-color": "rgba(0, 123, 255, 0.6)"
        },
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
                    dbc.Col(
                        dcc.Graph(
                            id='top-10-categories-graph',
                            style={'width': '100%', 'height': 'auto'}
                        ),
                        width=6,
                        style={'background-color':'#f8f9fa','border-radius':'10px','padding':'20px','margin-top':'10px','margin-left':'10px','margin-right':'10px','margin-bottom':'10px'}
                    ),
                    dbc.Col(
                        [
                            # add a titl
                            html.H5("The most common words in video titles ", style={"textAlign": "center",'margin-bottom':'20px'}),
                            html.Img(
                                id='wordcloud-image', 
                                # set center
                                style={'width': '100%', 'height': 'auto','display': 'block', 'margin-left': 'auto', 'margin-right': 'auto'}
                            )
                        ],
                        width=5,
                        style={'background-color':'#f8f9fa','border-radius':'10px','padding':'20px','margin-top':'10px','margin-left':'0px','margin-right':'10px','margin-bottom':'10px'}
                    )
                ]),
                dbc.Row([
                    dbc.Col(
                        [
                            html.H5("The best time to post a video", style={"textAlign": "center",'margin-bottom':'20px'}),
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
                        className="mb-4",
                        style={'background-color':'#f8f9fa','border-radius':'10px','padding':'20px','margin-top':'10px','margin-left':'10px','margin-right':'10px','margin-bottom':'20px'}
                    ),
                    dbc.Col(
                        [
                            html.H5("Top 5 videos", style={"textAlign": "center",'margin-bottom':'20px'}),
                            html.Div(
                                id='top-5-videos-content',
                                style={'width': '100%', 'height': 'auto'}
                            ),

                        ],
                        md=5,
                        className="mb-4",
                        style={'background-color':'#f8f9fa','border-radius':'10px','padding':'20px','margin-top':'10px','margin-left':'0px','margin-right':'10px','margin-bottom':'20px'}
                    )
                ])
            ]
        ),
    ]),
], fluid=True)


@app.callback(
    Output('wordcloud-image', 'src'),
    [Input('country-radioitems', 'value'), Input('date-slider', 'value')]
)
def update_image( selected_country, date_range):
    return generate_wordcloud(df,  date_range,selected_country,)

@app.callback(
    Output('heatmap-graph', 'figure'),
    [Input('heatmap-metric-selector', 'value'), Input('date-slider', 'value')]
)
def update_heatmap(selected_metric, date_range):
    return generate_heatmap(df, date_range, selected_metric)

@app.callback(
    Output('top-5-videos-content', 'children'),
    [Input('country-radioitems', 'value'), Input('date-slider', 'value')]
)
def update_top5_videos(selected_country, date_range):
    return generate_top5_videos(app, df, date_range, selected_country)

@app.callback(
    Output('top-10-categories-graph', 'figure'),
    [Input('country-radioitems', 'value'), Input('date-slider', 'value')]
)
def update_top10_categories(selected_country,date_range):
    return generate_top10_categories(df, date_range, selected_country)

if __name__ == '__main__':
    app.run(debug=True)
