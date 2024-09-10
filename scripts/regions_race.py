import pandas as pd
import geopandas as gpd
import numpy as np

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.io as pio
import os

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.axes_grid1 import make_axes_locatable

import plotly_settings
import json
import bar_chart_race as bcr

with open('../data/italy-regions.json') as json_file:
    italy_geojson = json.load(json_file)
df_regions = pd.read_csv('../data/dpc-covid19-ita-regioni.csv')
df_regions['codice_regione'] = df_regions['codice_regione'].replace({21: 4, 22: 4})
df_regions['denominazione_regione'] = df_regions['denominazione_regione'].replace({'P.A. Bolzano': 'Trentino-Alto Adige/Südtirol',
                                     'P.A. Trento': 'Trentino-Alto Adige/Südtirol'})

columns_to_last = ['totale_casi']
columns_to_exclude = ['data', 'stato', 'denominazione_regione', 'lat', 'long']
agg_functions = {}
for col in columns_to_last:
    agg_functions[col] = 'last'
for col in columns_to_exclude:
    agg_functions[col] = 'first'


df_regions = df_regions.groupby(['data', 'codice_regione']).aggregate(agg_functions).drop(columns='data').reset_index()
df_regions['date'] = pd.to_datetime(df_regions['data'].str[:10], format='%Y-%m-%d')

#%%
animation_len = plotly_settings.animation_len()


df_regions_weekly = df_regions.groupby('codice_regione').resample('W-Mon', on='date').aggregate(agg_functions).reset_index().sort_values(by='date')
for_race = df_regions_weekly[['date', 'denominazione_regione', 'totale_casi']]
data_race = for_race.pivot(index = 'date', columns = 'denominazione_regione', values = 'totale_casi')
test = data_race[:10]

df = data_race
len_of_period = np.ceil(animation_len * 1000 / len(df))
bcr.bar_chart_race(
    df=df,
    filename='../plots/regions_race.gif',
    orientation='h',
    sort='desc',
    n_bars=6,
    fixed_order=False,
    fixed_max=False,
    steps_per_period=5,
    interpolate_period=False,
    label_bars=True,
    bar_size=.95,
    tick_label_size=10,
    period_label={'x': .99, 'y': .25, 'ha': 'right', 'va': 'center'},
    period_fmt='%B, %Y',
    period_summary_func=lambda v, r: {'x': .99, 'y': .18,
                                      's': f'Total cases: {v.sum():,.0f}',
                                      'ha': 'right', 'size': 8, 'family': 'Courier New'},
    period_length=len_of_period,
    figsize=(6, 4),
    dpi=144,
    cmap='t10',
    title='COVID-19 cases by region',
    title_size='larger',
    scale='linear',
    writer=None,
    fig=None,
    bar_kwargs={'alpha': .7},
    filter_column_colors=True)
