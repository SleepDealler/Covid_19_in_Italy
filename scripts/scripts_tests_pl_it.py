import pandas as pd
import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots
import plotly.io as pio
import os
import plotly_settings



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
def replace_negative_on_column(df, column):
    for i in range(len(df)):
            if df.at[i, column] < 0:
                prev_value = df.at[max(i - 1, 0), column]
                next_value = df.at[min(i + 1, len(df) - 1), column]
                average_value = (prev_value + next_value) / 2
                df.at[i, column] = average_value

df_italy.rename(columns=col_names, inplace=True)
df_italy['date'] = pd.to_datetime(df_italy['date'].str[:10], format='%Y-%m-%d')
df_italy['tested'] = df_italy['swabs'].diff()
df_italy.at[0, 'tested'] = df_italy['swabs'].iloc[0]
replace_negative_on_column(df_italy, 'tested')
df_italy['deaths'] = df_italy['deceased'].diff()
df_italy.at[0, 'deaths'] = df_italy['deceased'].iloc[0]
replace_negative_on_column(df_italy, 'deaths')

casi = pd.read_csv("../data/casi.csv", sep=';')
casi['DATA_PRELIEVO_DIAGNOSI'] = pd.to_datetime(casi['DATA_PRELIEVO_DIAGNOSI'], format='%d/%m/%Y')



df_poland = pd.read_csv('../data/data_poland_rcb.csv')
df_poland['Date'] = pd.to_datetime(df_poland['Date'])

poland_population = 37970000  #  population of Poland
italy_population = 60360000   #  population of Italy

poland_factor = 3797
italy_factor = 6036

#%%
poland_cases = df_poland[['Date', 'liczba_przypadkow']]
poland_cases.set_index('Date', inplace=True)

#%%
poland_tests = df_poland[['Date', 'liczba_wykonanych_testow']]
poland_tests.set_index('Date', inplace=True)
#%%
fig = go.Figure()

fig.add_trace(go.Scatter(x=list(casi.DATA_PRELIEVO_DIAGNOSI), y=list(casi.CASI / italy_factor), name='Cases - ITALY', mode='lines'))
fig.add_trace(go.Scatter(x=list(poland_cases.index ), y=list(poland_cases.liczba_przypadkow / poland_factor), name='Cases - POLAND', mode='lines'))
fig.add_trace(go.Scatter(x=list(df_italy.date), y=list(df_italy.tested / italy_factor), name='Test - ITALY', mode='lines'))
fig.add_trace(go.Scatter(x=list(poland_tests.index ), y=list(poland_tests.liczba_wykonanych_testow / poland_factor), name='Test - POLAND', mode='lines'))
fig.update_layout(
    title_text="Number of cases per 10,000 citizens",
    xaxis_title="Date",
    yaxis_title="Number")

fig.write_html('../plots/cases_tests_compare.html')
fig.write_image('../plots/cases_tests_compare.png')

