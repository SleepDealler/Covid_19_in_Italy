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
import matplotlib.ticker as ticker

import plotly_settings
#%%
df_provinces = pd.read_csv('../data/dpc-covid19-ita-province.csv')
df_provinces['date'] = pd.to_datetime(df_provinces['data'].str[:10], format='%Y-%m-%d')
current = df_provinces[df_provinces['date']==pd.to_datetime('15-05-2024',dayfirst=True)]
data = current[['codice_provincia','totale_casi', 'denominazione_provincia']].copy()
data.rename(columns={'totale_casi': 'Cases'}, inplace=True)


# 1. Identify Columns to Sum and Exclude
columns_to_last = ['totale_casi']
columns_to_exclude = ['data', 'stato', 'codice_regione', 'denominazione_regione', 'lat', 'long',  'denominazione_provincia']
agg_functions = {}
for col in columns_to_last:
    agg_functions[col] = 'median'
for col in columns_to_exclude:
    agg_functions[col] = 'first'

#%%
df_provinces_weekly = df_provinces.groupby('codice_provincia').resample('W-Mon', on='date').aggregate(agg_functions).reset_index().sort_values(by='date')

animation_len = plotly_settings.animation_len()

import json
with open('../data/italy-provinces.json') as json_file:
    italy_geojson = json.load(json_file)


covid_data = df_provinces_weekly # [df_provinces_weekly['date']<'2020-05-05']
italy_gdf = gpd.GeoDataFrame.from_features(italy_geojson['features'])
merged = italy_gdf.merge(covid_data, left_on='prov_istat_code_num', right_on='codice_provincia')

#%%


def update(date):
    plt.clf()
    ax = plt.gca()
    current_data = merged[merged['date'] == date]
    current_data.plot(column='totale_casi', cmap=plotly_settings.color_palette_plt(), linewidth=0.5,
                      ax=ax, edgecolor = 'gray', legend=True, legend_kwds={'shrink': 0.5, 'aspect': 20})
    ax.set_title(
    f'COVID-19 Cases in Italy',
    fontdict={'fontsize':'22', 'fontweight':'10'})
    ax.text(0.45, 0.1, date.strftime("%B, %Y"), transform=ax.transAxes, color='#777777', size=20, ha='right', va='top', weight=800)
    plt.axis('off')

dates = merged['date'].unique()
fig, ax = plt.subplots(1, figsize=(8, 8))


#%%
fig.subplots_adjust(left=0, right=1, bottom=0, top=1)

ani = FuncAnimation(fig, update, frames=dates, repeat=False)
fps = np.ceil(len(dates) / animation_len)
ani.save('../plots/regions_animation.gif', writer='Pillow',fps=fps, dpi=400)