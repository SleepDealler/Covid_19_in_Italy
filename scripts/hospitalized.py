import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def hospitalized(df_italy,df_poland):
	df_poland['date'] = pd.to_datetime(df_poland['date'])
	df_poland['year_month'] = df_poland['date'].dt.to_period('M')
	df_poland_monthly_sum = df_poland.groupby('year_month')['hosp_patients'].sum().reset_index()
	df_poland_monthly_sum['year_month'] = df_poland_monthly_sum['year_month'].dt.to_timestamp()
	df_poland_monthly_sum.rename(columns={'year_month': 'date', 'hosp_patients': 'monthly_hosp_patients'}, inplace=True)

	df_italy['date'] = pd.to_datetime(df_italy['date'])
	df_italy['year_month'] = df_italy['date'].dt.to_period('M')
	df_italy_monthly_sum = df_italy.groupby('year_month')['total_hospitalized'].sum().reset_index()
	df_italy_monthly_sum['year_month'] = df_italy_monthly_sum['year_month'].dt.to_timestamp()
	df_italy_monthly_sum.rename(columns={'year_month': 'date', 'total_hospitalized': 'monthly_total_hospitalized'}, inplace=True)

	df_pol = df_poland_monthly_sum
	df_ita = df_italy_monthly_sum
	df_pol['date'] = pd.to_datetime(df_pol['date'])
	df_ita['date'] = pd.to_datetime(df_ita['date'])
	df_pol['year_month'] = df_pol['date'].dt.to_period('M')
	df_ita['year_month'] = df_ita['date'].dt.to_period('M')
	df_pol_monthly_sum = df_pol.groupby('year_month')['monthly_hosp_patients'].sum().reset_index()
	df_ita_monthly_sum = df_ita.groupby('year_month')['monthly_total_hospitalized'].sum().reset_index()
	df_combined = pd.merge(df_pol_monthly_sum, df_ita_monthly_sum, on='year_month', suffixes=('_pol', '_ita'))
	df_combined['year_month'] = df_combined['year_month'].dt.to_timestamp()
	df_combined.rename(columns={'year_month': 'date', 'monthly_hosp_patients': 'pol_hosp', 'monthly_total_hospitalized': 'ita_hosp'}, inplace=True)

	fig, ax = plt.subplots()

	def update(num):
		ax.clear()
		date = df_combined['date'].iloc[num]
		pol_hosp = df_combined['pol_hosp'].iloc[num] / 1000
		ita_hosp = df_combined['ita_hosp'].iloc[num] / 1000
		bars = ax.bar(['Poland', 'Italy'], [pol_hosp, ita_hosp], color=['blue', 'green'], label=['Poland', 'Italy'])
		ax.set_ylim(0, max(df_combined['pol_hosp'].max(), df_combined['ita_hosp'].max()) / 1000 * 1.1)
		ax.set_ylabel('Total Hospitalized (in thousands)')
		ax.set_title(f'Total Hospitalized Patients\n{date.strftime("%B %Y")}', fontsize=16)
		for bar in bars:
			height = bar.get_height()
			ax.annotate(f'{height:,.0f}K', xy=(bar.get_x() + bar.get_width() / 2, height), 
					xytext=(0, 3), textcoords="offset points", ha='center', va='bottom')
    
		ax.legend()

	ani = animation.FuncAnimation(fig, update, frames=len(df_combined), repeat=True, interval=1000)
	gif_path = '../plots/poland_italy_hospitalized_bar_chart.gif'
	ani.save(gif_path, writer='pillow')