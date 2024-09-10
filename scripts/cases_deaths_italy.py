import pandas as pd
import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots
import plotly.io as pio
import os
import plotly_settings


casi = pd.read_csv("../data/casi.csv", sep=';')
decessi = pd.read_csv("../data/decessi.csv", sep=';')
decessi = decessi[:-1]
ricoveri = pd.read_csv("../data/ricoveri.csv", sep=';')
sesso  = pd.read_csv("../data/sesso.csv", sep=';')

casi['DATA_PRELIEVO_DIAGNOSI'] = pd.to_datetime(casi['DATA_PRELIEVO_DIAGNOSI'], format='%d/%m/%Y')
decessi['DATA_DECESSO'] = pd.to_datetime(decessi['DATA_DECESSO'], format='%d/%m/%Y')
ricoveri['DATARICOVERO1'] = pd.to_datetime(ricoveri['DATARICOVERO1'], format='%d/%m/%Y')


merged_df = pd.merge(casi, decessi, left_on='DATA_PRELIEVO_DIAGNOSI',right_on='DATA_DECESSO', how='left')
merged_df['cases_5'] = merged_df['CASI'].shift(3)
merged_df['mortalit'] = merged_df['DECESSI'] / merged_df['cases_5']
healthcare_workers = pd.read_csv('../data/iss_opsan_italia_sintomatici.csv')

def replace_negative_on_column(df, column):
    for i in range(len(df)):
            if df.at[i, column] < 0:
                prev_value = df.at[max(i - 1, 0), column]
                next_value = df.at[min(i + 1, len(df) - 1), column]
                average_value = (prev_value + next_value) / 2
                df.at[i, column] = average_value


df_italy = pd.read_csv('../data/dpc-covid19-ita-andamento-nazionale.csv')
col_names = {
    'data': 'date',
    'stato': 'state',
    'codice_regione': 'region_code',
    'denominazione_regione': 'region_name',
    'ricoverati_con_sintomi': 'hospitalized_with_symptoms',
    'terapia_intensiva': 'intensive_care',
    'totale_ospedalizzati': 'total_hospitalized',
    'isolamento_domiciliare': 'home_isolation',
    'totale_positivi': 'total_positives',
    'variazione_totale_positivi': 'total_positivity_change',
    'nuovi_positivi': 'new_positive',
    'dimessi_guariti': 'discharged_cured',
    'deceduti': 'deceased',
    'note': 'note',
    'lat': 'lat',
    'long': 'long',
    'casi_da_sospetto_diagnostico': 'cases_of_diagnostic_suspicion',
    'casi_da_screening': 'cases_to_be_screened',
    'totale_casi': 'total_cases',
    'tamponi': 'swabs',
    'casi_testati': 'tested_cases',
    'ingressi_terapia_intensiva': 'intensive_therapy_entrances',
    'note_test': 'test_notes',
    'note_casi': 'case_notes',
    'totale_positivi_test_molecolare': 'total_positive_molecular_test',
    'totale_positivi_test_antigenico_rapido': 'total_positive_rapid_antigenic_test',
    'tamponi_test_molecolare': 'molecular_test_swabs',
    'tamponi_test_antigenico_rapido': 'rapid_antigenic_test_swabs',
    'codice_nuts_1': 'nuts_code_1',
    'codice_nuts_2': 'nuts_code_2'
}

df_italy.rename(columns=col_names, inplace=True)
df_italy['date'] = pd.to_datetime(df_italy['date'].str[:10], format='%Y-%m-%d')
df_italy['tested'] = df_italy['swabs'].diff()
df_italy.at[0, 'tested'] = df_italy['swabs'].iloc[0]
replace_negative_on_column(df_italy, 'tested')
df_italy['deaths'] = df_italy['deceased'].diff()
df_italy.at[0, 'deaths'] = df_italy['deceased'].iloc[0]
replace_negative_on_column(df_italy, 'deaths')

df_poland = pd.read_csv('../data/data_poland_rcb.csv')
df_poland['Date'] = pd.to_datetime(df_poland['Date'])

poland_population = 37970000  #  population of Poland
italy_population = 60360000   #  population of Italy

poland_factor = 3797
italy_factor = 6036

vaccination_start = '2020-12-27'
lockdown_start  = '2020-03-09'
lockdown_end = '2020-05-04'
zoning_start = '2020-11-03'
zoning_end = '2022-04-01'

fig = make_subplots(specs=[[{"secondary_y": True}]])
decessi=decessi[:-1]
scatter_cases = go.Scatter(x=list(casi.DATA_PRELIEVO_DIAGNOSI), y=list(casi.CASI), name='Cases', mode='lines')
scatter_deaths = go.Scatter(x=list(decessi.DATA_DECESSO), y=list(decessi.DECESSI), name='Deaths', mode='lines')

fig.add_trace(scatter_deaths, secondary_y=True)
fig.add_trace(scatter_cases)

cases_color = scatter_cases.line.color
deaths_color = scatter_deaths.line.color
color_lockdown = 'red'
color_zoning = 'darkgray'
fig.add_vrect(
    x0=lockdown_start, x1= lockdown_end,
    fillcolor=color_lockdown, opacity=0.5,
    layer="below", line_width=0,
)

# Adding background shading for zoning period
fig.add_vrect(
    x0=zoning_start, x1=zoning_end,
    fillcolor=color_zoning, opacity=0.5,
    layer="below", line_width=0,
)

# Adding a vertical line for vaccination start
fig.add_vline(x=vaccination_start, line_width=3, line_dash="dash", line_color="green")

fig.add_trace(go.Scatter(
    x=[None], y=[None], mode='markers',
    marker=dict(color=color_lockdown, size=15, symbol='square'),
    name="Lockdown Period"
))
fig.add_trace(go.Scatter(
    x=[None], y=[None], mode='markers',
    marker=dict(color=color_zoning, size=15, symbol='square'),
    name="Zoning Period"
))
fig.add_trace(go.Scatter(
    x=[None], y=[None],mode='lines',  line=dict(color='green', width=4, dash='dash'),
    name="Vaccination Start"
))

fig.update_layout(
    title_text="Number of COVID cases and deaths",
    xaxis_title="Date",
    yaxis=dict(
        title="Cases",
        titlefont=dict(color=cases_color),
        tickfont=dict(color=cases_color),
        ),
    yaxis2=dict(
        title="Deaths",
        titlefont=dict(color=deaths_color),
        tickfont=dict(color=deaths_color),
    ),)
fig.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=14, label="14d", step="day", stepmode="backward"),
                dict(count=30, label="1M", step="day", stepmode="todate"),
                dict(count=90, label="3M", step="day", stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(visible=True),
        type="date"
    )
)

fig.write_html('../plots/cases_deaths_italy.html')
fig.write_image("../plots/cases_deaths_italy.png")
