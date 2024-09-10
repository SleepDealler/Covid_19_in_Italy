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
sesso = sesso.iloc[:,:-1]
sesso['Mortality'] = (sesso['DECEDUTI']/sesso['CASI_CUMULATIVI'])
sesso['Mortality'] = round(sesso['Mortality'],4)
sesso = sesso[sesso['AGE_GROUP']!= 'Non noto']

F_mort = sesso[sesso['SESSO']=='F']
M_mort = sesso[sesso['SESSO']=='M']


fig = go.Figure()

fig.add_trace(go.Bar(x=F_mort['AGE_GROUP'], y=F_mort['Mortality'], name = 'Female',
                     # text=[f'{val:.2%}' for val in F_mort['Mortality']],
                     # textposition='outside',
                     hovertemplate='Age Group: %{x}<br>Mortality: %{y:.2%}',
                     ))
fig.add_trace(go.Bar(x=M_mort['AGE_GROUP'], y=M_mort['Mortality'], name = 'Male',
                     # text=[f'{val:.2%}' for val in M_mort['Mortality']],
                     # textposition='outside',
                     hovertemplate='Age Group: %{x}<br>Mortality: %{y:.2%}',
                     ))

fig.update_layout(
    title='COVID Mortality in age groups',
    yaxis=dict(
        title='Mortality [%]',
        tickformat=".0%",
    ),
    barmode='group',
    bargap=0.15,
    bargroupgap=0.1,

)
fig.write_html('../plots/mortality.html')
fig.write_image("../plots/mortality.png")
