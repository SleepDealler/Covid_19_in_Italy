import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.linear_model import LinearRegression
import datetime

def vaccin_pred(df_world):
    df = df_world
    df_poland = df[df['location'] == 'Poland']
    df_italy = df[df['location'] == 'Italy']
    df_poland['date'] = pd.to_datetime(df_poland['date'])
    df_italy['date'] = pd.to_datetime(df_italy['date'])
    start_date = '2020-12-01'
    df_poland = df_poland[df_poland['date'] >= start_date]
    df_italy = df_italy[df_italy['date'] >= start_date]
    fig = make_subplots(rows=1, cols=1)

    def add_traces_and_predictions(df, country_name, color):
        last_year = df[df['date'] >= (df['date'].max() - pd.DateOffset(years=1))]
        fig.add_trace(go.Scatter(x=df['date'], y=df['people_vaccinated_per_hundred'],
                            mode='lines', name=f'{country_name} Vaccinated [%]',
                            line=dict(color=color)), row=1, col=1)
        fig.add_trace(go.Scatter(x=df['date'], y=df['people_fully_vaccinated_per_hundred'],
                            mode='lines', name=f'{country_name} Fully Vaccinated [%]',
                            line=dict(color=color, dash='dot')), row=1, col=1)

        last_year = last_year.dropna(subset=['people_vaccinated_per_hundred', 'people_fully_vaccinated_per_hundred'])
        dates = last_year['date'].map(datetime.datetime.toordinal).values.reshape(-1, 1)
        model_vaccinated = LinearRegression().fit(dates, last_year['people_vaccinated_per_hundred'])
        model_fully_vaccinated = LinearRegression().fit(dates, last_year['people_fully_vaccinated_per_hundred'])
        future_dates = pd.date_range(start=last_year['date'].max(), periods=365).map(datetime.datetime.toordinal).values.reshape(-1, 1)
        future_dates_actual = pd.date_range(start=last_year['date'].max(), periods=365)
        pred_vaccinated = model_vaccinated.predict(future_dates)
        pred_fully_vaccinated = model_fully_vaccinated.predict(future_dates)

        fig.add_trace(go.Scatter(x=future_dates_actual, y=pred_vaccinated,
                            mode='lines', name=f'{country_name} Vaccinated [%] (Pred)',
                            line=dict(color=color, dash='dash')), row=1, col=1)
        fig.add_trace(go.Scatter(x=future_dates_actual, y=pred_fully_vaccinated,
                            mode='lines', name=f'{country_name} Fully Vaccinated [%] (Pred)',
                            line=dict(color=color, dash='dashdot')), row=1, col=1)

    add_traces_and_predictions(df_poland, 'Poland', 'blue')
    add_traces_and_predictions(df_italy, 'Italy', 'green')

    fig.update_layout(title={'text': 'Vaccinated and Fully Vaccinated Percentage of Population in Poland and Italy', 'font': {'size': 24}},
                      xaxis_title={'text': 'Date', 'font': {'size': 30}},
                      yaxis_title={'text': 'Vaccinated Population [%]', 'font': {'size': 30}},
                      hovermode='x unified')
    fig.write_html("../plots/vaccinated_population_poland_italy.html")
