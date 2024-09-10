
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






df_italy['tested_7day_avg'] = df_italy['tested'].rolling(window=7).mean()
df_italy['new_positive_7day_avg'] = df_italy['new_positive'].rolling(window=7).mean()


fig = make_subplots(specs=[[{"secondary_y": True}]])

# fig.add_trace(go.Scatter(x=list(df_italy.date), y=list(df_italy.tested ), fill='tozeroy', name='Tests - ITALY',line=dict(shape='spline', smoothing=1.3)))
# fig.add_trace(go.Scatter(x=list(df_italy.date), y=list(df_italy.new_positive), fill='tozeroy', name='Cases - ITALY',line=dict(shape='spline', smoothing=0.5)))

fig.add_trace(go.Scatter(x=df_italy['date'], y=df_italy['tested_7day_avg'], mode='lines', fill='tozeroy', name='Tests'))
fig.add_trace(go.Scatter(x=df_italy['date'], y=df_italy['new_positive_7day_avg'], mode='lines', fill='tozeroy', name='Cases'))


df_italy['positive_tests'] = df_italy['new_positive'] / df_italy['tested']
df_italy['positive_tests_rolling']=df_italy['positive_tests'].rolling(window=7).mean()
#fig.add_trace(go.Scatter(x=list(df_italy.date), y=list(df_italy.positive_tests), name='Positive rate', connectgaps=True, mode='lines+markers', line=go.scatter.Line(color='darkblue')), secondary_y=True)
fig.add_trace(go.Scatter(x=list(df_italy.date), y=list(df_italy.positive_tests_rolling), name='Positive rate', connectgaps=True, mode='lines+markers', line=go.scatter.Line(color='darkblue')), secondary_y=True)

fig.update_layout(
    title_text="Number of cases and tests - ITALY<br><sup>7 day mean</sup> ",
    xaxis_title="Date",
    yaxis_title="Number")
fig.update_layout(barmode='overlay')
fig.update_yaxes(title_text="Number", secondary_y=False, rangemode='tozero')
fig.update_yaxes(title_text="Rate ", secondary_y=True, rangemode='tozero', tickformat=',.0%',titlefont=dict(color="darkblue"))
fig.update_layout(bargap=0)
fig.update_layout(
    xaxis=dict(
        range=[df_italy['date'].min(), df_italy['date'].max()]
    )
)
fig.write_html('../plots/tests_italy.html')
fig.write_image('../plots/tests_italy.png')
