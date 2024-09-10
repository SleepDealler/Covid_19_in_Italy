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
sesso_filtered = sesso[sesso['AGE_GROUP']!='Non noto']


sum_by_gender = sesso_filtered.groupby(['AGE_GROUP']).sum().drop(columns='SESSO')
total_cases = sum_by_gender['CASI_CUMULATIVI'].sum()
sum_by_gender['Percentage'] = (sum_by_gender['CASI_CUMULATIVI'] / total_cases) * 100

population = pd.read_csv('../data/population_italy.csv',sep=';')
population = population.drop(columns=['males','females'])
population=population[:-1]
population['Age'] = population['Age'].astype(int)
bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 101]
labels = ['0-9', '10-19', '20-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80-89', '>90']


population['Age Group'] = pd.cut(population['Age'], bins=bins, labels=labels, right=False)
grouped_df = population.groupby('Age Group', observed=False).sum().drop(columns='Age')
total_cases = grouped_df['total'].sum()
grouped_df['Percentage'] = (grouped_df['total'] / total_cases) * 100


C = sum_by_gender['Percentage']
surplus_C = np.maximum(sum_by_gender['Percentage'] - grouped_df['Percentage'], 0)

A=grouped_df['Percentage']
surplus_A = np.maximum(-sum_by_gender['Percentage'] + grouped_df['Percentage'], 0)


trace_male = go.Bar(x=-A.values,
                	y=A.index,
                	orientation="h",
                	name="Population structure",
                	marker=dict(color="#1f77b4"),
					offsetgroup=1
					)

trace_female = go.Bar(x=C.values,
                	y=C.index,
                  	orientation="h",
                  	name="COVID cases",
					offsetgroup=1
					)
surplus_m = go.Bar(x=-surplus_A,
                	y=A.index,
                	orientation="h",
                	name="COVID underprevalance",
					offsetgroup=0
					)
surplus_k = go.Bar(x=surplus_C,
                	y=C.index,
                	orientation="h",
                	name="COVID overprevalance",
					offsetgroup=3
					)
layout = go.Layout(title="Population vs. number of cases",
               	xaxis=dict(title="Normalized count"),
               	yaxis=dict(title="Age"),
               	barmode="relative",
               	bargap=0.1)

fig = go.Figure(data=[trace_male, trace_female,surplus_m,surplus_k ], layout=layout)
fig.write_html('../plots/age_pyramid.html')
fig.write_image("../plots/age_pyramid.png")

