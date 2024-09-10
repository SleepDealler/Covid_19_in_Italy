import pandas as pd
import most_and_less, covid_positive_cases_pie_chart, hospitalized, vaccin_pred
import mortality_regions, intensive_care_deceased


df_italy = pd.read_csv('../data/dpc-covid19-ita-regioni.csv')
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
df_italy.drop(['region_code', 'lat', 'long', 'total_positivity_change', 'new_positive', 'note', 'test_notes', 'case_notes', 'nuts_code_1', 'nuts_code_2'], axis=1, inplace=True)
df_italy.fillna(0, inplace=True)

'''
This part was used to prepare filtered dataset. Row owi_data were too big to send with project.

df_world = pd.read_csv('../data/owid-covid-data.csv')
df_world_filtered = df_world[df_world['location'].isin(['Poland', 'Italy'])]
df_world_filtered.to_csv('../data/owid-covid-data_filtered.csv', index=False)
'''

df_world = pd.read_csv('../data/owid-covid-data_filtered.csv')
df_poland = df_world[df_world['location'] == 'Poland']

most_and_less.most_and_less(df_italy)
covid_positive_cases_pie_chart.covid_positive_cases_pie_chart(df_italy)
hospitalized.hospitalized(df_italy,df_poland)
vaccin_pred.vaccin_pred(df_world)
mortality_regions.Mortality_regions(df_italy)
intensive_care_deceased.ic_vs_d(df_italy)
