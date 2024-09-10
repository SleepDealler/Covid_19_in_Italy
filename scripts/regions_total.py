import pandas as pd
import geopandas as gpd
import numpy as np

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.io as pio
import os

import plotly_settings

#%%
import json
with open('../data/italy-regions.json') as json_file:
    italy_geojson = json.load(json_file)
df = pd.read_csv('../data/dpc-covid19-ita-regioni.csv')

df['codice_regione'] = df['codice_regione'].replace({21: 4, 22: 4})

df['denominazione_regione'] = df['denominazione_regione'].replace({'P.A. Bolzano': 'Trentino-Alto Adige/Südtirol',
                                     'P.A. Trento': 'Trentino-Alto Adige/Südtirol'})
#df['date'] = pd.to_datetime(df['data'].str[:10], format='%Y-%m-%d')

# 1. Identify Columns to Sum and Exclude
columns_to_sum = ['totale_casi', 'ricoverati_con_sintomi', 'terapia_intensiva', 'totale_ospedalizzati',
                  'isolamento_domiciliare', 'totale_positivi', 'variazione_totale_positivi', 'nuovi_positivi',
                  'dimessi_guariti', 'deceduti', 'totale_casi', 'tamponi']
columns_to_exclude = ['data', 'stato', 'codice_regione', 'denominazione_regione', 'lat', 'long']
agg_functions = {}
for col in columns_to_sum:
    agg_functions[col] = 'sum'
for col in columns_to_exclude:
    agg_functions[col] = 'first'
df = df.groupby(['data', 'codice_regione']).aggregate(agg_functions)

df['date'] = pd.to_datetime(df['data'].str[:10], format='%Y-%m-%d')
current = df[df['date']==pd.to_datetime('15-05-2024',dayfirst=True)]

data= current[['codice_regione','totale_casi', 'denominazione_regione']].copy()
data.rename(columns={'totale_casi': 'Cases'}, inplace=True)


covid_data = data

hover_data = {'codice_regione': True, 'Cases': True, 'denominazione_regione': True}

fig = px.choropleth(
    covid_data,
    geojson=italy_geojson,
    locations='codice_regione',
    featureidkey='properties.reg_istat_code_num',
    color='Cases',
    labels={'Cases': 'Number of Cases'},
    title='COVID-19 Cases in Italy by Region',
    color_continuous_scale=plotly_settings.color_palette(),
    scope="europe",
    hover_data = hover_data
                   )
fig.update_geos(showcountries=False, showcoastlines=False, showland=False, fitbounds="locations")
#fig.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(
    title_text="COVID-19 Cases in Italy by region",
    title_x=0.5)

fig.write_html('../plots/regions_total.html')
fig.write_image("../plots/regions_total.png")
