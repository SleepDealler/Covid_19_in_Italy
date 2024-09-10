import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from PIL import Image

def ic_vs_d(data):
    data['date'] = pd.to_datetime(data['date'])
    selected_regions = ['Lazio', 'Lombardia', 'Campania', 'Piemonte', 'Sicilia']

    filtered_data = data[data['region_name'].isin(selected_regions)][['date', 'region_name', 'intensive_care', 'deceased']]
    filtered_data.set_index('date', inplace=True)
    monthly_data = filtered_data.groupby([pd.Grouper(freq='MS'), 'region_name']).sum().reset_index()
    monthly_data['monthly_deceased'] = monthly_data.groupby('region_name')['deceased'].diff().fillna(monthly_data['deceased'])
    monthly_data['monthly_deceased'] = monthly_data['monthly_deceased'].apply(lambda x: max(x, 0))
    fig, ax = plt.subplots(figsize=(12, 7))

    x_limits = (0, monthly_data['intensive_care'].max())
    y_limits = (0, monthly_data['monthly_deceased'].max())
    bubble_size_factor = 0.1

    def update_bubble(num):
        ax.clear()
        date = pd.Timestamp(monthly_data['date'].unique()[num])
        for region in selected_regions:
            region_data = monthly_data[(monthly_data['region_name'] == region) & (monthly_data['date'] == date)]
            ax.scatter(region_data['intensive_care'], region_data['monthly_deceased'],
                       s=region_data['intensive_care'] / bubble_size_factor, label=region, alpha=0.7)
        
        ax.set_title(f'COVID-19 intensive care and deceased correlation in Italy {date.strftime("%Y-%m")}', fontsize=24)
        ax.set_xlim(x_limits)
        ax.set_ylim(y_limits)
        ax.set_xlabel('Monthly intensive care', fontsize = 16)
        ax.set_ylabel('Monthly deceased', fontsize = 16)
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: f'{int(x/1e3)}'))
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: f'{int(x/1e3)}k'))
        ax.grid(True, linestyle='-')

        handles, labels = ax.get_legend_handles_labels()
        for handle in handles:
            handle.set_sizes([100])
        ax.legend(handles, labels, loc='upper right')

        plt.tight_layout()

    frames = []

    for i in range(len(monthly_data['date'].unique())):
        update_bubble(i)
        fig.canvas.draw()
        frame = Image.frombytes('RGB', fig.canvas.get_width_height(), fig.canvas.tostring_rgb())
        frames.append(frame)

    output_path = '../plots/italy_intensive_care_vs_deceased.gif'
    frames[0].save(output_path, save_all=True, append_images=frames[1:], duration=1000, loop=0)
