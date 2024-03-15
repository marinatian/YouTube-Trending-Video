import plotly.express as px
import pandas as pd

def generate_heatmap(df,date_range, selected_metric ='view_count', metrics=['view_count', 'likes', 'comment_count']):

    # filter the df use the date range
    df = df.loc[lambda x : (x['trending_date_map'] >= date_range[0]) & (x['trending_date_map'] <= date_range[1])]

    # df['publishedAt'] = pd.to_datetime(df['publishedAt'], errors='coerce')
    # df['hour_of_day'] = df['publishedAt'].dt.hour
    # df['day_of_week'] = df['publishedAt'].dt.dayofweek
    # df['day_name'] = df['publishedAt'].dt.day_name()

    df = (
        df
        .assign(publishedAt=lambda x: pd.to_datetime(x['publishedAt'], errors='coerce'))
        .assign(hour_of_day=lambda x: x['publishedAt'].dt.hour)
        .assign(day_of_week=lambda x: x['publishedAt'].dt.dayofweek)
        .assign(day_name=lambda x: x['publishedAt'].dt.day_name())
    )



    # Aggregate data for heatmap
    def aggregate_data(metrics):
        threshold = df[metrics].quantile(0.95)
        filtered_df = df[df[metrics] > threshold]
        heatmap_df = filtered_df.groupby(['day_of_week', 'hour_of_day', 'day_name'])[metrics].mean().reset_index()
        heatmap_df = heatmap_df.pivot(index='day_name', columns='hour_of_day', values=metrics).fillna(0)
        return heatmap_df

    aggregated_data = (
        aggregate_data(selected_metric)
        .reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
        .reindex(columns=range(24))
    )
    fig = px.imshow(
        aggregated_data,
        #labels=dict(x="Hour of Day", y="Day of Week", color=selected_metric.capitalize()),
        x=aggregated_data.columns,
        y=aggregated_data.index,
        aspect='auto',
    )
    
    fig.update_layout(
        xaxis_nticks=24,
        yaxis_nticks=7,
        margin=dict(t=20, l=20, b=20, r=20),
        hovermode='closest',
    )
    
    fig.update_coloraxes(colorscale='Teal', colorbar_title_side='right')
    
    return fig
