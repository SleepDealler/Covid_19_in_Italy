import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.dates import DateFormatter
import pandas as pd

def Mortality_regions(data):
    regions = ["Lazio", "Lombardia", "Campania", "Piemonte", "Sicilia"]
    filtered_data = data[data['region_name'].isin(regions)][['date', 'region_name', 'deceased']]
    filtered_data['date'] = pd.to_datetime(filtered_data['date'])
    filtered_data.set_index('date', inplace=True)
    monthly_data = filtered_data.groupby('region_name').resample('ME').last().reset_index(level=1)

    pivot_data = monthly_data.pivot(index='date', columns='region_name', values='deceased').fillna(0)
    pivot_data = pivot_data.sort_index()
    x_limits = (pivot_data.index.min(), pivot_data.index.max())
    y_limit = pivot_data.max().max() + 10

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_title("Total mortality in 5 most populated regions in Italy", fontsize=24)
    ax.set_xlabel("Date", fontsize=18)
    ax.set_ylabel("Number of Deceased", fontsize=18)
    date_format = DateFormatter("%Y-%m")
    ax.xaxis.set_major_formatter(date_format)
    ax.xaxis.set_tick_params(rotation=45)
    ax.set_xlim(x_limits)
    ax.set_ylim(0, y_limit)

    lines = {region: ax.plot([], [], label=region)[0] for region in regions}

    def init():
        for line in lines.values():
            line.set_data([], [])
        return lines.values()

    def update(frame):
        for region in regions:
            lines[region].set_data(pivot_data.index[:frame], pivot_data[region].values[:frame])
        return lines.values()

    ax.legend()
    plt.grid(color='grey', linestyle='-', linewidth=0.5)
    plt.tight_layout(pad=2.0)
    ani = animation.FuncAnimation(fig, update, frames=len(pivot_data), init_func=init, blit=True, repeat=False)
    gif_path = '../plots/region_mortality_monthly.gif'
    ani.save(gif_path, writer='pillow')


