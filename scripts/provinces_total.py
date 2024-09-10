import json

import pandas as pd
import plotly.express as px
import plotly_settings

with open('../data/italy-provinces.json') as json_file:
    italy_geojson = json.load(json_file)

df = pd.read_csv('../data/dpc-covid19-ita-province.csv')
df['date'] = pd.to_datetime(df['data'].str[:10], format='%Y-%m-%d')

df['date'] = pd.to_datetime(df['data'].str[:10], format='%Y-%m-%d')
current = df[df['date'] == pd.to_datetime('15-05-2024', dayfirst=True)]
data = current[['codice_provincia', 'totale_casi', 'denominazione_provincia']].copy()

data.rename(columns={
    'codice_provincia': 'Province Code',
    'totale_casi': 'Total Cases',
    'denominazione_provincia': 'Province Name'
}, inplace=True)

hover_data = {
    'Province Code': True,
    'Total Cases': True,
    'Province Name': True
}
covid_data = data

fig = px.choropleth(
    data,
    geojson=italy_geojson,
    locations='Province Code',
    featureidkey='properties.prov_istat_code_num',
    color='Total Cases',
    labels={'Total Cases': 'Number of Cases'},
    color_continuous_scale=plotly_settings.color_palette(),
    scope="europe",
    hover_data=hover_data
)

fig.update_geos(showcountries=False, showcoastlines=False, showland=False, fitbounds="locations")
#fig.update_layout(margin={"r": 0, "t": 40, "l": 0, "b": 0})
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(
    title_text="COVID-19 Cases in Italy by province",
    title_x=0.5)

fig.write_html('../plots/total_provinces.html')
fig.write_image("../plots/total_provinces.png")

