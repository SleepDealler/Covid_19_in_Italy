import plotly.express as px
import pandas as pd

def most_and_less(df_italy):
    populations = {
        'Lombardia': 10060574,
        'Campania': 5801692,
        'Basilicata': 553254,
        'Valle d\'Aosta': 123360
    }

    filtered_df = df_italy[df_italy['region_name'].isin(['Valle d\'Aosta', 'Basilicata', 'Campania', 'Lombardia'])]
    filtered_df.rename(columns={'region_name': 'Region'}, inplace=True)

    filtered_df['Percentage of Population Infected'] = filtered_df.apply(
        lambda row: f"{(row['total_positives'] / populations[row['Region']]) * 100:.2f}%", axis=1
    )

    fig = px.line(
        filtered_df,
        x='date',
        y='total_positives',
        color='Region',
        title='Total positives for the 2 most and least densely populated regions in Italy',
        labels={'date': 'Date', 'total_positives': 'Total Positives'},
        hover_data=['Percentage of Population Infected']
    )

    fig.update_layout(
        title={'text': 'Total positives for the 2 most and least densely populated regions in Italy', 'font': {'size': 24}},
        xaxis_title={'text': 'Date', 'font': {'size': 30}},
        yaxis_title={'text': 'Total Positives', 'font': {'size': 30}}
    )

    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(step="all")
            ])
        )
    )

    html_file_path = '../plots/most_and_less.html'
    fig.write_html(html_file_path)
