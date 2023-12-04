import matplotlib.pyplot as plt
import pandas as pd

file_path = "/home/yimoning/research/pydevs/pyjoulse_test/result1.csv"
df = pd.read_csv(file_path, sep=';')
df = df.drop(columns=['tag'])
df['cumulative_time'] = df['duration'].cumsum()
columns = ['package_0', 'dram_0', 'core_0', 'uncore_0']
for col in columns:
    df[col] = df[col].astype(float)
df.set_index('cumulative_time', inplace=True)

df.index = pd.to_timedelta(df.index, unit='s')

df_avg = df.resample('15S').mean()
df_avg = df_avg.ffill()

columns = ['package_0', 'dram_0', 'core_0', 'uncore_0']
for col in columns:
    plt.figure(figsize=(10, 6))
    plt.step(df_avg.index, df_avg[col], label=col, where='post')
    plt.title(col)
    plt.xlabel('Time (s)')
    plt.ylabel('Value')
    plt.legend()
    plt.grid(True)
    plt.show()
