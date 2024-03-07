import pandas as pd
import plotly.express as px

def generate_top10_categories(df, date_range, selected_country='A11'):

    # filter the df use the date range
    df = df.loc[lambda x : (x['trending_date_map'] >= date_range[0]) & (x['trending_date_map'] <= date_range[1])]

    # If 'All' is selected, use the full dataset; otherwise, filter by the selected country
    if selected_country != 'All':
        df = df[df['country'] == selected_country]

    category_counts = df['categoryName'].value_counts().nlargest(10)

    fig = px.bar(category_counts, orientation='h', color=category_counts.index,
                 labels={'value': 'Number of Videos', 'index': 'Category'},
                 title=f'Top 10 Most Popular Categories in {selected_country}')

    # dont show the legend
    fig.update_layout(
        yaxis={'categoryorder': 'total ascending'},
        showlegend=False
    )
    return fig