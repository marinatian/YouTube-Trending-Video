import dash_bootstrap_components as dbc
from dash import html
import dash

def generate_top5_videos(app, df, date_range, selected_country='US',category=None):
    # filter the df use the date range
    df = df.loc[lambda x : (x['trending_date_map'] >= date_range[0]) & (x['trending_date_map'] <= date_range[1])]
    
    filtered_df = df[df['country'] == selected_country]
    
    if category:
        filtered_df = filtered_df[filtered_df['categoryName'] == category]
    
    top_videos = filtered_df.sort_values(by='view_count', ascending=False).drop_duplicates(subset=['video_id'])
    top_videos = top_videos.iloc[:, [1,8,9,10,11,12]]
    top_5videos = top_videos.head(5)
    
    rows = []
    for _, row in top_5videos.iterrows():
        video_info = dbc.Col([
            html.H6(row['title'], className='mt-2', style={'white-space': 'normal', 'font-weight': 'bold','text-align':'left',"color":"#45819a"}),
            html.Img(src=app.get_asset_url('view.png'),style={'width': '20px', 'height': 'auto'}),
            html.Span(f"  {int(row['view_count'] / 1000)}K", style={'margin-bottom': '2px', 'white-space': 'normal'}),
            html.Br(),
            html.Img(src=app.get_asset_url('comment.png'),style={'width': '20px', 'height': 'auto'}),
            html.Span(f"  {int(row['comment_count'] / 1000) }K", style={'margin-bottom': '2px', 'white-space': 'normal'}),
            html.Br(),
            html.Img(src=app.get_asset_url('like.png'),style={'width': '20px', 'height': 'auto'}),
            html.Span(f"  {int(row['likes'] / 1000)}K", style={'margin-bottom': '2px', 'white-space': 'normal'})
        ], width=7, style={'padding-right': '5px','margin-left': '20px'})

        thumbnail = dbc.Col([
            html.Img(src=row['thumbnail_link'], style={'width': '180px', 'height': 'auto','display': 'block', 'margin-left': 'auto', 'margin-right': 'auto'})
        ], width=4)

        video_row = dbc.Row([thumbnail, video_info], className='mb-3')
        rows.append(video_row)
    
    return rows