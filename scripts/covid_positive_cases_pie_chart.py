import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def covid_positive_cases_pie_chart(df_italy):
    df = df_italy[['date', 'region_name', 'total_positive_molecular_test', 'total_positive_rapid_antigenic_test']]

    df['date'] = pd.to_datetime(df['date'])
    df['month_end'] = df['date'].dt.is_month_end
    last_days_data = df[df['month_end']]
    df_groupped = last_days_data.groupby('date').agg({
        'total_positive_molecular_test': 'sum',
        'total_positive_rapid_antigenic_test': 'sum'
    }).reset_index()

    df_groupped = df_groupped.loc[
        (df_groupped['total_positive_molecular_test'] != 0) |
        (df_groupped['total_positive_rapid_antigenic_test'] != 0)
    ]

    df = df_groupped
    df['date'] = pd.to_datetime(df['date'])
    df['year_month'] = df['date'].dt.strftime('%Y-%m')
    fig, ax = plt.subplots()

    def update(num):
        ax.clear()
        year_month = df['year_month'].iloc[num]
        positive_molecular = df['total_positive_molecular_test'].iloc[num]
        positive_rapid = df['total_positive_rapid_antigenic_test'].iloc[num]
        sizes = [positive_molecular, positive_rapid]
        labels = [
            f'Molecular test\n{positive_molecular / 1000:,.0f}K',
            f'Rapid antigenic test\n{positive_rapid / 1000:,.0f}K'
        ]

        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        ax.set_title(f'COVID-19 Molecular vs Rapid antigenic test in Italy\n{year_month}', fontsize=16)

    ani = animation.FuncAnimation(fig, update, frames=len(df), repeat=True, interval=500)
    gif_path = '../plots/covid_positive_cases_pie_chart.gif'
    ani.save(gif_path, writer='pillow')