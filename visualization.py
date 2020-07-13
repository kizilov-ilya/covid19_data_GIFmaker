import pandas as pd
import matplotlib.pyplot as plt
import glob
import moviepy.editor as mpy
import csv
from datetime import datetime, timedelta
from tqdm import tqdm

start_date = datetime(2020, 3, 1)
date_delta = (datetime.now() - start_date).days
file = "C:\\Users\\Ilya\\PycharmProjects\\Sketches\\corona_stat\\choosed_country.csv"

# Section 2
df = pd.read_csv('users_mod.csv', parse_dates=['date'])

# Section 3
df['rate'] = df['amount']

# Section 4

df_current = df[df['date'] == datetime.now().date()]
top_states_rate = ['Confirmed', 'Deaths', 'Recovered']
# Section 5

df = df[df['state'].isin(top_states_rate)]
df = df[df['date'] >= '2020-03-01']
df = df.pivot(index='date', columns='state', values='rate')

# Section 6

df = df.reset_index()
df = df.reset_index(drop=True)
df = df.drop(columns='date')

# Section 6.5

with open(file, 'r', newline='') as file:
    reader = csv.reader(file)
    filename = ''
    for row in reader:
        filename = str(row[0])

# Section 7

plt.style.use('fivethirtyeight')
length = len(df.index)
for i in tqdm(range(10, length + 10)):
    ax = df.iloc[:i].plot(figsize=(16, 9), linewidth=2,
                          color=['#9932CC', '#FF0000', '#7CFC00'])
    ax.set_xlabel('День отсчета от 01.03.2020')
    ax.set_ylabel('# Количество относительно времени')
    ax.set_title(f"Случаи за все время в {filename}", fontsize=18)
    ax.legend(loc='upper left', frameon=False)
    ax.grid(axis='x')
    fig = ax.get_figure()
    fig.savefig(f".\\pngs\\{i}pngs.png")
    plt.close(fig=fig)
# Section 8

gif_name = f'COVID_{filename}.gif'
fps = 6
file_list = glob.glob('.\\pngs\\*')
clip = mpy.ImageSequenceClip(file_list, fps=fps)
clip.write_gif(f'{gif_name}', fps=fps)
