import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import pandas as pd
import dash_bootstrap_components as dbc
from heatmap import generate_heatmap
from mywordcloud import generate_wordcloud
from Top_5_videos import generate_top5_videos
from Top_10_Categories import generate_top10_categories
pd.options.mode.chained_assignment = None  # default='warn'

url = 'https://media.githubusercontent.com/media/marinatian/YouTube-Trending-Video/main/YouTube-Trending-Video.csv'
df = pd.read_csv(url, low_memory=False,lineterminator='\n')

df.dropna(inplace=True)

df = (
    df
    .assign(trending_date=lambda x: pd.to_datetime(x['trending_date']))
    # add a column to map the trending_date from min to max
    .assign(trending_date_map=lambda x: (x['trending_date'] - min(x['trending_date'])).dt.days)
)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],suppress_callback_exceptions=True)
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
        html.H6("Helping North American video creators to visualize content trends and audience preferences.",style={"textAlign": "center"}),
        html.Div(style={'margin-top': '10px'}),
        dbc.Nav(
            [
                
                html.Div(
                    [
                        dcc.RangeSlider(
                            id='date-slider',
                            min=1,
                            max=df['trending_date_map'].max(),
                            step=1,
                            value=[1, df['trending_date_map'].max()],
                            marks={
                                1: {'label': str(min(df['trending_date']).date()), 'style': {'white-space': 'nowrap'}},
                                int(df['trending_date_map'].max()): {'label': str(max(df['trending_date']).date()), 'style': {'white-space': 'nowrap'}}
                            }
                        )
                    ],
                    style={
                        "background-color": "white",
                        "padding": "10px",
                        "margin-bottom": "10px",
                        'margin-top': '30px'
                    }
                ),

                html.Div(style={'margin-top': '30px'}),
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
                ]),

                # add a button to go to another page
                html.Div([
                    html.A(
                        dbc.Button(
                            "Go to category page",
                            color="primary",
                            className="mr-1",
                            id='go-to-another-page',
                            href='/another-page'
                            ),
                        href='/another-page'
                    )],
                    style={'margin-top': '30px'}
                ),
            ],

            style={
                "background-color": "white",
                "padding": "10px",
                "margin-top": "50px",
                "margin-bottom": "10px",
                'border-top': '2px solid #d6d6d6'
                },
            vertical=True,
            pills=True,
        )
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
    html.Div([
        dcc.Location(id='url', refresh=False),
        dcc.Store(id='date-slider-store'),
        html.Div(id='page-content')
    ]),
], fluid=True)


index_page = html.Div([
    dbc.Row([
        sidebar,
        dbc.Col(
            md=9,
            style={'margin-left': '18rem'},
            children=[
                dbc.Row([
                    dbc.Col(
                        [
                            # add a titl
                            html.H5("What types of movies are popular with audiences? ", style={"textAlign": "center",'margin-bottom':'20px'}),
                        dcc.Graph(
                            id='top-10-categories-graph',
                            style={'width': '100%', 'height': 'auto'}
                        )
                        ],
                        width=6,
                        style={'background-color':'#f8f9fa','border-radius':'10px','padding':'20px','margin-top':'10px','margin-left':'10px','margin-right':'10px','margin-bottom':'10px'}
                    ),
                    dbc.Col(
                        [
                            # add a titl
                            html.H5("What words appear commonly in titles?", style={"textAlign": "center",'margin-bottom':'20px'}),
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
                            html.H5("What's the best time to post a video?", style={"textAlign": "center",'margin-bottom':'20px'}),
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
])

another_page_layout = html.Div(
    dbc.Row([

        dbc.Row([

            dbc.Col([
                    html.Div([
                        html.A(
                            dbc.Button(
                                "Back to Home",
                                color="primary",
                                className="mr-1",
                                id='back-to-home',
                                href='/'
                                ),
                            href='/'
                        )],
                        style={'margin-top': '30px', 'margin-left': '100px','margin-top': '50px'})],
                    md=3
                ),

            dbc.Col([
                    # add a dropdown to select the category
                    html.Div([
                        html.H5('Select categoryName', style={"textAlign": "center",'margin-bottom':'10px','margin-top':'10px'}),
                        dcc.Dropdown(
                            id='category-dropdown',
                            options=[{'label': i, 'value': i} for i in df['categoryName'].dropna().unique()],
                            value=df['categoryName'].dropna().unique()[0],
                            style={'width': '100%'}
                        )],
                        style={'margin-left': '20px','width': '100%', 'margin-top': '50px'})
                ],md=6),

            ]),


        # wordcloud
        dbc.Col(
            [
                # add a titl
                html.H5("What words appear commonly in titles?", style={"textAlign": "center",'margin-bottom':'20px'}),
                html.Img(
                    id='wordcloud-image-another',
                    # set center
                    style={'width': '100%', 'height': 'auto','display': 'block', 'margin-left': 'auto', 'margin-right': 'auto'}
                )
            ],
            width=5,
            style={'background-color':'#f8f9fa','border-radius':'10px','padding':'20px','margin-top':'10px','margin-left':'30px','margin-right':'10px','margin-bottom':'10px'}
        ),

        # top 5 videos
        dbc.Col(
            [
                html.H5("Top 5 videos", style={"textAlign": "center",'margin-bottom':'20px'}),
                html.Div(
                    id='top-5-videos-content-another',
                    style={'width': '100%', 'height': 'auto'}
                ),
            ],
            md=5,
            style={'background-color':'#f8f9fa','border-radius':'10px','padding':'20px','margin-top':'10px','margin-left':'10px','margin-right':'10px','margin-bottom':'10px'}
        )
    ])
)

@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')],
    [State('date-slider-store', 'data')]
)
def display_page(pathname, date_range):
    if pathname == '/another-page':
        return another_page_layout
    else:
        return index_page

@app.callback(
    Output('date-slider-store', 'data'),
    [Input('date-slider', 'value')]
)
def store_date_slider_value(value):
    return value


@app.callback(
    Output('wordcloud-image-another', 'src'),
    [Input('date-slider-store', 'data'), Input('category-dropdown', 'value')]
)
def update_image(date_range, category):
    if date_range is not None:
        return generate_wordcloud(df, date_range, category=category, width=800, height=500)
    return None

@app.callback(
    Output('top-5-videos-content-another', 'children'),
    [Input('date-slider-store', 'data'), Input('category-dropdown', 'value')]
)
def update_top5_videos(date_range, category):
    if date_range is not None:
        return generate_top5_videos(app, df, date_range, category=category)
    return None

@app.callback(
    Output('wordcloud-image', 'src'),
    [Input('country-radioitems', 'value'), Input('date-slider', 'value')]
)
def update_image( selected_country, date_range):
    return generate_wordcloud(df, date_range, selected_country)

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
    app.run(debug=False)
